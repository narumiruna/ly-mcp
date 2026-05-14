import asyncio
import json
from pathlib import Path
from typing import Annotated
from typing import Any

import typer

from lymcp import api

app = typer.Typer(no_args_is_help=True, help="Query Taiwan Legislative Yuan API v2 from the terminal.")
bills_app = typer.Typer(no_args_is_help=True, help="Query bills.")
committees_app = typer.Typer(no_args_is_help=True, help="Query committees.")
gazettes_app = typer.Typer(no_args_is_help=True, help="Query gazettes.")
gazette_agendas_app = typer.Typer(no_args_is_help=True, help="Query gazette agendas.")
interpellations_app = typer.Typer(no_args_is_help=True, help="Query interpellations.")
ivods_app = typer.Typer(no_args_is_help=True, help="Query IVOD recordings.")
laws_app = typer.Typer(no_args_is_help=True, help="Query laws.")
law_versions_app = typer.Typer(no_args_is_help=True, help="Query law versions.")
law_contents_app = typer.Typer(no_args_is_help=True, help="Query law contents.")
legislators_app = typer.Typer(no_args_is_help=True, help="Query legislators.")
meets_app = typer.Typer(no_args_is_help=True, help="Query meetings.")

app.add_typer(bills_app, name="bills")
app.add_typer(committees_app, name="committees")
app.add_typer(gazettes_app, name="gazettes")
app.add_typer(gazette_agendas_app, name="gazette-agendas")
app.add_typer(interpellations_app, name="interpellations")
app.add_typer(ivods_app, name="ivods")
app.add_typer(laws_app, name="laws")
app.add_typer(law_versions_app, name="law-versions")
app.add_typer(law_contents_app, name="law-contents")
app.add_typer(legislators_app, name="legislators")
app.add_typer(meets_app, name="meets")

COMMAND_INVENTORY: tuple[tuple[str, ...], ...] = (
    ("stat",),
    ("bills", "list"),
    ("bills", "get"),
    ("bills", "related"),
    ("bills", "meets"),
    ("bills", "doc-html"),
    ("committees", "list"),
    ("committees", "get"),
    ("committees", "meets"),
    ("gazettes", "list"),
    ("gazettes", "get"),
    ("gazettes", "agendas"),
    ("gazette-agendas", "list"),
    ("gazette-agendas", "get"),
    ("interpellations", "list"),
    ("interpellations", "get"),
    ("ivods", "list"),
    ("ivods", "get"),
    ("laws", "list"),
    ("laws", "get"),
    ("laws", "progress"),
    ("laws", "bills"),
    ("laws", "versions"),
    ("law-versions", "list"),
    ("law-versions", "get"),
    ("law-versions", "contents"),
    ("law-contents", "list"),
    ("law-contents", "get"),
    ("legislators", "list"),
    ("legislators", "get"),
    ("legislators", "propose-bills"),
    ("legislators", "cosign-bills"),
    ("legislators", "meets"),
    ("legislators", "interpellations"),
    ("meets", "list"),
    ("meets", "get"),
    ("meets", "bills"),
    ("meets", "interpellations"),
    ("meets", "ivods"),
)

_compact_output = False
_output_path: Path | None = None


def _fields(value: str | None) -> list[str]:
    if not value:
        return []
    return [field.strip() for field in value.split(",") if field.strip()]


def _json_text(payload: dict[str, Any]) -> str:
    if _compact_output:
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _emit(payload: dict[str, Any], *, err: bool = False) -> None:
    text = _json_text(payload)
    if _output_path is not None and not err:
        _output_path.write_text(f"{text}\n", encoding="utf-8")
        return
    typer.echo(text, err=err)


def _error_payload(action: str, error: Exception) -> dict[str, Any]:
    if isinstance(error, api.LymcpApiError):
        return {"ok": False, "error": error.to_dict()}
    return {
        "ok": False,
        "error": {
            "type": "unexpected_error",
            "message": f"{action}: {error}",
        },
    }


def _run(request: Any, action: str) -> None:
    try:
        _emit(asyncio.run(request.do()))
    except Exception as e:
        _emit(_error_payload(action, e), err=True)
        raise typer.Exit(1) from e


@app.callback()
def main(
    compact: Annotated[bool, typer.Option("--compact", help="Print compact single-line JSON.")] = False,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Write successful JSON output to a file."),
    ] = None,
) -> None:
    """Query Taiwan Legislative Yuan API v2."""
    global _compact_output, _output_path
    _compact_output = compact
    _output_path = output


@app.command("stat")
def stat() -> None:
    """Get API statistics."""
    _run(api.GetStatRequest(), "Failed to get statistics")


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
        "page": page,
        "limit": limit,
        "output_fields": _fields(fields),
    }


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


def _ivod_kwargs(
    term: int | None,
    session: int | None,
    meeting_code: str | None,
    member_name: str | None,
    committee_code: int | None,
    meeting_code_data: str | None,
    date: str | None,
    video_type: str | None,
    page: int,
    limit: int,
    fields: str | None,
) -> dict[str, Any]:
    return {
        "term": term,
        "session": session,
        "meeting_code": meeting_code,
        "member_name": member_name,
        "committee_code": committee_code,
        "meeting_code_data": meeting_code_data,
        "date": date,
        "video_type": video_type,
        "page": page,
        "limit": limit,
        "output_fields": _fields(fields),
    }


@bills_app.command("list")
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
        page,
        limit,
        fields,
    )
    kwargs["proposal_unit_or_member"] = proposal_unit_or_member
    _run(api.ListBillRequest(**kwargs), "Failed to list bills")


@bills_app.command("get")
def get_bill(bill_no: str) -> None:
    """Get bill details."""
    _run(api.GetBillRequest(bill_no=bill_no), "Failed to get bill")


@bills_app.command("related")
def get_bill_related_bills(bill_no: str, page: int = 1, limit: int = 20) -> None:
    """Get related bills."""
    _run(api.GetBillRelatedBillsRequest(bill_no=bill_no, page=page, limit=limit), "Failed to get related bills")


@bills_app.command("meets")
def get_bill_meets(
    bill_no: str,
    term: int | None = None,
    session: int | None = None,
    meeting_type: str | None = None,
    date: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> None:
    """Get bill deliberation records."""
    _run(
        api.GetBillMeetsRequest(
            bill_no=bill_no,
            term=term,
            session=session,
            meeting_type=meeting_type,
            date=date,
            page=page,
            limit=limit,
        ),
        "Failed to get bill meets",
    )


@bills_app.command("doc-html")
def get_bill_doc_html(bill_no: str) -> None:
    """Get bill document HTML."""
    _run(api.GetBillDocHtmlRequest(bill_no=bill_no), "Failed to get bill document HTML")


@committees_app.command("list")
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


@committees_app.command("get")
def get_committee(comt_cd: str) -> None:
    """Get committee details."""
    _run(api.GetCommitteeRequest(comt_cd=comt_cd), "Failed to get committee")


@committees_app.command("meets")
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


@gazettes_app.command("list")
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


@gazettes_app.command("get")
def get_gazette(gazette_id: str) -> None:
    """Get gazette details."""
    _run(api.GetGazetteRequest(gazette_id=gazette_id), "Failed to get gazette")


@gazettes_app.command("agendas")
def get_gazette_agendas(
    gazette_id: str,
    volume: int | None = None,
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
            volume=volume,
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to get gazette agendas",
    )


@gazette_agendas_app.command("list")
def list_gazette_agendas(
    gazette_id: str | None = None,
    volume: int | None = None,
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
            term=term,
            meeting_date=meeting_date,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list gazette agendas",
    )


@gazette_agendas_app.command("get")
def get_gazette_agenda(gazette_agenda_id: str) -> None:
    """Get gazette agenda details."""
    _run(api.GetGazetteAgendaRequest(gazette_agenda_id=gazette_agenda_id), "Failed to get gazette agenda")


@interpellations_app.command("list")
def list_interpellations(
    interpellation_member: str | None = None,
    term: int | None = None,
    session: int | None = None,
    meeting_code: str | None = None,
    page: int = 1,
    limit: int = 20,
    fields: str | None = typer.Option(None, "--fields", help="Comma-separated upstream output fields."),
) -> None:
    """List interpellations."""
    _run(
        api.ListInterpellationsRequest(
            interpellation_member=interpellation_member,
            term=term,
            session=session,
            meeting_code=meeting_code,
            page=page,
            limit=limit,
            output_fields=_fields(fields),
        ),
        "Failed to list interpellations",
    )


@interpellations_app.command("get")
def get_interpellation(interpellation_id: str) -> None:
    """Get interpellation details."""
    _run(api.GetInterpellationRequest(interpellation_id=interpellation_id), "Failed to get interpellation")


@ivods_app.command("list")
def list_ivods(
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
    """List IVOD recordings."""
    _run(
        api.ListIvodsRequest(
            **_ivod_kwargs(
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
        ),
        "Failed to list IVODs",
    )


@ivods_app.command("get")
def get_ivod(ivod_id: str) -> None:
    """Get IVOD recording details."""
    _run(api.GetIvodRequest(ivod_id=ivod_id), "Failed to get IVOD")


@laws_app.command("list")
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


@laws_app.command("get")
def get_law(law_id: str) -> None:
    """Get law details."""
    _run(api.GetLawRequest(law_id=law_id), "Failed to get law")


@laws_app.command("progress")
def get_law_progress(law_id: str) -> None:
    """Get undecided progress for a law."""
    _run(api.GetLawProgressRequest(law_id=law_id), "Failed to get law progress")


@laws_app.command("bills")
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
        page,
        limit,
        fields,
    )
    kwargs["law_id"] = law_id
    _run(api.GetLawBillsRequest(**kwargs), "Failed to get law bills")


@laws_app.command("versions")
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


@law_versions_app.command("list")
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


@law_versions_app.command("get")
def get_law_version(law_version_id: str) -> None:
    """Get law version details."""
    _run(api.GetLawVersionRequest(law_version_id=law_version_id), "Failed to get law version")


@law_versions_app.command("contents")
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


@law_contents_app.command("list")
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


@law_contents_app.command("get")
def get_law_content(law_content_id: str) -> None:
    """Get law article content details."""
    _run(api.GetLawContentRequest(law_content_id=law_content_id), "Failed to get law content")


@legislators_app.command("list")
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


@legislators_app.command("get")
def get_legislator(term: int, name: str) -> None:
    """Get legislator details."""
    _run(api.GetLegislatorRequest(term=term, name=name), "Failed to get legislator")


@legislators_app.command("propose-bills")
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
        page,
        limit,
        fields,
    )
    kwargs["bill_term"] = kwargs.pop("term")
    kwargs["term"] = term
    kwargs["name"] = name
    _run(api.GetLegislatorProposeBillsRequest(**kwargs), "Failed to get legislator proposed bills")


@legislators_app.command("cosign-bills")
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
        page,
        limit,
        fields,
    )
    kwargs["bill_term"] = kwargs.pop("term")
    kwargs["term"] = term
    kwargs["name"] = name
    _run(api.GetLegislatorCosignBillsRequest(**kwargs), "Failed to get legislator co-signed bills")


@legislators_app.command("meets")
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


@legislators_app.command("interpellations")
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


@meets_app.command("list")
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


@meets_app.command("get")
def get_meet(meet_id: str) -> None:
    """Get meeting details."""
    _run(api.GetMeetRequest(meet_id=meet_id), "Failed to get meeting")


@meets_app.command("bills")
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
        page,
        limit,
        fields,
    )
    kwargs["meet_id"] = meet_id
    _run(api.GetMeetBillsRequest(**kwargs), "Failed to get meeting bills")


@meets_app.command("interpellations")
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


@meets_app.command("ivods")
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
