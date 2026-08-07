import json
from typing import Annotated

from pydantic import Field

from lymcp.api import GetLawBillsRequest
from lymcp.api import GetLawContentRequest
from lymcp.api import GetLawProgressRequest
from lymcp.api import GetLawRequest
from lymcp.api import GetLawVersionContentsRequest
from lymcp.api import GetLawVersionRequest
from lymcp.api import GetLawVersionsRequest
from lymcp.api import ListLawContentsRequest
from lymcp.api import ListLawsRequest
from lymcp.api import ListLawVersionsRequest
from lymcp.tools.support import serialize_tool_error as _serialize_tool_error


async def list_laws(
    law_number: Annotated[str | None, Field(description="法律編號，例：09200015")] = None,
    category: Annotated[str | None, Field(description="類別，母法或子法")] = None,
    parent_law_number: Annotated[str | None, Field(description="母法編號，例：09200")] = None,
    law_status: Annotated[str | None, Field(description="法律狀態，例：現行")] = None,
    authority: Annotated[str | None, Field(description="主管機關，例：總統府")] = None,
    latest_version_date: Annotated[
        str | None, Field(description="最新版本日期，格式：YYYY-MM-DD，例：2024-10-25")
    ] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出立法院法律列表。

    Args:
        law_number: 法律編號，例：09200015
        category: 類別，母法或子法
        parent_law_number: 母法編號，例：09200
        law_status: 法律狀態，例：現行
        authority: 主管機關，例：總統府
        latest_version_date: 最新版本日期，格式：YYYY-MM-DD，例：2024-10-25
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的法律查詢結果。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListLawsRequest(
            law_number=law_number,
            category=category,
            parent_law_number=parent_law_number,
            law_status=law_status,
            authority=authority,
            latest_version_date=latest_version_date,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list laws", e)


async def get_law(
    law_id: Annotated[str, Field(description="法律編號，必填，例：09200015")],
) -> str:
    """
    取得特定法律的詳細資訊。

    Args:
        law_id: 法律編號，必填，例：09200015

    Returns:
        str: JSON 格式，包含法律基本資料、法條內容、版本資訊等詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawRequest(law_id=law_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law detail", e)


async def get_law_progress(
    law_id: Annotated[str, Field(description="法律編號，必填，例：09200015")],
) -> str:
    """
    取得特定法律的未議決進度列表。

    Args:
        law_id: 法律編號，必填，例：09200015

    Returns:
        str: JSON 格式，包含該法律相關的未議決進度資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawProgressRequest(law_id=law_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law progress", e)


async def get_law_bills(
    law_id: Annotated[str, Field(description="法律編號，必填，例：09200015")],
    term: Annotated[int | None, Field(description="屆，例：11")] = None,
    session: Annotated[int | None, Field(description="會期，例：2")] = None,
    bill_flow_status: Annotated[str | None, Field(description="議案流程狀態，如：交付審查、三讀")] = None,
    bill_type: Annotated[str | None, Field(description="議案類別，如：法律案、預算案")] = None,
    proposer: Annotated[str | None, Field(description="提案人姓名")] = None,
    cosigner: Annotated[str | None, Field(description="連署人姓名")] = None,
    law_number: Annotated[str | None, Field(description="法律編號")] = None,
    bill_status: Annotated[str | None, Field(description="議案狀態，如：交付審查、三讀、排入院會")] = None,
    meeting_code: Annotated[str | None, Field(description="會議代碼")] = None,
    proposal_source: Annotated[str | None, Field(description="提案來源，如：委員提案、政府提案")] = None,
    bill_number: Annotated[str | None, Field(description="議案編號")] = None,
    proposal_number: Annotated[str | None, Field(description="提案編號")] = None,
    reference_number: Annotated[str | None, Field(description="字號")] = None,
    article_number: Annotated[str | None, Field(description="法條編號")] = None,
    proposal_date: Annotated[str | None, Field(description="提案日期，格式：YYYY-MM-DD")] = None,
    proposal_unit_or_member: Annotated[str | None, Field(description="提案單位或提案委員")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得特定法律相關的議案列表。

    Args:
        law_id: 法律編號，必填，例：09200015
        term: 屆，例：11
        session: 會期，例：2
        bill_flow_status: 議案流程狀態，如：交付審查、三讀
        bill_type: 議案類別，如：法律案、預算案
        proposer: 提案人姓名
        cosigner: 連署人姓名
        law_number: 法律編號
        bill_status: 議案狀態，如：交付審查、三讀、排入院會
        meeting_code: 會議代碼
        proposal_source: 提案來源，如：委員提案、政府提案
        bill_number: 議案編號
        proposal_number: 提案編號
        reference_number: 字號
        article_number: 法條編號
        proposal_date: 提案日期，格式：YYYY-MM-DD
        proposal_unit_or_member: 提案單位或提案委員
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含該法律相關的議案資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawBillsRequest(
            law_id=law_id,
            term=term,
            session=session,
            bill_flow_status=bill_flow_status,
            bill_type=bill_type,
            proposer=proposer,
            co_proposer=cosigner,
            law_number=law_number,
            bill_status=bill_status,
            meeting_code=meeting_code,
            proposal_source=proposal_source,
            bill_number=bill_number,
            proposal_number=proposal_number,
            reference_number=reference_number,
            article_number=article_number,
            proposal_date=proposal_date,
            proposal_unit_or_member=proposal_unit_or_member,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law bills", e)


async def get_law_versions(
    law_id: Annotated[str, Field(description="法律編號，必填，例：09200015")],
    law_number: Annotated[str | None, Field(description="法律編號，例：90481")] = None,
    version_number: Annotated[str | None, Field(description="版本編號，例：90481:1944-02-29-制定")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD，例：1944-02-29")] = None,
    action: Annotated[str | None, Field(description="動作，例：制定")] = None,
    main_proposer: Annotated[str | None, Field(description="歷程主提案，例：張子揚")] = None,
    progress: Annotated[str | None, Field(description="歷程進度，例：一讀")] = None,
    current_version: Annotated[str | None, Field(description="現行版本，現行或非現行")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得特定法律過往的版本紀錄列表。

    Args:
        law_id: 法律編號，必填，例：09200015
        law_number: 法律編號，例：90481
        version_number: 版本編號，例：90481:1944-02-29-制定
        date: 日期，格式：YYYY-MM-DD，例：1944-02-29
        action: 動作，例：制定
        main_proposer: 歷程主提案，例：張子揚
        progress: 歷程進度，例：一讀
        current_version: 現行版本，現行或非現行
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含該法律的歷史版本紀錄資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawVersionsRequest(
            law_id=law_id,
            law_number=law_number,
            version_number=version_number,
            date=date,
            action=action,
            main_proposer=main_proposer,
            progress=progress,
            current_version=current_version,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law versions", e)


async def list_law_versions(
    law_number: Annotated[str | None, Field(description="法律編號，例：90481")] = None,
    version_number: Annotated[str | None, Field(description="版本編號，例：90481:1944-02-29-制定")] = None,
    date: Annotated[str | None, Field(description="日期，格式：YYYY-MM-DD，例：1944-02-29")] = None,
    action: Annotated[str | None, Field(description="動作，例：制定")] = None,
    main_proposer: Annotated[str | None, Field(description="歷程主提案，例：張子揚")] = None,
    progress: Annotated[str | None, Field(description="歷程進度，例：一讀")] = None,
    current_version: Annotated[str | None, Field(description="現行版本，現行或非現行")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20，建議不超過100")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出法律版本資料。

    Args:
        law_number: 法律編號，例：90481
        version_number: 版本編號，例：90481:1944-02-29-制定
        date: 日期，格式：YYYY-MM-DD，例：1944-02-29
        action: 動作，例：制定
        main_proposer: 歷程主提案，例：張子揚
        progress: 歷程進度，例：一讀
        current_version: 現行版本，現行或非現行
        page: 頁數，預設1
        limit: 每頁筆數，預設20，建議不超過100
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含法律版本列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListLawVersionsRequest(
            law_number=law_number,
            version_number=version_number,
            date=date,
            action=action,
            main_proposer=main_proposer,
            progress=progress,
            current_version=current_version,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list law versions", e)


async def get_law_version(
    law_version_id: Annotated[str, Field(description="版本編號，必填，例：90481:1944-02-29-制定")],
) -> str:
    """
    取得特定法律版本資訊。

    Args:
        law_version_id: 版本編號，必填，例：90481:1944-02-29-制定

    Returns:
        str: JSON 格式，包含法律版本詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawVersionRequest(law_version_id=law_version_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law version", e)


async def get_law_version_contents(
    law_version_id: Annotated[str, Field(description="版本編號，必填，例：90481:1944-02-29-制定")],
    law_number: Annotated[str | None, Field(description="法律編號，例：90481")] = None,
    version_id: Annotated[str | None, Field(description="法條資料版本編號，例：90481:1944-02-29-制定")] = None,
    order: Annotated[int | None, Field(description="順序，例：1")] = None,
    article_number: Annotated[str | None, Field(description="條號，例：第一條")] = None,
    current_version_status: Annotated[str | None, Field(description="現行版，可選值：現行、非現行")] = None,
    version_tracking: Annotated[str | None, Field(description="版本追蹤，例：new")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    取得法律版本包含的法條列表。

    Args:
        law_version_id: 版本編號，必填，例：90481:1944-02-29-制定
        law_number: 法律編號，例：90481
        version_id: 法條資料版本編號，例：90481:1944-02-29-制定
        order: 順序，例：1
        article_number: 條號，例：第一條
        current_version_status: 現行版，可選值：現行、非現行
        version_tracking: 版本追蹤，例：new
        page: 頁數，預設1
        limit: 每頁筆數，預設20
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式，包含特定法律版本的法條列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawVersionContentsRequest(
            law_version_id=law_version_id,
            law_number=law_number,
            version_id=version_id,
            order=order,
            article_number=article_number,
            current_version_status=current_version_status,
            version_tracking=version_tracking,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law version contents", e)


async def list_law_contents(
    law_number: Annotated[str | None, Field(description="法律編號，例：90481")] = None,
    version_id: Annotated[str | None, Field(description="版本編號，例：90481:90481:1944-02-29-制定:1")] = None,
    order: Annotated[int | None, Field(description="順序，例：1")] = None,
    article_number: Annotated[str | None, Field(description="條號，例：第一條")] = None,
    current_version_status: Annotated[str | None, Field(description="現行版，可選值：現行、非現行")] = None,
    version_tracking: Annotated[str | None, Field(description="版本追蹤，例：new")] = None,
    page: Annotated[int, Field(description="頁數，預設1")] = 1,
    limit: Annotated[int, Field(description="每頁筆數，預設20")] = 20,
    output_fields: Annotated[
        list[str] | None, Field(description="自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）")
    ] = None,
) -> str:
    """
    列出法條資料。

    Args:
        law_number: 法律編號，例：90481
        version_id: 版本編號，例：90481:90481:1944-02-29-制定:1
        order: 順序，例：1
        article_number: 條號，例：第一條
        current_version_status: 現行版，可選值：現行、非現行
        version_tracking: 版本追蹤，例：new
        page: 頁數，預設1
        limit: 每頁筆數，預設20
        output_fields: 自訂回傳欄位（如需指定欄位，請填寫欄位名稱列表）

    Returns:
        str: JSON 格式的法條列表。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = ListLawContentsRequest(
            law_number=law_number,
            version_id=version_id,
            order=order,
            article_number=article_number,
            current_version_status=current_version_status,
            version_tracking=version_tracking,
            page=page,
            limit=limit,
            output_fields=output_fields or [],
        )
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to list law contents", e)


async def get_law_content(
    law_content_id: Annotated[str, Field(description="法條編號，例：90481:90481:1944-02-29-制定:0")],
) -> str:
    """
    取得特定法條的詳細資訊。

    Args:
        law_content_id: 法條編號，例：90481:90481:1944-02-29-制定:0

    Returns:
        str: JSON 格式，包含該法條的詳細資訊。

    Raises:
        例外時回傳中文錯誤訊息字串。
    """
    try:
        req = GetLawContentRequest(law_content_id=law_content_id)
        resp = await req.do()
        return json.dumps(resp, ensure_ascii=False, indent=2)
    except Exception as e:
        return _serialize_tool_error("Failed to get law content", e)
