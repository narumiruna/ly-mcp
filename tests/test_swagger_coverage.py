import re
from pathlib import Path

import pytest

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


def swagger_paths() -> set[str]:
    swagger = Path(__file__).parents[1] / "swagger.yaml"
    return set(re.findall(r"^  (/[^:]+):$", swagger.read_text(encoding="utf-8"), flags=re.MULTILINE))


@pytest.mark.asyncio
async def test_swagger_endpoints_match_mcp_tools_and_cli_commands() -> None:
    tools = await server.mcp.list_tools()

    assert set(ENDPOINT_COVERAGE) == swagger_paths()
    assert {tool for tool, _ in ENDPOINT_COVERAGE.values()} == {tool.name for tool in tools}
    assert {command for _, command in ENDPOINT_COVERAGE.values()} == set(cli.COMMAND_INVENTORY)
