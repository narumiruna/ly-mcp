import json
from typing import Any

import pytest

from lymcp import api
from lymcp import server
from tests.fixtures import load_json_fixture

SAMPLE_RESPONSE = {"ok": True}


LIST_CONTRACT_CASES = [
    ("list_bills", "ListBillRequest", "bills_list.json", "bills"),
    ("list_gazettes", "ListGazettesRequest", "gazettes_list.json", "gazettes"),
    ("list_laws", "ListLawsRequest", "laws_list.json", "laws"),
    ("list_legislators", "ListLegislatorsRequest", "legislators_list.json", "legislators"),
    ("list_meets", "ListMeetsRequest", "meets_list.json", "meets"),
]


class StubRequest:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response

    async def do(self) -> dict[str, Any]:
        return self.response


@pytest.mark.asyncio
async def test_get_stat_returns_fixture_json(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_response = load_json_fixture("stat.json")

    monkeypatch.setattr(server, "GetStatRequest", lambda: StubRequest(expected_response))

    response_text = await server.get_stat()

    assert json.loads(response_text) == expected_response


@pytest.mark.asyncio
async def test_list_bills_returns_fixture_json(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_response = load_json_fixture("bills_list.json")
    calls: list[dict[str, Any]] = []

    class StubListBillRequest(StubRequest):
        def __init__(self, **kwargs: Any) -> None:
            calls.append(kwargs)
            super().__init__(expected_response)

    monkeypatch.setattr(server, "ListBillRequest", StubListBillRequest)

    response_text = await server.list_bills(
        term=11,
        bill_type="法律案",
        proposal_unit_or_member="王世堅",
        limit=1,
    )

    assert json.loads(response_text) == expected_response
    assert calls == [
        {
            "session": None,
            "term": 11,
            "bill_flow_status": None,
            "bill_type": "法律案",
            "proposer": None,
            "co_proposer": None,
            "law_number": None,
            "bill_status": None,
            "meeting_code": None,
            "proposal_source": None,
            "bill_number": None,
            "proposal_number": None,
            "reference_number": None,
            "article_number": None,
            "proposal_date": None,
            "proposal_unit_or_member": "王世堅",
            "page": 1,
            "limit": 1,
            "output_fields": [],
        }
    ]


@pytest.mark.asyncio
async def test_get_bill_returns_fixture_json(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_response = load_json_fixture("bill_detail.json")
    calls: list[dict[str, Any]] = []

    class StubGetBillRequest(StubRequest):
        def __init__(self, **kwargs: Any) -> None:
            calls.append(kwargs)
            super().__init__(expected_response)

    monkeypatch.setattr(server, "GetBillRequest", StubGetBillRequest)

    response_text = await server.get_bill("202110213410000")

    assert json.loads(response_text) == expected_response
    assert calls == [{"bill_no": "202110213410000"}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "request_class_name", "call_kwargs", "url"),
    [
        (
            "get_bill",
            "GetBillRequest",
            {"bill_no": "invalid_bill_number"},
            f"{api.BASE_URL}/bills/invalid_bill_number",
        ),
        (
            "get_law_version",
            "GetLawVersionRequest",
            {"law_version_id": "invalid_law_version"},
            f"{api.BASE_URL}/law_versions/invalid_law_version",
        ),
    ],
)
async def test_detail_tool_returns_structured_http_status_error(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    request_class_name: str,
    call_kwargs: dict[str, Any],
    url: str,
) -> None:
    class StubErrorRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs

        async def do(self) -> dict[str, Any]:
            raise api.LymcpApiError(
                "http_status",
                f"Upstream API returned HTTP 404 for {url}",
                url=url,
                status_code=404,
                response_excerpt="not found",
            )

    monkeypatch.setattr(server, request_class_name, StubErrorRequest)

    response_text = await getattr(server, tool_name)(**call_kwargs)
    response = json.loads(response_text)

    assert response["ok"] is False
    assert response["error"] == {
        "type": "http_status",
        "message": f"Upstream API returned HTTP 404 for {url}",
        "url": url,
        "status_code": 404,
        "response_excerpt": "not found",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(("tool_name", "request_class_name", "fixture_name", "collection_key"), LIST_CONTRACT_CASES)
async def test_list_tool_returns_collection_contract(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    request_class_name: str,
    fixture_name: str,
    collection_key: str,
) -> None:
    expected_response = load_json_fixture(fixture_name)

    monkeypatch.setattr(server, request_class_name, lambda **_: StubRequest(expected_response))

    response_text = await getattr(server, tool_name)(limit=1)
    response = json.loads(response_text)

    assert isinstance(response["total"], int)
    assert isinstance(response["total_page"], int)
    assert response["page"] == 1
    assert response["limit"] == 1
    assert isinstance(response["filter"], dict)
    assert isinstance(response["id_fields"], list)
    assert isinstance(response[collection_key], list)
    assert response[collection_key]
    assert isinstance(response["supported_filter_fields"], list)
    assert response["supported_filter_fields"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "request_class_name", "call_kwargs"),
    [
        ("get_bill_related_bills", "GetBillRelatedBillsRequest", {"bill_no": "202110213410000", "limit": 1}),
        ("get_bill_meets", "GetBillMeetsRequest", {"bill_no": "202110213410000", "term": 11, "limit": 1}),
        ("get_bill_doc_html", "GetBillDocHtmlRequest", {"bill_no": "202110213410000"}),
        ("list_committees", "ListCommitteesRequest", {"limit": 1}),
        ("get_committee", "GetCommitteeRequest", {"comt_cd": "16"}),
        ("get_committee_meets", "GetCommitteeMeetsRequest", {"comt_cd": "16", "term": 11, "limit": 1}),
        ("list_gazettes", "ListGazettesRequest", {"limit": 1}),
        ("get_gazette", "GetGazetteRequest", {"gazette_id": "1137701"}),
        ("get_gazette_agendas", "GetGazetteAgendasRequest", {"gazette_id": "1137701", "term": 11, "limit": 1}),
        ("list_gazette_agendas", "ListGazetteAgendasRequest", {"term": 11, "limit": 1}),
        ("get_gazette_agenda", "GetGazetteAgendaRequest", {"gazette_agenda_id": "1137701_00001"}),
        ("list_interpellations", "ListInterpellationsRequest", {"interpellation_member": "羅智強", "limit": 1}),
        ("get_interpellation", "GetInterpellationRequest", {"interpellation_id": "11-1-1-1"}),
        (
            "get_legislator_interpellations",
            "GetLegislatorInterpellationsRequest",
            {"term": 11, "name": "韓國瑜", "limit": 1},
        ),
        ("list_ivods", "ListIvodsRequest", {"term": 11, "video_type": "Clip", "limit": 1}),
        ("get_ivod", "GetIvodRequest", {"ivod_id": "156045"}),
        ("get_meet_ivods", "GetMeetIvodsRequest", {"meet_id": "院會-11-2-3", "term": 11, "limit": 1}),
        ("list_laws", "ListLawsRequest", {"limit": 1}),
        ("get_law", "GetLawRequest", {"law_id": "09200015"}),
        ("get_law_progress", "GetLawProgressRequest", {"law_id": "09200015"}),
        ("get_law_bills", "GetLawBillsRequest", {"law_id": "09200015", "term": 11, "limit": 1}),
        ("get_law_versions", "GetLawVersionsRequest", {"law_id": "09200015", "limit": 1}),
        ("list_law_versions", "ListLawVersionsRequest", {"law_number": "90481", "limit": 1}),
        ("get_law_version", "GetLawVersionRequest", {"law_version_id": "90481:1944-02-29-制定"}),
        (
            "get_law_version_contents",
            "GetLawVersionContentsRequest",
            {"law_version_id": "90481:1944-02-29-制定", "law_number": "90481", "limit": 1},
        ),
        ("list_law_contents", "ListLawContentsRequest", {"law_number": "90481", "limit": 1}),
        ("get_law_content", "GetLawContentRequest", {"law_content_id": "90481:90481:1944-02-29-制定:0"}),
        ("list_legislators", "ListLegislatorsRequest", {"term": 11, "limit": 1}),
        ("get_legislator", "GetLegislatorRequest", {"term": 11, "name": "韓國瑜"}),
        (
            "get_legislator_propose_bills",
            "GetLegislatorProposeBillsRequest",
            {"term": 11, "name": "韓國瑜", "limit": 1},
        ),
        (
            "get_legislator_cosign_bills",
            "GetLegislatorCosignBillsRequest",
            {"term": 11, "name": "韓國瑜", "limit": 1},
        ),
        (
            "get_legislator_meets",
            "GetLegislatorMeetsRequest",
            {"term": 11, "name": "韓國瑜", "limit": 1},
        ),
        ("list_meets", "ListMeetsRequest", {"term": 11, "limit": 1}),
        ("get_meet", "GetMeetRequest", {"meet_id": "院會-11-2-3"}),
        ("get_meet_bills", "GetMeetBillsRequest", {"meet_id": "院會-11-2-3", "term": 11, "limit": 1}),
        (
            "get_meet_interpellations",
            "GetMeetInterpellationsRequest",
            {"meet_id": "院會-11-2-3", "term": 11, "limit": 1},
        ),
    ],
)
async def test_tool_returns_request_response(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    request_class_name: str,
    call_kwargs: dict[str, Any],
) -> None:
    calls: list[dict[str, Any]] = []

    class StubToolRequest(StubRequest):
        def __init__(self, **kwargs: Any) -> None:
            calls.append(kwargs)
            super().__init__(SAMPLE_RESPONSE)

    monkeypatch.setattr(server, request_class_name, StubToolRequest)

    response_text = await getattr(server, tool_name)(**call_kwargs)

    assert json.loads(response_text) == SAMPLE_RESPONSE
    assert len(calls) == 1
    for key, value in call_kwargs.items():
        expected_key = "co_proposer" if tool_name == "get_meet_bills" and key == "co_proposer" else key
        assert calls[0][expected_key] == value
