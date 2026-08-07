from mcp.server import MCPServer

from lymcp.tools.bills import get_bill
from lymcp.tools.bills import get_bill_doc_html
from lymcp.tools.bills import get_bill_meets
from lymcp.tools.bills import get_bill_related_bills
from lymcp.tools.bills import list_bills
from lymcp.tools.committees import get_committee
from lymcp.tools.committees import get_committee_meets
from lymcp.tools.committees import list_committees
from lymcp.tools.gazettes import get_gazette
from lymcp.tools.gazettes import get_gazette_agenda
from lymcp.tools.gazettes import get_gazette_agendas
from lymcp.tools.gazettes import list_gazette_agendas
from lymcp.tools.gazettes import list_gazettes
from lymcp.tools.interpellations import get_interpellation
from lymcp.tools.interpellations import get_legislator_interpellations
from lymcp.tools.interpellations import list_interpellations
from lymcp.tools.ivods import get_ivod
from lymcp.tools.ivods import get_meet_ivods
from lymcp.tools.ivods import list_ivods
from lymcp.tools.laws import get_law
from lymcp.tools.laws import get_law_bills
from lymcp.tools.laws import get_law_content
from lymcp.tools.laws import get_law_progress
from lymcp.tools.laws import get_law_version
from lymcp.tools.laws import get_law_version_contents
from lymcp.tools.laws import get_law_versions
from lymcp.tools.laws import list_law_contents
from lymcp.tools.laws import list_law_versions
from lymcp.tools.laws import list_laws
from lymcp.tools.legislators import get_legislator
from lymcp.tools.legislators import get_legislator_cosign_bills
from lymcp.tools.legislators import get_legislator_meets
from lymcp.tools.legislators import get_legislator_propose_bills
from lymcp.tools.legislators import list_legislators
from lymcp.tools.meets import get_meet
from lymcp.tools.meets import get_meet_bills
from lymcp.tools.meets import get_meet_interpellations
from lymcp.tools.meets import list_meets
from lymcp.tools.stats import get_stat
from lymcp.tools.votes import get_vote
from lymcp.tools.votes import get_vote_meets
from lymcp.tools.votes import list_votes

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = MCPServer("立法院 API v2 MCP Server", log_level="ERROR")


@mcp.resource(
    "lymcp://query-semantics",
    name="query_semantics",
    title="Query Semantics",
    description="Date semantics for latest known, latest occurred, and next scheduled Legislative Yuan records.",
    mime_type="text/markdown",
)
def query_semantics_resource() -> str:
    return """
# Query Semantics

Use Asia/Taipei calendar dates when comparing Legislative Yuan records.

- `latest known`: use the upstream default sort and do not remove future scheduled records.
- `latest occurred`: include only records whose relevant date is on or before the reference date.
- `next scheduled`: include only records whose relevant date is after the reference date, then choose the earliest date.

For meetings, compare values in `日期` or nested `會議資料.日期`.
For bills, compare `提案日期` or `最新進度日期` according to the user's question.
If a record contains multiple dates, explain which date was used.
""".strip()


@mcp.resource(
    "lymcp://workflow-reference",
    name="workflow_reference",
    title="Workflow Reference",
    description="Common MCP workflows, key tools, IDs, and high-value filters.",
    mime_type="text/markdown",
)
def workflow_reference_resource() -> str:
    return """
# Workflow Reference

## Latest Plenary Meeting Bills

Use `list_meets(meeting_type="院會", term=...)` to find candidate meetings.
Apply the date semantics from `lymcp://query-semantics`, then call
`get_meet_bills(meet_id=...)`.

## Law Amendment History

Use `list_laws` to resolve a law number from a law name.
Then use `get_law_versions(law_id=...)` or `list_law_versions(law_number=...)`.
Call `get_law_version_contents(law_version_id=...)` for article text in a version.

## Legislator Proposal Record

Use `get_legislator(term=..., name=...)` to confirm the legislator, then
`get_legislator_propose_bills(term=..., name=...)`.
Add bill filters such as `bill_type`, `proposal_date`, or `law_number` when the
question narrows scope.

## Legislator Interpellations

Use `get_legislator_interpellations(term=..., name=...)` or
`list_interpellations(interpellation_member=...)`.
Use `meeting_code` when the question references a specific meeting.

## Committee Meeting Lookup

Use `list_committees` to resolve committee codes when needed.
Then use `list_meets(meeting_type="委員會", committee_code=..., term=..., session=...)`
or `get_committee_meets(comt_cd=...)`.

## Legislator Vote Record

Use `list_votes(voting_member=..., term=...)` for every recorded participation,
or `agreeing_member`, `opposing_member`, and `abstaining_member` for a specific
position. Call `get_vote(vote_id=...)` for full details and
`get_vote_meets(vote_id=...)` for the related meeting context.
""".strip()


@mcp.prompt(
    name="latest_plenary_meeting_bills",
    title="Latest Plenary Meeting Bills",
    description="Find bills discussed in a latest-known, latest-occurred, or next-scheduled plenary meeting.",
)
def latest_plenary_meeting_bills(
    term: int = 11,
    reference_date: str = "today",
    semantics: str = "latest occurred",
) -> str:
    return f"""
Find bills discussed in the {semantics} plenary meeting for term {term}.

Use Asia/Taipei date comparisons. Treat the reference date as `{reference_date}`.
Use `list_meets` with `meeting_type="院會"` and `term={term}`.
If semantics is `latest occurred`, choose a meeting whose `日期` is on or before
the reference date. If semantics is `next scheduled`, choose the earliest meeting
after the reference date. If semantics is `latest known`, use the upstream
default sort without filtering out scheduled records. Then call `get_meet_bills`
with the selected `meet_id`.
""".strip()


@mcp.prompt(
    name="law_amendment_history",
    title="Law Amendment History",
    description="Resolve a law and inspect its amendment or version history.",
)
def law_amendment_history(law_name_or_number: str) -> str:
    return f"""
Look up the amendment history for `{law_name_or_number}`.

If the input is a law name, first call `list_laws` with a narrow filter or
output fields that expose `法律編號` and `名稱`. After resolving the law number,
call `get_law_versions` or `list_law_versions`. For a specific version, call
`get_law_version`; for article text in that version, call
`get_law_version_contents`.
""".strip()


@mcp.prompt(
    name="legislator_proposal_record",
    title="Legislator Proposal Record",
    description="Find bills proposed by a legislator.",
)
def legislator_proposal_record(name: str, term: int = 11) -> str:
    return f"""
Find proposal records for legislator `{name}` in term {term}.

First call `get_legislator(term={term}, name="{name}")` to confirm the
legislator. Then call `get_legislator_propose_bills(term={term}, name="{name}")`.
Use filters such as `bill_type`, `proposal_date`, `law_number`, or `bill_status`
if the question narrows the request.
""".strip()


@mcp.prompt(
    name="legislator_interpellations",
    title="Legislator Interpellations",
    description="Find interpellations by a legislator.",
)
def legislator_interpellations(name: str, term: int = 11) -> str:
    return f"""
Find interpellations by legislator `{name}` in term {term}.

Call `get_legislator_interpellations(term={term}, name="{name}")`.
If the user asks for all interpellations matching a member name across meetings,
use `list_interpellations(interpellation_member="{name}")`. Use `meeting_code`
when the question references a specific meeting.
""".strip()


@mcp.prompt(
    name="committee_meeting_lookup",
    title="Committee Meeting Lookup",
    description="Find committee meetings by term, session, committee, or date.",
)
def committee_meeting_lookup(term: int = 11, session: int | None = None, committee_code: int | None = None) -> str:
    return f"""
Find committee meetings for term {term}.

If needed, use `list_committees` to resolve the committee code.
Then call `list_meets` with `meeting_type="委員會"`, `term={term}`,
`session={session}`, and `committee_code={committee_code}` when those filters are known.
Use `get_committee_meets` when the committee code is already known and the user
wants records scoped to that committee.
""".strip()


@mcp.prompt(
    name="legislator_vote_record",
    title="Legislator Vote Record",
    description="Find a legislator's recorded votes and related meeting context.",
)
def legislator_vote_record(name: str, term: int = 11, position: str = "any") -> str:
    return f"""
Find vote records for legislator `{name}` in term {term} with position `{position}`.

Use `list_votes(term={term}, voting_member="{name}")` when position is `any`.
For a specific position, use exactly one of `agreeing_member`, `opposing_member`,
or `abstaining_member`. Resolve a selected result with `get_vote`, and call
`get_vote_meets` when the question needs meeting or related-bill context.
""".strip()


TOOLS = (
    get_stat,
    list_bills,
    get_bill,
    get_bill_related_bills,
    get_bill_meets,
    get_bill_doc_html,
    list_committees,
    get_committee,
    get_committee_meets,
    list_gazettes,
    get_gazette,
    get_gazette_agendas,
    list_gazette_agendas,
    get_gazette_agenda,
    list_interpellations,
    get_interpellation,
    get_legislator_interpellations,
    list_ivods,
    get_ivod,
    get_meet_ivods,
    list_laws,
    get_law,
    get_law_progress,
    get_law_bills,
    get_law_versions,
    list_law_versions,
    get_law_version,
    get_law_version_contents,
    list_law_contents,
    get_law_content,
    list_legislators,
    get_legislator,
    get_legislator_propose_bills,
    get_legislator_cosign_bills,
    get_legislator_meets,
    list_meets,
    get_meet,
    get_meet_bills,
    get_meet_interpellations,
    list_votes,
    get_vote,
    get_vote_meets,
)

for tool in TOOLS:
    mcp.tool()(tool)


def main() -> None:
    mcp.run()
