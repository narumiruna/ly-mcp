from typing import Any

import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query IVOD recordings.")


def _ivod_kwargs(
    term: int | None,
    session: int | None,
    meeting_code: str | None,
    member_name: str | None,
    committee_code: int | None,
    meeting_code_data: str | None,
    date: str | None,
    video_type: str | None,
    page: int,
    limit: int,
    fields: str | None,
) -> dict[str, Any]:
    return {
        "term": term,
        "session": session,
        "meeting_code": meeting_code,
        "member_name": member_name,
        "committee_code": committee_code,
        "meeting_code_data": meeting_code_data,
        "date": date,
        "video_type": video_type,
        "page": page,
        "limit": limit,
        "output_fields": _fields(fields),
    }


@app.command("list")
def list_ivods(
    term: int | None = None,
    session: int | None = None,
    meeting_code: str | None = None,
    member_name: str | None = None,
    committee_code: int | None = None,
    meeting_code_data: str | None = None,
    date: str | None = None,
    video_type: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List IVOD recordings."""
    _run(
        api.ListIvodsRequest(
            **_ivod_kwargs(
                term,
                session,
                meeting_code,
                member_name,
                committee_code,
                meeting_code_data,
                date,
                video_type,
                page,
                limit,
                fields,
            )
        ),
        "Failed to list IVODs",
    )


@app.command("get")
def get_ivod(ivod_id: str) -> None:
    """Get IVOD recording details."""
    _run(api.GetIvodRequest(ivod_id=ivod_id), "Failed to get IVOD")
