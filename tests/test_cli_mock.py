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


def test_root_help_lists_agent_friendly_command_groups() -> None:
    result = runner.invoke(cli.app, ["--help"])

    assert result.exit_code == 0
    assert "bills" in result.stdout
    assert "laws" in result.stdout
    assert "meets" in result.stdout
    assert "legislators" in result.stdout


def test_command_inventory_matches_mcp_tool_coverage() -> None:
    assert len(cli.COMMAND_INVENTORY) == 39
    assert ("stat",) in cli.COMMAND_INVENTORY
    assert ("bills", "list") in cli.COMMAND_INVENTORY
    assert ("law-versions", "contents") in cli.COMMAND_INVENTORY
    assert ("meets", "ivods") in cli.COMMAND_INVENTORY


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
