import typer

from lymcp import api
from lymcp.commands.bills import _bill_kwargs
from lymcp.commands.law_versions import _version_kwargs
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query laws.")


@app.command("list")
def list_laws(
    law_number: str | None = None,
    category: str | None = None,
    parent_law_number: str | None = None,
    law_status: str | None = None,
    authority: str | None = None,
    latest_version_date: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List laws."""
    _run(
        api.ListLawsRequest(
            law_number=law_number,
            category=category,
            parent_law_number=parent_law_number,
            law_status=law_status,
            authority=authority,
            latest_version_date=latest_version_date,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list laws",
    )


@app.command("get")
def get_law(law_id: str) -> None:
    """Get law details."""
    _run(api.GetLawRequest(law_id=law_id), "Failed to get law")


@app.command("progress")
def get_law_progress(law_id: str) -> None:
    """Get undecided progress for a law."""
    _run(api.GetLawProgressRequest(law_id=law_id), "Failed to get law progress")


@app.command("bills")
def get_law_bills(
    law_id: str,
    term: int | None = None,
    session: int | None = None,
    bill_flow_status: str | None = None,
    bill_type: str | None = None,
    proposer: str | None = None,
    cosigner: str | None = None,
    law_number: str | None = None,
    bill_status: str | None = None,
    meeting_code: str | None = None,
    proposal_source: str | None = None,
    bill_number: str | None = None,
    proposal_number: str | None = None,
    reference_number: str | None = None,
    article_number: str | None = None,
    proposal_date: str | None = None,
    proposal_unit_or_member: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get bills related to a law."""
    kwargs = _bill_kwargs(
        term,
        session,
        bill_flow_status,
        bill_type,
        proposer,
        cosigner,
        law_number,
        bill_status,
        meeting_code,
        proposal_source,
        bill_number,
        proposal_number,
        reference_number,
        article_number,
        proposal_date,
        proposal_unit_or_member,
        page,
        limit,
        fields,
    )
    kwargs["law_id"] = law_id
    _run(api.GetLawBillsRequest(**kwargs), "Failed to get law bills")


@app.command("versions")
def get_law_versions(
    law_id: str,
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
    """Get historical versions for a law."""
    kwargs = _version_kwargs(
        law_number, version_number, date, action, main_proposer, progress, current_version, page, limit, fields
    )
    kwargs["law_id"] = law_id
    _run(api.GetLawVersionsRequest(**kwargs), "Failed to get law versions")
