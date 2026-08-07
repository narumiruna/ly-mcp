import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query interpellations.")


@app.command("list")
def list_interpellations(
    interpellation_member: str | None = None,
    term: int | None = None,
    session: int | None = None,
    meeting_code: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List interpellations."""
    _run(
        api.ListInterpellationsRequest(
            interpellation_member=interpellation_member,
            term=term,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list interpellations",
    )


@app.command("get")
def get_interpellation(interpellation_id: str) -> None:
    """Get interpellation details."""
    _run(api.GetInterpellationRequest(interpellation_id=interpellation_id), "Failed to get interpellation")
