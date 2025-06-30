from mcp.server.fastmcp import FastMCP

from .tools.bill_detail import get_bill_detail
from .tools.bill_detail import get_bill_doc_html
from .tools.bill_detail import get_bill_related_bills
from .tools.bill_meets import get_bill_meets
from .tools.search_bills import search_bills

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("立法院 API v2 MCP Server", log_level="ERROR")


mcp.tool()(search_bills)
mcp.tool()(get_bill_detail)
mcp.tool()(get_bill_related_bills)
mcp.tool()(get_bill_doc_html)
mcp.tool()(get_bill_meets)


def main():
    mcp.run()
