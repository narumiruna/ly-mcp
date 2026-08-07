import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query gazette agendas.")


@app.command("list")
def list_gazette_agendas(
    gazette_id: str | None = None,
    volume: int | None = None,
    issue: int | None = None,
    booklet: int | None = None,
    term: int | None = None,
    meeting_date: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List gazette agendas."""
    _run(
        api.ListGazetteAgendasRequest(
            gazette_id=gazette_id,
            volume=volume,
            issue=issue,
            booklet=booklet,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list gazette agendas",
    )


@app.command("get")
def get_gazette_agenda(gazette_agenda_id: str) -> None:
    """Get gazette agenda details."""
    _run(api.GetGazetteAgendaRequest(gazette_agenda_id=gazette_agenda_id), "Failed to get gazette agenda")
