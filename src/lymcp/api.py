from typing import Final

import httpx
from loguru import logger
from pydantic import BaseModel
from pydantic import Field

BASE_URL: Final[str] = "https://ly.govapi.tw/v2"
HTTPX_TIMEOUT: Final[float] = 30.0


class SearchBillRequest(BaseModel):
    session: int | None = Field(default=None, serialization_alias="屆")
    term: int | None = Field(default=None, serialization_alias="會期")
    bill_flow_status: str | None = Field(default=None, serialization_alias="議案流程.狀態")
    bill_type: str | None = Field(default=None, serialization_alias="議案類別")
    proposer: str | None = Field(default=None, serialization_alias="提案人")
    co_proposer: str | None = Field(default=None, serialization_alias="連署人")
    law_number: str | None = Field(default=None, serialization_alias="法律編號")
    bill_status: str | None = Field(default=None, serialization_alias="議案狀態")
    meeting_code: str | None = Field(default=None, serialization_alias="會議代碼")
    proposal_source: str | None = Field(default=None, serialization_alias="提案來源")
    bill_number: str | None = Field(default=None, serialization_alias="議案編號")
    proposal_number: str | None = Field(default=None, serialization_alias="提案編號")
    reference_number: str | None = Field(default=None, serialization_alias="字號")
    article_number: str | None = Field(default=None, serialization_alias="法條編號")
    proposal_date: str | None = Field(default=None, serialization_alias="提案日期")
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True)
            logger.info("Searching bills with parameters: {}", params)

            resp = await client.get(f"{BASE_URL}/bills", params=params)
            resp.raise_for_status()

            return resp.json()


class GetBillDetailRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias="議案編號")

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting bill detail for bill_no: {}", self.bill_no)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}")
            resp.raise_for_status()
            return resp.json()


class BillMeetsRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias="議案編號")
    term: int | None = Field(default=None, serialization_alias="屆")
    session: int | None = Field(default=None, serialization_alias="會期")
    meeting_type: str | None = Field(default=None, serialization_alias="會議種類")
    date: str | None = Field(default=None, serialization_alias="日期")
    page: int = 1
    limit: int = 20

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True, exclude={"bill_no"})
            logger.info("Getting bill meets for bill_no: {}, params: {}", self.bill_no, params)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}/meets", params=params)
            resp.raise_for_status()
            return resp.json()


class BillRelatedBillsRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias="議案編號")
    page: int = 1
    limit: int = 20

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True, exclude={"bill_no"})
            logger.info("Getting bill related bills for bill_no: {}, params: {}", self.bill_no, params)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}/related_bills", params=params)
            resp.raise_for_status()
            return resp.json()


class BillDocHtmlRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias="議案編號")

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting bill doc html for bill_no: {}", self.bill_no)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}/doc_html")
            resp.raise_for_status()
            return resp.json()


class ListCommitteesRequest(BaseModel):
    committee_type: str | None = Field(default=None, serialization_alias="委員會類別")
    comt_cd: str | None = Field(default=None, serialization_alias="委員會代號")
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True)
            logger.info("Listing committees with parameters: {}", params)
            resp = await client.get(f"{BASE_URL}/committees", params=params)
            resp.raise_for_status()
            return resp.json()


class GetCommitteeRequest(BaseModel):
    comt_cd: str = Field(..., serialization_alias="委員會代號")

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting committee detail for comt_cd: {}", self.comt_cd)
            resp = await client.get(f"{BASE_URL}/committees/{self.comt_cd}")
            resp.raise_for_status()
            return resp.json()


class CommitteeMeetsRequest(BaseModel):
    comt_cd: str = Field(..., serialization_alias="委員會代號")
    term: int | None = Field(default=None, serialization_alias="屆")
    meeting_code: str | None = Field(default=None, serialization_alias="會議代碼")
    session: int | None = Field(default=None, serialization_alias="會期")
    meeting_type: str | None = Field(default=None, serialization_alias="會議種類")
    member: str | None = Field(default=None, serialization_alias="會議資料.出席委員")
    date: str | None = Field(default=None, serialization_alias="日期")
    committee_code: str | None = Field(default=None, serialization_alias="委員會代號")
    meet_id: str | None = Field(default=None, serialization_alias="會議資料.會議編號")
    bill_no: str | None = Field(default=None, serialization_alias="議事網資料.關係文書.議案.議案編號")
    law_number: str | None = Field(default=None, serialization_alias="議事網資料.關係文書.議案.法律編號")
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True, exclude={"comt_cd"})
            logger.info("Getting committee meets for comt_cd: {}, params: {}", self.comt_cd, params)
            resp = await client.get(f"{BASE_URL}/committees/{self.comt_cd}/meets", params=params)
            resp.raise_for_status()
            return resp.json()
