import json
from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from lymcp import api
from lymcp import cli
from tests.fixtures import load_json_fixture

runner = CliRunner()


class StubRequest:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response

    async def do(self) -> dict[str, Any]:
        return self.response


def recording_request(calls: list[dict[str, Any]]) -> type[StubRequest]:
    class RecordingRequest(StubRequest):
        def __init__(self, **kwargs: Any) -> None:
            calls.append(kwargs)
            super().__init__({"ok": True})

    return RecordingRequest


def test_root_help_lists_agent_friendly_command_groups() -> None:
    result = runner.invoke(cli.app, ["--help"])

    assert result.exit_code == 0
    assert "bills" in result.stdout
    assert "laws" in result.stdout
    assert "meets" in result.stdout
    assert "legislators" in result.stdout
    assert "votes" in result.stdout


def test_command_inventory_matches_mcp_tool_coverage() -> None:
    assert len(cli.COMMAND_INVENTORY) == 42
    assert ("stat",) in cli.COMMAND_INVENTORY
    assert ("bills", "list") in cli.COMMAND_INVENTORY
    assert ("law-versions", "contents") in cli.COMMAND_INVENTORY
    assert ("meets", "ivods") in cli.COMMAND_INVENTORY
    assert ("votes", "list") in cli.COMMAND_INVENTORY
    assert ("votes", "get") in cli.COMMAND_INVENTORY
    assert ("votes", "meets") in cli.COMMAND_INVENTORY


def test_stat_outputs_fixture_json(monkeypatch: Any) -> None:
    expected_response = load_json_fixture("stat.json")

    monkeypatch.setattr(cli.api, "GetStatRequest", lambda: StubRequest(expected_response))

    result = runner.invoke(cli.app, ["stat"])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected_response


def test_list_bills_passes_filters_and_fields(monkeypatch: Any) -> None:
    expected_response = load_json_fixture("bills_list.json")
    calls: list[dict[str, Any]] = []

    class StubListBillRequest(StubRequest):
        def __init__(self, **kwargs: Any) -> None:
            calls.append(kwargs)
            super().__init__(expected_response)

    monkeypatch.setattr(cli.api, "ListBillRequest", StubListBillRequest)

    result = runner.invoke(
        cli.app,
        [
            "bills",
            "list",
            "--term",
            "11",
            "--bill-type",
            "法律案",
            "--proposal-unit-or-member",
            "王世堅",
            "--fields",
            "議案編號,案由",
            "--limit",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected_response
    assert calls == [
        {
            "term": 11,
            "session": None,
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
            "page": 1,
            "limit": 1,
            "output_fields": ["議案編號", "案由"],
            "proposal_unit_or_member": "王世堅",
        }
    ]


def test_nested_bill_and_gazette_filters_reach_requests(monkeypatch: Any) -> None:
    cases = [
        (
            [
                "bills",
                "meets",
                "202110213410000",
                "--meeting-code",
                "院會-11-2-6",
                "--member",
                "陳秀寳",
                "--committee-code",
                "23",
                "--meet-id",
                "2024102368",
                "--related-bill-no",
                "202110071090000",
                "--law-number",
                "01177",
                "--fields",
                "會議代碼",
            ],
            "GetBillMeetsRequest",
            {
                "meeting_code": "院會-11-2-6",
                "member": "陳秀寳",
                "committee_code": 23,
                "meet_id": "2024102368",
                "related_bill_no": "202110071090000",
                "law_number": "01177",
                "output_fields": ["會議代碼"],
            },
        ),
        (
            ["laws", "bills", "09200015", "--proposal-unit-or-member", "民進黨團"],
            "GetLawBillsRequest",
            {"proposal_unit_or_member": "民進黨團"},
        ),
        (
            ["legislators", "propose-bills", "11", "韓國瑜", "--proposal-unit-or-member", "民進黨團"],
            "GetLegislatorProposeBillsRequest",
            {"proposal_unit_or_member": "民進黨團"},
        ),
        (
            ["legislators", "cosign-bills", "11", "韓國瑜", "--proposal-unit-or-member", "民進黨團"],
            "GetLegislatorCosignBillsRequest",
            {"proposal_unit_or_member": "民進黨團"},
        ),
        (
            ["meets", "bills", "院會-11-2-3", "--proposal-unit-or-member", "民進黨團"],
            "GetMeetBillsRequest",
            {"proposal_unit_or_member": "民進黨團"},
        ),
        (
            [
                "gazettes",
                "agendas",
                "1137701",
                "--gazette-number",
                "1137702",
                "--issue",
                "77",
                "--booklet",
                "1",
            ],
            "GetGazetteAgendasRequest",
            {"gazette_number": "1137702", "issue": 77, "booklet": 1},
        ),
        (
            ["gazette-agendas", "list", "--issue", "77", "--booklet", "1"],
            "ListGazetteAgendasRequest",
            {"issue": 77, "booklet": 1},
        ),
    ]

    for command, request_class_name, expected in cases:
        calls: list[dict[str, Any]] = []

        monkeypatch.setattr(cli.api, request_class_name, recording_request(calls))
        result = runner.invoke(cli.app, command)

        assert result.exit_code == 0, result.output
        assert len(calls) == 1
        for key, value in expected.items():
            assert calls[0][key] == value


def test_contract_aligned_cli_parameters(monkeypatch: Any) -> None:
    cases = [
        (
            ["committees", "list", "--committee-type", "1", "--comt-cd", "15"],
            "ListCommitteesRequest",
            {"committee_type": 1, "comt_cd": 15},
        ),
        (
            ["committees", "meets", "16", "--committee-code", "23"],
            "GetCommitteeMeetsRequest",
            {"committee_code": 23},
        ),
        (
            ["legislators", "interpellations", "11", "韓國瑜", "--term-query", "10"],
            "GetLegislatorInterpellationsRequest",
            {"term": 11, "term_query": 10},
        ),
    ]

    for command, request_class_name, expected in cases:
        calls: list[dict[str, Any]] = []
        monkeypatch.setattr(cli.api, request_class_name, recording_request(calls))

        result = runner.invoke(cli.app, command)

        assert result.exit_code == 0, result.output
        assert len(calls) == 1
        for key, value in expected.items():
            assert calls[0][key] == value

    related_help = runner.invoke(cli.app, ["bills", "related", "--help"])
    assert related_help.exit_code == 0
    assert "--page" not in related_help.stdout
    assert "--limit" not in related_help.stdout


def test_vote_commands_pass_filters_and_identifiers(monkeypatch: Any) -> None:
    cases = [
        (
            ["votes", "list", "--term", "11", "--voting-member", "黃國昌", "--fields", "表決代碼"],
            "ListVotesRequest",
            {"term": 11, "voting_member": "黃國昌", "output_fields": ["表決代碼"]},
        ),
        (
            ["votes", "get", "1141921_00002_591"],
            "GetVoteRequest",
            {"vote_id": "1141921_00002_591"},
        ),
        (
            ["votes", "meets", "1141921_00002_591", "--term", "11", "--session", "2"],
            "GetVoteMeetsRequest",
            {"vote_id": "1141921_00002_591", "term": 11, "session": 2},
        ),
    ]

    for command, request_class_name, expected in cases:
        calls: list[dict[str, Any]] = []

        monkeypatch.setattr(cli.api, request_class_name, recording_request(calls))
        result = runner.invoke(cli.app, command)

        assert result.exit_code == 0, result.output
        assert len(calls) == 1
        for key, value in expected.items():
            assert calls[0][key] == value


def test_get_bill_outputs_compact_json(monkeypatch: Any) -> None:
    expected_response = load_json_fixture("bill_detail.json")

    def stub_get_bill_request(**kwargs: Any) -> StubRequest:
        return StubRequest({"kwargs": kwargs, **expected_response})

    monkeypatch.setattr(cli.api, "GetBillRequest", stub_get_bill_request)

    result = runner.invoke(cli.app, ["--compact", "bills", "get", "202110213410000"])

    assert result.exit_code == 0
    assert "\n" not in result.stdout.strip()
    assert json.loads(result.stdout)["kwargs"] == {"bill_no": "202110213410000"}


def test_output_writes_successful_json_to_file(monkeypatch: Any, tmp_path: Path) -> None:
    output_path = tmp_path / "stat.json"
    expected_response = load_json_fixture("stat.json")

    monkeypatch.setattr(cli.api, "GetStatRequest", lambda: StubRequest(expected_response))

    result = runner.invoke(cli.app, ["--output", str(output_path), "stat"])

    assert result.exit_code == 0
    assert result.stdout == ""
    assert json.loads(output_path.read_text(encoding="utf-8")) == expected_response


def test_api_error_outputs_json_to_stderr(monkeypatch: Any) -> None:
    class StubErrorRequest:
        async def do(self) -> dict[str, Any]:
            raise api.LymcpApiError(
                "http_status",
                "Upstream API returned HTTP 404",
                url=f"{api.BASE_URL}/bills/invalid",
                status_code=404,
                response_excerpt="not found",
            )

    monkeypatch.setattr(cli.api, "GetBillRequest", lambda **kwargs: StubErrorRequest())

    result = runner.invoke(cli.app, ["bills", "get", "invalid"])

    assert result.exit_code == 1
    assert result.stdout == ""
    payload = json.loads(result.stderr)
    assert payload["ok"] is False
    assert payload["error"]["type"] == "http_status"
    assert payload["error"]["status_code"] == 404


def test_required_argument_failure_exits_before_api_call() -> None:
    result = runner.invoke(cli.app, ["bills", "get"])

    assert result.exit_code != 0
    assert "Missing argument" in result.stderr
