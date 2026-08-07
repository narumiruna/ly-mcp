import typer

from lymcp import api
from lymcp.commands.bills import _bill_kwargs
from lymcp.commands.ivods import _ivod_kwargs
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query meetings.")


@app.command("list")
def list_meets(
    term: int | None = None,
    meeting_code: str | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    meeting_attendee: str | None = None,
    date: str | None = None,
    committee_code: int | None = None,
    meeting_id: str | None = None,
    meeting_bills_bill_no: str | None = None,
    meeting_bills_law_no: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List meetings."""
    _run(
        api.ListMeetsRequest(
            term=term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            meeting_attendee=meeting_attendee,
            date=date,
            committee_code=committee_code,
            meeting_id=meeting_id,
            meeting_bills_bill_no=meeting_bills_bill_no,
            meeting_bills_law_no=meeting_bills_law_no,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list meetings",
    )


@app.command("get")
def get_meet(meet_id: str) -> None:
    """Get meeting details."""
    _run(api.GetMeetRequest(meet_id=meet_id), "Failed to get meeting")


@app.command("bills")
def get_meet_bills(
    meet_id: str,
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
    """Get bills discussed in a meeting."""
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
    kwargs["meet_id"] = meet_id
    _run(api.GetMeetBillsRequest(**kwargs), "Failed to get meeting bills")


@app.command("interpellations")
def get_meet_interpellations(
    meet_id: str,
    interpellation_member: str | None = None,
    term: int | None = None,
    session: int | None = None,
    meeting_code: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get interpellations in a meeting."""
    _run(
        api.GetMeetInterpellationsRequest(
            meet_id=meet_id,
            interpellation_member=interpellation_member,
            term=term,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get meeting interpellations",
    )


@app.command("ivods")
def get_meet_ivods(
    meet_id: str,
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
    """Get IVOD recordings for a meeting."""
    kwargs = _ivod_kwargs(
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
    kwargs["meet_id"] = meet_id
    _run(api.GetMeetIvodsRequest(**kwargs), "Failed to get meeting IVODs")
