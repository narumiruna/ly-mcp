from typing import Any

import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query law versions.")


def _version_kwargs(
    law_number: str | None,
    version_number: str | None,
    date: str | None,
    action: str | None,
    main_proposer: str | None,
    progress: str | None,
    current_version: str | None,
    page: int,
    limit: int,
    fields: str | None,
) -> dict[str, Any]:
    return {
        "law_number": law_number,
        "version_number": version_number,
        "date": date,
        "action": action,
        "main_proposer": main_proposer,
        "progress": progress,
        "current_version": current_version,
        "page": page,
        "limit": limit,
        "output_fields": _fields(fields),
    }


@app.command("list")
def list_law_versions(
    law_number: str | None = None,
    version_number: str | None = None,
    date: str | None = None,
    action: str | None = None,
    main_proposer: str | None = None,
    progress: str | None = None,
    current_version: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List law versions."""
    _run(
        api.ListLawVersionsRequest(
            **_version_kwargs(
                law_number, version_number, date, action, main_proposer, progress, current_version, page, limit, fields
            )
        ),
        "Failed to list law versions",
    )


@app.command("get")
def get_law_version(law_version_id: str) -> None:
    """Get law version details."""
    _run(api.GetLawVersionRequest(law_version_id=law_version_id), "Failed to get law version")


@app.command("contents")
def get_law_version_contents(
    law_version_id: str,
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
    """Get law article contents in a version."""
    _run(
        api.GetLawVersionContentsRequest(
            law_version_id=law_version_id,
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
        "Failed to get law version contents",
    )
