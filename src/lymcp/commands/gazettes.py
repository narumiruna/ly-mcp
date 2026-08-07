import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query gazettes.")


@app.command("list")
def list_gazettes(
    gazette_id: str | None = None,
    volume: int | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List gazettes."""
    _run(
        api.ListGazettesRequest(
            gazette_id=gazette_id,
            volume=volume,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list gazettes",
    )


@app.command("get")
def get_gazette(gazette_id: str) -> None:
    """Get gazette details."""
    _run(api.GetGazetteRequest(gazette_id=gazette_id), "Failed to get gazette")


@app.command("agendas")
def get_gazette_agendas(
    gazette_id: str,
    gazette_number: str | None = None,
    volume: int | None = None,
    issue: int | None = None,
    booklet: int | None = None,
    term: int | None = None,
    meeting_date: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get agendas from a gazette."""
    _run(
        api.GetGazetteAgendasRequest(
            gazette_id=gazette_id,
            gazette_number=gazette_number,
            volume=volume,
            issue=issue,
            booklet=booklet,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get gazette agendas",
    )
