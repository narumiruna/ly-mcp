import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query committees.")


@app.command("list")
def list_committees(
    committee_type: str | None = None,
    comt_cd: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List committees."""
    _run(
        api.ListCommitteesRequest(
            committee_type=committee_type,
            comt_cd=comt_cd,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list committees",
    )


@app.command("get")
def get_committee(comt_cd: str) -> None:
    """Get committee details."""
    _run(api.GetCommitteeRequest(comt_cd=comt_cd), "Failed to get committee")


@app.command("meets")
def get_committee_meets(
    comt_cd: str,
    term: int | None = None,
    meeting_code: str | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    member: str | None = None,
    date: str | None = None,
    committee_code: str | None = None,
    meet_id: str | None = None,
    bill_no: str | None = None,
    law_number: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get committee meeting records."""
    _run(
        api.GetCommitteeMeetsRequest(
            comt_cd=comt_cd,
            term=term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            member=member,
            date=date,
            committee_code=committee_code,
            meet_id=meet_id,
            bill_no=bill_no,
            law_number=law_number,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get committee meets",
    )
