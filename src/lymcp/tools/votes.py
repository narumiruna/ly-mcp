import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetVoteMeetsRequest
from lymcp.api import GetVoteRequest
from lymcp.api import ListVotesRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_votes(
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-4-14")] = None,
    vote_type: Annotated[str | None, Field(description="表決型態，例：記名表決")] = None,
    vote_time: Annotated[str | None, Field(description="上游表決時間字串")] = None,
    voting_member: Annotated[str | None, Field(description="參與投票的委員姓名")] = None,
    agreeing_member: Annotated[str | None, Field(description="投贊成票的委員姓名")] = None,
    opposing_member: Annotated[str | None, Field(description="投反對票的委員姓名")] = None,
    abstaining_member: Annotated[str | None, Field(description="投棄權票的委員姓名")] = None,
    gazette_document_id: Annotated[str | None, Field(description="公報文件代碼，例：1150101_00002")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[list[str] | None, Field(description="自訂上游回傳欄位列表")] = None,
) -> str:
    """列出立法院表決紀錄。"""
    try:
        request = ListVotesRequest(
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
            output_fields=output_fields or [],
        )
        response = await request.do()
        return json.dumps(response, ensure_ascii=False, indent=2)
    except Exception as error:
        return _serialize_tool_error("Failed to list votes", error)


async def get_vote(
    vote_id: Annotated[str, Field(description="表決代碼，例：1150101_00002_55")],
) -> str:
    """取得特定表決紀錄。"""
    try:
        response = await GetVoteRequest(vote_id=vote_id).do()
        return json.dumps(response, ensure_ascii=False, indent=2)
    except Exception as error:
        return _serialize_tool_error("Failed to get vote", error)


async def get_vote_meets(
    vote_id: Annotated[str, Field(description="表決代碼，例：1150101_00002_55")],
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼，例：院會-11-2-6")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    meeting_type: Annotated[str | None, Field(description="會議種類，例：院會")] = None,
    member: Annotated[str | None, Field(description="出席委員姓名")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD")] = None,
    committee_code: Annotated[int | None, Field(description="委員會代號，例：23")] = None,
    meet_id: Annotated[str | None, Field(description="會議資料中的會議編號")] = None,
    bill_no: Annotated[str | None, Field(description="關係文書中的議案編號")] = None,
    law_number: Annotated[str | None, Field(description="關係文書中的法律編號")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[list[str] | None, Field(description="自訂上游回傳欄位列表")] = None,
) -> str:
    """取得特定表決所屬的會議列表。"""
    try:
        request = GetVoteMeetsRequest(
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
            output_fields=output_fields or [],
        )
        response = await request.do()
        return json.dumps(response, ensure_ascii=False, indent=2)
    except Exception as error:
        return _serialize_tool_error("Failed to get vote meets", error)
