import re
from pathlib import Path
from typing import Any
from typing import Protocol
from typing import cast
from typing import get_args
from typing import get_origin

import pytest
import yaml
from pydantic import BaseModel

from lymcp import api
from lymcp import cli
from lymcp import server

ENDPOINT_COVERAGE: dict[str, tuple[str, tuple[str, ...]]] = {
    "/stat": ("get_stat", ("stat",)),
    "/bills": ("list_bills", ("bills", "list")),
    "/bills/{billNo}": ("get_bill", ("bills", "get")),
    "/bills/{billNo}/related_bills": ("get_bill_related_bills", ("bills", "related")),
    "/bills/{billNo}/doc_html": ("get_bill_doc_html", ("bills", "doc-html")),
    "/bills/{billNo}/meets": ("get_bill_meets", ("bills", "meets")),
    "/committees": ("list_committees", ("committees", "list")),
    "/committees/{comtCd}": ("get_committee", ("committees", "get")),
    "/committees/{comtCd}/meets": ("get_committee_meets", ("committees", "meets")),
    "/gazettes": ("list_gazettes", ("gazettes", "list")),
    "/gazettes/{id}": ("get_gazette", ("gazettes", "get")),
    "/gazettes/{id}/agendas": ("get_gazette_agendas", ("gazettes", "agendas")),
    "/gazette_agendas": ("list_gazette_agendas", ("gazette-agendas", "list")),
    "/gazette_agendas/{id}": ("get_gazette_agenda", ("gazette-agendas", "get")),
    "/interpellations": ("list_interpellations", ("interpellations", "list")),
    "/interpellations/{id}": ("get_interpellation", ("interpellations", "get")),
    "/ivods": ("list_ivods", ("ivods", "list")),
    "/ivods/{id}": ("get_ivod", ("ivods", "get")),
    "/laws": ("list_laws", ("laws", "list")),
    "/laws/{id}": ("get_law", ("laws", "get")),
    "/laws/{id}/progress": ("get_law_progress", ("laws", "progress")),
    "/laws/{id}/bills": ("get_law_bills", ("laws", "bills")),
    "/laws/{id}/versions": ("get_law_versions", ("laws", "versions")),
    "/law_contents": ("list_law_contents", ("law-contents", "list")),
    "/law_contents/{id}": ("get_law_content", ("law-contents", "get")),
    "/law_versions": ("list_law_versions", ("law-versions", "list")),
    "/law_versions/{id}": ("get_law_version", ("law-versions", "get")),
    "/law_versions/{id}/contents": ("get_law_version_contents", ("law-versions", "contents")),
    "/legislators": ("list_legislators", ("legislators", "list")),
    "/legislators/{term}/{name}": ("get_legislator", ("legislators", "get")),
    "/legislators/{term}/{name}/propose_bills": (
        "get_legislator_propose_bills",
        ("legislators", "propose-bills"),
    ),
    "/legislators/{term}/{name}/cosign_bills": (
        "get_legislator_cosign_bills",
        ("legislators", "cosign-bills"),
    ),
    "/legislators/{term}/{name}/meets": ("get_legislator_meets", ("legislators", "meets")),
    "/legislators/{term}/{name}/interpellations": (
        "get_legislator_interpellations",
        ("legislators", "interpellations"),
    ),
    "/meets": ("list_meets", ("meets", "list")),
    "/meets/{id}": ("get_meet", ("meets", "get")),
    "/meets/{id}/ivods": ("get_meet_ivods", ("meets", "ivods")),
    "/meets/{id}/bills": ("get_meet_bills", ("meets", "bills")),
    "/meets/{id}/interpellations": ("get_meet_interpellations", ("meets", "interpellations")),
    "/votes": ("list_votes", ("votes", "list")),
    "/votes/{id}": ("get_vote", ("votes", "get")),
    "/votes/{id}/meets": ("get_vote_meets", ("votes", "meets")),
}


class RequestWithDo(Protocol):
    async def do(self) -> dict[str, object]: ...


REQUEST_COVERAGE: dict[str, str] = {
    "/stat": "GetStatRequest",
    "/bills": "ListBillRequest",
    "/bills/{billNo}": "GetBillRequest",
    "/bills/{billNo}/related_bills": "GetBillRelatedBillsRequest",
    "/bills/{billNo}/doc_html": "GetBillDocHtmlRequest",
    "/bills/{billNo}/meets": "GetBillMeetsRequest",
    "/committees": "ListCommitteesRequest",
    "/committees/{comtCd}": "GetCommitteeRequest",
    "/committees/{comtCd}/meets": "GetCommitteeMeetsRequest",
    "/gazettes": "ListGazettesRequest",
    "/gazettes/{id}": "GetGazetteRequest",
    "/gazettes/{id}/agendas": "GetGazetteAgendasRequest",
    "/gazette_agendas": "ListGazetteAgendasRequest",
    "/gazette_agendas/{id}": "GetGazetteAgendaRequest",
    "/interpellations": "ListInterpellationsRequest",
    "/interpellations/{id}": "GetInterpellationRequest",
    "/ivods": "ListIvodsRequest",
    "/ivods/{id}": "GetIvodRequest",
    "/laws": "ListLawsRequest",
    "/laws/{id}": "GetLawRequest",
    "/laws/{id}/progress": "GetLawProgressRequest",
    "/laws/{id}/bills": "GetLawBillsRequest",
    "/laws/{id}/versions": "GetLawVersionsRequest",
    "/law_contents": "ListLawContentsRequest",
    "/law_contents/{id}": "GetLawContentRequest",
    "/law_versions": "ListLawVersionsRequest",
    "/law_versions/{id}": "GetLawVersionRequest",
    "/law_versions/{id}/contents": "GetLawVersionContentsRequest",
    "/legislators": "ListLegislatorsRequest",
    "/legislators/{term}/{name}": "GetLegislatorRequest",
    "/legislators/{term}/{name}/propose_bills": "GetLegislatorProposeBillsRequest",
    "/legislators/{term}/{name}/cosign_bills": "GetLegislatorCosignBillsRequest",
    "/legislators/{term}/{name}/meets": "GetLegislatorMeetsRequest",
    "/legislators/{term}/{name}/interpellations": "GetLegislatorInterpellationsRequest",
    "/meets": "ListMeetsRequest",
    "/meets/{id}": "GetMeetRequest",
    "/meets/{id}/ivods": "GetMeetIvodsRequest",
    "/meets/{id}/bills": "GetMeetBillsRequest",
    "/meets/{id}/interpellations": "GetMeetInterpellationsRequest",
    "/votes": "ListVotesRequest",
    "/votes/{id}": "GetVoteRequest",
    "/votes/{id}/meets": "GetVoteMeetsRequest",
}


def swagger_contract() -> dict[str, Any]:
    swagger = Path(__file__).parents[1] / "swagger.yaml"
    return yaml.safe_load(swagger.read_text(encoding="utf-8"))


def swagger_paths() -> set[str]:
    swagger = Path(__file__).parents[1] / "swagger.yaml"
    return set(re.findall(r"^  (/[^:]+):$", swagger.read_text(encoding="utf-8"), flags=re.MULTILINE))


def sample_value(annotation: Any) -> object:
    candidates = (annotation, *get_args(annotation))
    if int in candidates:
        return 1
    if bool in candidates:
        return True
    if get_origin(annotation) is list:
        return ["field"]
    return "value"


@pytest.mark.asyncio
async def test_swagger_endpoints_match_mcp_tools_and_cli_commands() -> None:
    tools = await server.mcp.list_tools()

    assert set(ENDPOINT_COVERAGE) == swagger_paths()
    assert {tool for tool, _ in ENDPOINT_COVERAGE.values()} == {tool.name for tool in tools}
    assert {command for _, command in ENDPOINT_COVERAGE.values()} == set(cli.COMMAND_INVENTORY)


@pytest.mark.asyncio
async def test_swagger_query_parameters_are_serialized(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, object] = {}

    async def fake_make_api_request(
        url: str,
        method: str = "GET",
        params: dict[str, object] | None = None,
    ) -> dict[str, object]:
        del url, method
        captured_params.update(params or {})
        return {}

    monkeypatch.setattr(api, "make_api_request", fake_make_api_request)
    contract = swagger_contract()
    missing_by_endpoint: dict[str, list[str]] = {}

    assert set(REQUEST_COVERAGE) == swagger_paths()
    for endpoint, request_name in REQUEST_COVERAGE.items():
        request_class: type[BaseModel] = getattr(api, request_name)
        values = {name: sample_value(field.annotation) for name, field in request_class.model_fields.items()}
        captured_params.clear()

        request = cast(RequestWithDo, request_class(**values))
        await request.do()

        expected = {
            parameter["name"]
            for parameter in contract["paths"][endpoint]["get"].get("parameters", [])
            if parameter.get("in") == "query"
        }
        missing = expected - set(captured_params)
        if missing:
            missing_by_endpoint[endpoint] = sorted(missing)

    assert missing_by_endpoint == {}
