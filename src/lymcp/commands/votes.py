import typer

from lymcp import api
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query votes.")


@app.command("list")
def list_votes(
    term: int | None = None,
    meeting_code: str | None = None,
    vote_type: str | None = None,
    vote_time: str | None = None,
    voting_member: str | None = None,
    agreeing_member: str | None = None,
    opposing_member: str | None = None,
    abstaining_member: str | None = None,
    gazette_document_id: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List vote records."""
    _run(
        api.ListVotesRequest(
            term=term,
            meeting_code=meeting_code,
            vote_type=vote_type,
            vote_time=vote_time,
            voting_member=voting_member,
            agreeing_member=agreeing_member,
            opposing_member=opposing_member,
            abstaining_member=abstaining_member,
            gazette_document_id=gazette_document_id,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list votes",
    )


@app.command("get")
def get_vote(vote_id: str) -> None:
    """Get a vote record."""
    _run(api.GetVoteRequest(vote_id=vote_id), "Failed to get vote")


@app.command("meets")
def get_vote_meets(
    vote_id: str,
    term: int | None = None,
    meeting_code: str | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    member: str | None = None,
    date: str | None = None,
    committee_code: int | None = None,
    meet_id: str | None = None,
    bill_no: str | None = None,
    law_number: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get meetings related to a vote."""
    _run(
        api.GetVoteMeetsRequest(
            vote_id=vote_id,
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
        "Failed to get vote meetings",
    )
