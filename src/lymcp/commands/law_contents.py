import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query law contents.")


@app.command("list")
def list_law_contents(
    law_number: str | None = None,
    version_id: str | None = None,
    order: int | None = None,
    article_number: str | None = None,
    current_version_status: str | None = None,
    version_tracking: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List law article contents."""
    _run(
        api.ListLawContentsRequest(
            law_number=law_number,
            version_id=version_id,
            order=order,
            article_number=article_number,
            current_version_status=current_version_status,
            version_tracking=version_tracking,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list law contents",
    )


@app.command("get")
def get_law_content(law_content_id: str) -> None:
    """Get law article content details."""
    _run(api.GetLawContentRequest(law_content_id=law_content_id), "Failed to get law content")
