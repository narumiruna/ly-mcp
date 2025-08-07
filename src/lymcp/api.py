from typing import Final

import httpx
from loguru import logger
from pydantic import BaseModel
from pydantic import Field

from .translate import translate

BASE_URL: Final[str] = "https://ly.govapi.tw/v2"
HTTPX_TIMEOUT: Final[float] = 30.0

class GetStatRequest(BaseModel):
    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting statistics")
            resp = await client.get(f"{BASE_URL}/stat")
            resp.raise_for_status()
            return resp.json()

class ListBillRequest(BaseModel):
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    bill_flow_status: str | None = Field(default=None, serialization_alias=translate["bill_flow_status"])
    bill_type: str | None = Field(default=None, serialization_alias=translate["bill_type"])
    proposer: str | None = Field(default=None, serialization_alias=translate["proposer"])
    co_proposer: str | None = Field(default=None, serialization_alias=translate["co_proposer"])
    law_number: str | None = Field(default=None, serialization_alias=translate["law_number"])
    bill_status: str | None = Field(default=None, serialization_alias=translate["bill_status"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    proposal_source: str | None = Field(default=None, serialization_alias=translate["proposal_source"])
    bill_number: str | None = Field(default=None, serialization_alias=translate["bill_number"])
    proposal_number: str | None = Field(default=None, serialization_alias=translate["proposal_number"])
    reference_number: str | None = Field(default=None, serialization_alias=translate["reference_number"])
    article_number: str | None = Field(default=None, serialization_alias=translate["article_number"])
    proposal_date: str | None = Field(default=None, serialization_alias=translate["proposal_date"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            params = self.model_dump(exclude_none=True, by_alias=True)
            logger.info("Listing bills with parameters: {}", params)

            resp = await client.get(f"{BASE_URL}/bills", params=params)
            resp.raise_for_status()

            return resp.json()


class GetBillDetailRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting bill detail for bill_no: {}", self.bill_no)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}")
            resp.raise_for_status()
            return resp.json()


class BillMeetsRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_type: str | None = Field(default=None, serialization_alias=translate["meeting_type"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
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
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])
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
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting bill doc html for bill_no: {}", self.bill_no)
            resp = await client.get(f"{BASE_URL}/bills/{self.bill_no}/doc_html")
            resp.raise_for_status()
            return resp.json()


class ListCommitteesRequest(BaseModel):
    committee_type: str | None = Field(default=None, serialization_alias=translate["committee_type"])
    comt_cd: str | None = Field(default=None, serialization_alias=translate["comt_cd"])
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
    comt_cd: str = Field(..., serialization_alias=translate["comt_cd"])

    async def do(self) -> dict:
        async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
            logger.info("Getting committee detail for comt_cd: {}", self.comt_cd)
            resp = await client.get(f"{BASE_URL}/committees/{self.comt_cd}")
            resp.raise_for_status()
            return resp.json()


class CommitteeMeetsRequest(BaseModel):
    comt_cd: str = Field(..., serialization_alias=translate["comt_cd"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_type: str | None = Field(default=None, serialization_alias=translate["meeting_type"])
    member: str | None = Field(default=None, serialization_alias=translate["member"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    committee_code: str | None = Field(default=None, serialization_alias=translate["committee_code"])
    meet_id: str | None = Field(default=None, serialization_alias=translate["meet_id"])
    bill_no: str | None = Field(default=None, serialization_alias=translate["bill_no_nested"])
    law_number: str | None = Field(default=None, serialization_alias=translate["law_number_nested"])
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
