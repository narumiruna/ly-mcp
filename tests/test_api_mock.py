from collections.abc import Callable
from typing import Any

import httpx
import pytest

from lymcp import api
from tests.fixtures import load_json_fixture

RequestFactory = Callable[[], Any]
SAMPLE_RESPONSE = {"ok": True}


class FakeAsyncClient:
    def __init__(
        self,
        *,
        response: httpx.Response | None = None,
        error: Exception | None = None,
        timeout: float | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.timeout = timeout

    async def __aenter__(self) -> "FakeAsyncClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def get(self, url: str, params: dict[str, Any] | None = None) -> httpx.Response:
        if self.error is not None:
            raise self.error
        assert self.response is not None
        return self.response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("factory", "fixture_name", "expected_url", "expected_params"),
    [
        (
            api.GetStatRequest,
            "stat.json",
            f"{api.BASE_URL}/stat",
            None,
        ),
        (
            lambda: api.ListBillRequest(
                term=11,
                bill_type="法律案",
                proposal_unit_or_member="王世堅",
                limit=1,
            ),
            "bills_list.json",
            f"{api.BASE_URL}/bills",
            {
                "屆": 11,
                "議案類別": "法律案",
                "提案單位/提案委員": "王世堅",
                "page": 1,
                "limit": 1,
                "output_fields": [],
            },
        ),
        (
            lambda: api.GetBillRequest(bill_no="202110213410000"),
            "bill_detail.json",
            f"{api.BASE_URL}/bills/202110213410000",
            None,
        ),
        (
            lambda: api.ListGazettesRequest(limit=1),
            "gazettes_list.json",
            f"{api.BASE_URL}/gazettes",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetGazetteRequest(gazette_id="1137701"),
            "gazette_detail.json",
            f"{api.BASE_URL}/gazettes/1137701",
            None,
        ),
        (
            lambda: api.ListLawsRequest(category="母法", law_status="現行", authority="司法院", limit=1),
            "laws_list.json",
            f"{api.BASE_URL}/laws",
            {
                "類別": "母法",
                "法律狀態": "現行",
                "主管機關": "司法院",
                "page": 1,
                "limit": 1,
                "output_fields": [],
            },
        ),
        (
            lambda: api.GetLawRequest(law_id="09200015"),
            "law_detail.json",
            f"{api.BASE_URL}/laws/09200015",
            None,
        ),
        (
            lambda: api.ListLegislatorsRequest(
                term=11,
                party="台灣民眾黨",
                district_name="全國不分區及僑居國外國民",
                legislator_name="吳春城",
                limit=1,
            ),
            "legislators_list.json",
            f"{api.BASE_URL}/legislators",
            {
                "屆": 11,
                "黨籍": "台灣民眾黨",
                "選區名稱": "全國不分區及僑居國外國民",
                "委員姓名": "吳春城",
                "page": 1,
                "limit": 1,
                "output_fields": [],
            },
        ),
        (
            lambda: api.GetLegislatorRequest(term=11, name="韓國瑜"),
            "legislator_detail.json",
            f"{api.BASE_URL}/legislators/11/韓國瑜",
            None,
        ),
        (
            lambda: api.ListMeetsRequest(
                term=11,
                session=5,
                meeting_type="委員會",
                date="2026-05-18",
                committee_code=35,
                limit=1,
            ),
            "meets_list.json",
            f"{api.BASE_URL}/meets",
            {
                "屆": 11,
                "會期": 5,
                "會議種類": "委員會",
                "日期": "2026-05-18",
                "委員會代號": 35,
                "page": 1,
                "limit": 1,
                "output_fields": [],
            },
        ),
        (
            lambda: api.GetMeetRequest(meet_id="院會-11-2-3"),
            "meet_detail.json",
            f"{api.BASE_URL}/meets/院會-11-2-3",
            None,
        ),
    ],
)
async def test_request_uses_expected_endpoint_and_returns_fixture(
    monkeypatch: pytest.MonkeyPatch,
    factory: RequestFactory,
    fixture_name: str,
    expected_url: str,
    expected_params: dict[str, Any] | None,
) -> None:
    expected_response = load_json_fixture(fixture_name)
    calls: list[dict[str, Any]] = []

    async def fake_make_api_request(
        url: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        calls.append({"url": url, "method": method, "params": params})
        return expected_response

    monkeypatch.setattr(api, "make_api_request", fake_make_api_request)

    response = await factory().do()

    assert response == expected_response
    assert calls == [{"url": expected_url, "method": "GET", "params": expected_params}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("factory", "expected_url", "expected_params"),
    [
        (
            lambda: api.GetBillMeetsRequest(bill_no="202110213410000", term=11, limit=1),
            f"{api.BASE_URL}/bills/202110213410000/meets",
            {"屆": 11, "page": 1, "limit": 1},
        ),
        (
            lambda: api.GetBillRelatedBillsRequest(bill_no="202110213410000", limit=1),
            f"{api.BASE_URL}/bills/202110213410000/related_bills",
            {"page": 1, "limit": 1},
        ),
        (
            lambda: api.GetBillDocHtmlRequest(bill_no="202110213410000"),
            f"{api.BASE_URL}/bills/202110213410000/doc_html",
            None,
        ),
        (
            lambda: api.ListCommitteesRequest(limit=1),
            f"{api.BASE_URL}/committees",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetCommitteeRequest(comt_cd="16"),
            f"{api.BASE_URL}/committees/16",
            None,
        ),
        (
            lambda: api.GetCommitteeMeetsRequest(comt_cd="16", term=11, limit=1),
            f"{api.BASE_URL}/committees/16/meets",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetGazetteAgendasRequest(gazette_id="1137701", term=11, limit=1),
            f"{api.BASE_URL}/gazettes/1137701/agendas",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.ListGazetteAgendasRequest(term=11, limit=1),
            f"{api.BASE_URL}/gazette_agendas",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetGazetteAgendaRequest(gazette_agenda_id="1137701_00001"),
            f"{api.BASE_URL}/gazette_agendas/1137701_00001",
            None,
        ),
        (
            lambda: api.ListInterpellationsRequest(interpellation_member="羅智強", limit=1),
            f"{api.BASE_URL}/interpellations",
            {"質詢委員": "羅智強", "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetInterpellationRequest(interpellation_id="11-1-1-1"),
            f"{api.BASE_URL}/interpellations/11-1-1-1",
            None,
        ),
        (
            lambda: api.GetLegislatorInterpellationsRequest(term=11, name="韓國瑜", limit=1),
            f"{api.BASE_URL}/legislators/11/韓國瑜/interpellations",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.ListIvodsRequest(term=11, video_type="Clip", limit=1),
            f"{api.BASE_URL}/ivods",
            {"屆": 11, "影片種類": "Clip", "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetIvodRequest(ivod_id="156045"),
            f"{api.BASE_URL}/ivods/156045",
            None,
        ),
        (
            lambda: api.GetMeetIvodsRequest(meet_id="院會-11-2-3", term=11, limit=1),
            f"{api.BASE_URL}/meets/院會-11-2-3/ivods",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLawProgressRequest(law_id="09200015"),
            f"{api.BASE_URL}/laws/09200015/progress",
            None,
        ),
        (
            lambda: api.GetLawBillsRequest(law_id="09200015", term=11, limit=1),
            f"{api.BASE_URL}/laws/09200015/bills",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLawVersionsRequest(law_id="09200015", limit=1),
            f"{api.BASE_URL}/laws/09200015/versions",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.ListLawVersionsRequest(law_number="90481", current_version="非現行", limit=1),
            f"{api.BASE_URL}/law_versions",
            {"法律編號": "90481", "現行版本": "非現行", "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLawVersionRequest(law_version_id="90481:1944-02-29-制定"),
            f"{api.BASE_URL}/law_versions/90481:1944-02-29-制定",
            None,
        ),
        (
            lambda: api.GetLawVersionContentsRequest(
                law_version_id="90481:1944-02-29-制定",
                law_number="90481",
                limit=1,
            ),
            f"{api.BASE_URL}/law_versions/90481:1944-02-29-制定/contents",
            {"法律編號": "90481", "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.ListLawContentsRequest(law_number="90481", limit=1),
            f"{api.BASE_URL}/law_contents",
            {"法律編號": "90481", "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLawContentRequest(law_content_id="90481:90481:1944-02-29-制定:0"),
            f"{api.BASE_URL}/law_contents/90481:90481:1944-02-29-制定:0",
            None,
        ),
        (
            lambda: api.GetLegislatorProposeBillsRequest(term=11, name="韓國瑜", limit=1),
            f"{api.BASE_URL}/legislators/11/韓國瑜/propose_bills",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLegislatorCosignBillsRequest(term=11, name="韓國瑜", limit=1),
            f"{api.BASE_URL}/legislators/11/韓國瑜/cosign_bills",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetLegislatorMeetsRequest(term=11, name="韓國瑜", limit=1),
            f"{api.BASE_URL}/legislators/11/韓國瑜/meets",
            {"page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetMeetBillsRequest(meet_id="院會-11-2-3", term=11, limit=1),
            f"{api.BASE_URL}/meets/院會-11-2-3/bills",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
        (
            lambda: api.GetMeetInterpellationsRequest(meet_id="院會-11-2-3", term=11, limit=1),
            f"{api.BASE_URL}/meets/院會-11-2-3/interpellations",
            {"屆": 11, "page": 1, "limit": 1, "output_fields": []},
        ),
    ],
)
async def test_remaining_requests_use_expected_endpoint(
    monkeypatch: pytest.MonkeyPatch,
    factory: RequestFactory,
    expected_url: str,
    expected_params: dict[str, Any] | None,
) -> None:
    calls: list[dict[str, Any]] = []

    async def fake_make_api_request(
        url: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        calls.append({"url": url, "method": method, "params": params})
        return SAMPLE_RESPONSE

    monkeypatch.setattr(api, "make_api_request", fake_make_api_request)

    response = await factory().do()

    assert response == SAMPLE_RESPONSE
    assert calls == [{"url": expected_url, "method": "GET", "params": expected_params}]


@pytest.mark.asyncio
async def test_make_api_request_rejects_unsupported_method() -> None:
    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        await api.make_api_request(f"{api.BASE_URL}/stat", method="POST")


@pytest.mark.asyncio
async def test_make_api_request_wraps_http_status_error(monkeypatch: pytest.MonkeyPatch) -> None:
    url = f"{api.BASE_URL}/bills/invalid_bill_number"
    response = httpx.Response(
        404,
        request=httpx.Request("GET", url),
        text="not found",
    )

    monkeypatch.setattr(api.httpx, "AsyncClient", lambda **kwargs: FakeAsyncClient(response=response, **kwargs))

    with pytest.raises(api.LymcpApiError) as exc_info:
        await api.make_api_request(url)

    error = exc_info.value
    assert error.error_type == "http_status"
    assert error.status_code == 404
    assert error.url == url
    assert error.response_excerpt == "not found"


@pytest.mark.asyncio
async def test_make_api_request_wraps_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    url = f"{api.BASE_URL}/stat"

    monkeypatch.setattr(
        api.httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(error=httpx.TimeoutException("timed out"), **kwargs),
    )

    with pytest.raises(api.LymcpApiError) as exc_info:
        await api.make_api_request(url)

    error = exc_info.value
    assert error.error_type == "timeout"
    assert error.status_code is None
    assert error.url == url


@pytest.mark.asyncio
async def test_make_api_request_wraps_non_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    url = f"{api.BASE_URL}/stat"
    response = httpx.Response(
        200,
        request=httpx.Request("GET", url),
        text="<html>not json</html>",
    )

    monkeypatch.setattr(api.httpx, "AsyncClient", lambda **kwargs: FakeAsyncClient(response=response, **kwargs))

    with pytest.raises(api.LymcpApiError) as exc_info:
        await api.make_api_request(url)

    error = exc_info.value
    assert error.error_type == "invalid_json"
    assert error.status_code == 200
    assert error.url == url
    assert error.response_excerpt == "<html>not json</html>"
