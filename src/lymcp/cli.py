from pathlib import Path
from typing import Annotated

import typer

from lymcp import api
from lymcp.commands.bills import app as bills_app
from lymcp.commands.committees import app as committees_app
from lymcp.commands.gazette_agendas import app as gazette_agendas_app
from lymcp.commands.gazettes import app as gazettes_app
from lymcp.commands.interpellations import app as interpellations_app
from lymcp.commands.ivods import app as ivods_app
from lymcp.commands.law_contents import app as law_contents_app
from lymcp.commands.law_versions import app as law_versions_app
from lymcp.commands.laws import app as laws_app
from lymcp.commands.legislators import app as legislators_app
from lymcp.commands.meets import app as meets_app
from lymcp.commands.support import _run
from lymcp.commands.support import configure_output
from lymcp.commands.votes import app as votes_app

app = typer.Typer(no_args_is_help=True, help="Query Taiwan Legislative Yuan API v2 from the terminal.")
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
app.add_typer(votes_app, name="votes")

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
    ("votes", "list"),
    ("votes", "get"),
    ("votes", "meets"),
)


@app.callback()
def main(
    compact: Annotated[bool, typer.Option("--compact", help="Print compact single-line JSON.")] = False,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Write successful JSON output to a file."),
    ] = None,
) -> None:
    """Query Taiwan Legislative Yuan API v2."""
    configure_output(compact=compact, output_path=output)


@app.command("stat")
def stat() -> None:
    """Get API statistics."""
    _run(api.GetStatRequest(), "Failed to get statistics")
