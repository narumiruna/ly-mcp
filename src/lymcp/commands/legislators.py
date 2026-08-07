import typer

from lymcp import api
from lymcp.commands.bills import _bill_kwargs
from lymcp.commands.support import _fields
from lymcp.commands.support import _run

app = typer.Typer(no_args_is_help=True, help="Query legislators.")


@app.command("list")
def list_legislators(
    term: int | None = None,
    party: str | None = None,
    district_name: str | None = None,
    legislator_id: int | None = None,
    legislator_name: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List legislators."""
    _run(
        api.ListLegislatorsRequest(
            term=term,
            party=party,
            district_name=district_name,
            legislator_id=legislator_id,
            legislator_name=legislator_name,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list legislators",
    )


@app.command("get")
def get_legislator(term: int, name: str) -> None:
    """Get legislator details."""
    _run(api.GetLegislatorRequest(term=term, name=name), "Failed to get legislator")


@app.command("propose-bills")
def get_legislator_propose_bills(
    term: int,
    name: str,
    bill_term: int | None = None,
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
    """Get bills proposed by a legislator."""
    kwargs = _bill_kwargs(
        bill_term,
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
    kwargs["bill_term"] = kwargs.pop("term")
    kwargs["term"] = term
    kwargs["name"] = name
    _run(api.GetLegislatorProposeBillsRequest(**kwargs), "Failed to get legislator proposed bills")


@app.command("cosign-bills")
def get_legislator_cosign_bills(
    term: int,
    name: str,
    bill_term: int | None = None,
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
    """Get bills co-signed by a legislator."""
    kwargs = _bill_kwargs(
        bill_term,
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
    kwargs["bill_term"] = kwargs.pop("term")
    kwargs["term"] = term
    kwargs["name"] = name
    _run(api.GetLegislatorCosignBillsRequest(**kwargs), "Failed to get legislator co-signed bills")


@app.command("meets")
def get_legislator_meets(
    term: int,
    name: str,
    meet_term: int | None = None,
    meeting_code: str | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    member: str | None = None,
    date: str | None = None,
    committee_code: int | None = None,
    meet_id: str | None = None,
    bill_no_nested: str | None = None,
    law_number_nested: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get meetings attended by a legislator."""
    _run(
        api.GetLegislatorMeetsRequest(
            term=term,
            name=name,
            meet_term=meet_term,
            meeting_code=meeting_code,
            session=session,
            meeting_type=meeting_type,
            member=member,
            date=date,
            committee_code=committee_code,
            meet_id=meet_id,
            bill_no_nested=bill_no_nested,
            law_number_nested=law_number_nested,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get legislator meetings",
    )


@app.command("interpellations")
def get_legislator_interpellations(
    term: int,
    name: str,
    interpellation_member: str | None = None,
    term_query: int | None = None,
    session: int | None = None,
    meeting_code: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """Get interpellations by a legislator."""
    _run(
        api.GetLegislatorInterpellationsRequest(
            term=term,
            name=name,
            interpellation_member=interpellation_member,
            term_query=term_query,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get legislator interpellations",
    )
