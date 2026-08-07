from typing import Any

import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query bills.")


def _bill_kwargs(
    term: int | None,
    session: int | None,
    bill_flow_status: str | None,
    bill_type: str | None,
    proposer: str | None,
    cosigner: str | None,
    law_number: str | None,
    bill_status: str | None,
    meeting_code: str | None,
    proposal_source: str | None,
    bill_number: str | None,
    proposal_number: str | None,
    reference_number: str | None,
    article_number: str | None,
    proposal_date: str | None,
    proposal_unit_or_member: str | None,
    page: int,
    limit: int,
    fields: str | None,
) -> dict[str, Any]:
    return {
        "term": term,
        "session": session,
        "bill_flow_status": bill_flow_status,
        "bill_type": bill_type,
        "proposer": proposer,
        "co_proposer": cosigner,
        "law_number": law_number,
        "bill_status": bill_status,
        "meeting_code": meeting_code,
        "proposal_source": proposal_source,
        "bill_number": bill_number,
        "proposal_number": proposal_number,
        "reference_number": reference_number,
        "article_number": article_number,
        "proposal_date": proposal_date,
        "proposal_unit_or_member": proposal_unit_or_member,
        "page": page,
        "limit": limit,
        "output_fields": _fields(fields),
    }


@app.command("list")
def list_bills(
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
    """List bills."""
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
    _run(api.ListBillRequest(**kwargs), "Failed to list bills")


@app.command("get")
def get_bill(bill_no: str) -> None:
    """Get bill details."""
    _run(api.GetBillRequest(bill_no=bill_no), "Failed to get bill")


@app.command("related")
def get_bill_related_bills(bill_no: str, page: int = 1, limit: int = 20) -> None:
    """Get related bills."""
    _run(api.GetBillRelatedBillsRequest(bill_no=bill_no, page=page, limit=limit), "Failed to get related bills")


@app.command("meets")
def get_bill_meets(
    bill_no: str,
    term: int | None = None,
    meeting_code: str | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    member: str | None = None,
    date: str | None = None,
    committee_code: int | None = None,
    meet_id: str | None = None,
    related_bill_no: str | None = None,
    law_number: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get bill deliberation records."""
    _run(
        api.GetBillMeetsRequest(
            bill_no=bill_no,
            term=term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            member=member,
            date=date,
            committee_code=committee_code,
            meet_id=meet_id,
            related_bill_no=related_bill_no,
            law_number=law_number,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get bill meets",
    )


@app.command("doc-html")
def get_bill_doc_html(bill_no: str) -> None:
    """Get bill document HTML."""
    _run(api.GetBillDocHtmlRequest(bill_no=bill_no), "Failed to get bill document HTML")
