from typing import Final

import httpx
from loguru import logger
from pydantic import BaseModel
from pydantic import Field

from .translate import translate

BASE_URL: Final[str] = "https://ly.govapi.tw/v2"
HTTPX_TIMEOUT: Final[float] = 30.0

async def make_api_request(url: str, method: str = "GET", params: dict | None = None) -> dict:
    """Shared function to make API requests with consistent error handling."""
    async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
        if method.upper() == "GET":
            resp = await client.get(url, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        resp.raise_for_status()
        return resp.json()

class GetStatRequest(BaseModel):
    async def do(self) -> dict:
        logger.info("Getting statistics")
        return await make_api_request(
            url=f"{BASE_URL}/stat"
        )

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
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing bills with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/bills",
            params=params,
        )

class GetBillRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])

    async def do(self) -> dict:
        logger.info("Getting bill detail for bill_no: {}", self.bill_no)
        return await make_api_request(
            url=f"{BASE_URL}/bills/{self.bill_no}",
        )

class GetBillMeetsRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_type: str | None = Field(default=None, serialization_alias=translate["meeting_type"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    page: int = 1
    limit: int = 20

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"bill_no"})
        logger.info("Getting bill meets for bill_no: {}, params: {}", self.bill_no, params)
        return await make_api_request(
            url=f"{BASE_URL}/bills/{self.bill_no}/meets",
            params=params,
        )

class GetBillRelatedBillsRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])
    page: int = 1
    limit: int = 20

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"bill_no"})
        logger.info("Getting bill related bills for bill_no: {}, params: {}", self.bill_no, params)
        return await make_api_request(
            url=f"{BASE_URL}/bills/{self.bill_no}/related_bills",
            params=params,
        )

class GetBillDocHtmlRequest(BaseModel):
    bill_no: str = Field(..., serialization_alias=translate["bill_no"])

    async def do(self) -> dict:
        logger.info("Getting bill doc html for bill_no: {}", self.bill_no)
        return await make_api_request(
            url=f"{BASE_URL}/bills/{self.bill_no}/doc_html",
        )

class ListCommitteesRequest(BaseModel):
    committee_type: str | None = Field(default=None, serialization_alias=translate["committee_type"])
    comt_cd: str | None = Field(default=None, serialization_alias=translate["comt_cd"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing committees with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/committees",
            params=params,
        )

class GetCommitteeRequest(BaseModel):
    comt_cd: str = Field(..., serialization_alias=translate["comt_cd"])

    async def do(self) -> dict:
        logger.info("Getting committee detail for comt_cd: {}", self.comt_cd)
        return await make_api_request(
            url=f"{BASE_URL}/committees/{self.comt_cd}",
        )

class GetCommitteeMeetsRequest(BaseModel):
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
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"comt_cd"})
        logger.info("Getting committee meets for comt_cd: {}, params: {}", self.comt_cd, params)
        return await make_api_request(
            url=f"{BASE_URL}/committees/{self.comt_cd}/meets",
            params=params,
        )


class ListGazettesRequest(BaseModel):
    gazette_id: str | None = Field(default=None, serialization_alias=translate["gazette_id"])
    volume: int | None = Field(default=None, serialization_alias=translate["volume"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing gazettes with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/gazettes",
            params=params,
        )


class GetGazetteRequest(BaseModel):
    gazette_id: str = Field(..., serialization_alias=translate["gazette_id"])

    async def do(self) -> dict:
        logger.info("Getting gazette detail for gazette_id: {}", self.gazette_id)
        return await make_api_request(
            url=f"{BASE_URL}/gazettes/{self.gazette_id}",
        )


class GetGazetteAgendasRequest(BaseModel):
    gazette_id: str = Field(..., serialization_alias=translate["gazette_id"])
    volume: int | None = Field(default=None, serialization_alias=translate["volume"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    meeting_date: str | None = Field(default=None, serialization_alias=translate["meeting_date"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"gazette_id"})
        logger.info("Getting gazette agendas for gazette_id: {}, params: {}", self.gazette_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/gazettes/{self.gazette_id}/agendas",
            params=params,
        )


class ListGazetteAgendasRequest(BaseModel):
    gazette_id: str | None = Field(default=None, serialization_alias=translate["gazette_id"])
    volume: int | None = Field(default=None, serialization_alias=translate["volume"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    meeting_date: str | None = Field(default=None, serialization_alias=translate["meeting_date"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing gazette agendas with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/gazette_agendas",
            params=params,
        )


class GetGazetteAgendaRequest(BaseModel):
    gazette_agenda_id: str = Field(..., serialization_alias=translate["gazette_agenda_id"])

    async def do(self) -> dict:
        logger.info("Getting gazette agenda detail for gazette_agenda_id: {}", self.gazette_agenda_id)
        return await make_api_request(
            url=f"{BASE_URL}/gazette_agendas/{self.gazette_agenda_id}",
        )


class ListInterpellationsRequest(BaseModel):
    interpellation_member: str | None = Field(default=None, serialization_alias=translate["interpellation_member"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing interpellations with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/interpellations",
            params=params,
        )


class GetInterpellationRequest(BaseModel):
    interpellation_id: str = Field(..., serialization_alias=translate["interpellation_id"])

    async def do(self) -> dict:
        logger.info("Getting interpellation detail for interpellation_id: {}", self.interpellation_id)
        return await make_api_request(
            url=f"{BASE_URL}/interpellations/{self.interpellation_id}",
        )


class GetLegislatorInterpellationsRequest(BaseModel):
    term: int = Field(..., serialization_alias=translate["term"])
    name: str
    interpellation_member: str | None = Field(default=None, serialization_alias=translate["interpellation_member"])
    term_query: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"term", "name"})
        logger.info("Getting legislator interpellations for term: {}, name: {}, params: {}",
            self.term, self.name, params)
        return await make_api_request(
            url=f"{BASE_URL}/legislators/{self.term}/{self.name}/interpellations",
            params=params,
        )


class ListIvodsRequest(BaseModel):
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code_detailed"])
    member_name: str | None = Field(default=None, serialization_alias=translate["member_name"])
    committee_code: int | None = Field(default=None, serialization_alias=translate["committee_code_detailed"])
    meeting_code_data: str | None = Field(default=None, serialization_alias=translate["meeting_code_data"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    video_type: str | None = Field(default=None, serialization_alias=translate["video_type"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing IVODs with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/ivods",
            params=params,
        )


class GetIvodRequest(BaseModel):
    ivod_id: str = Field(..., serialization_alias=translate["ivod_id"])

    async def do(self) -> dict:
        logger.info("Getting IVOD detail for ivod_id: {}", self.ivod_id)
        return await make_api_request(
            url=f"{BASE_URL}/ivods/{self.ivod_id}",
        )


class GetMeetIvodsRequest(BaseModel):
    meet_id: str = Field(..., serialization_alias=translate["meet_id"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code_detailed"])
    member_name: str | None = Field(default=None, serialization_alias=translate["member_name"])
    committee_code: int | None = Field(default=None, serialization_alias=translate["committee_code_detailed"])
    meeting_code_data: str | None = Field(default=None, serialization_alias=translate["meeting_code_data"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    video_type: str | None = Field(default=None, serialization_alias=translate["video_type"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"meet_id"})
        logger.info("Getting meet IVODs for meet_id: {}, params: {}", self.meet_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/meets/{self.meet_id}/ivods",
            params=params,
        )


class ListLawsRequest(BaseModel):
    law_number: str | None = Field(default=None, serialization_alias=translate["law_number"])
    category: str | None = Field(default=None, serialization_alias=translate["law_category"])
    parent_law_number: str | None = Field(default=None, serialization_alias=translate["parent_law_number"])
    law_status: str | None = Field(default=None, serialization_alias=translate["law_status"])
    authority: str | None = Field(default=None, serialization_alias=translate["authority"])
    latest_version_date: str | None = Field(default=None, serialization_alias=translate["latest_version_date"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing laws with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/laws",
            params=params,
        )


class GetLawRequest(BaseModel):
    law_id: str = Field(..., serialization_alias=translate["law_id"])

    async def do(self) -> dict:
        logger.info("Getting law detail for law_id: {}", self.law_id)
        return await make_api_request(
            url=f"{BASE_URL}/laws/{self.law_id}",
        )


class GetLawProgressRequest(BaseModel):
    law_id: str = Field(..., serialization_alias=translate["law_id"])

    async def do(self) -> dict:
        logger.info("Getting law progress for law_id: {}", self.law_id)
        return await make_api_request(
            url=f"{BASE_URL}/laws/{self.law_id}/progress",
        )


class GetLawBillsRequest(BaseModel):
    law_id: str = Field(..., serialization_alias=translate["law_id"])
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
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"law_id"})
        logger.info("Getting law bills for law_id: {}, params: {}", self.law_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/laws/{self.law_id}/bills",
            params=params,
        )


class GetLawVersionsRequest(BaseModel):
    law_id: str = Field(..., serialization_alias=translate["law_id"])
    law_number: str | None = Field(default=None, serialization_alias=translate["law_number"])
    version_number: str | None = Field(default=None, serialization_alias=translate["version_number"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    action: str | None = Field(default=None, serialization_alias=translate["action"])
    main_proposer: str | None = Field(default=None, serialization_alias=translate["main_proposer"])
    progress: str | None = Field(default=None, serialization_alias=translate["progress"])
    current_version: str | None = Field(default=None, serialization_alias=translate["current_version"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"law_id"})
        logger.info("Getting law versions for law_id: {}, params: {}", self.law_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/laws/{self.law_id}/versions",
            params=params,
        )


class ListLawContentsRequest(BaseModel):
    law_number: str | None = Field(default=None, serialization_alias=translate["law_number"])
    version_id: str | None = Field(default=None, serialization_alias=translate["version_id"])
    order: int | None = Field(default=None, serialization_alias=translate["order"])
    article_number: str | None = Field(default=None, serialization_alias=translate["law_article_number"])
    current_version_status: str | None = Field(default=None, serialization_alias=translate["current_version_status"])
    version_tracking: str | None = Field(default=None, serialization_alias=translate["version_tracking"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing law contents with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/law_contents",
            params=params,
        )


class GetLawContentRequest(BaseModel):
    law_content_id: str = Field(..., serialization_alias=translate["law_content_id"])

    async def do(self) -> dict:
        logger.info("Getting law content detail for law_content_id: {}", self.law_content_id)
        return await make_api_request(
            url=f"{BASE_URL}/law_contents/{self.law_content_id}",
        )


# Legislators API models

class ListLegislatorsRequest(BaseModel):
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    party: str | None = Field(default=None, serialization_alias=translate["party"])
    district_name: str | None = Field(default=None, serialization_alias=translate["district_name"])
    legislator_id: int | None = Field(default=None, serialization_alias=translate["legislator_id"])
    legislator_name: str | None = Field(default=None, serialization_alias=translate["legislator_name"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing legislators with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/legislators",
            params=params,
        )


class GetLegislatorRequest(BaseModel):
    term: int = Field(...)
    name: str = Field(...)

    async def do(self) -> dict:
        logger.info("Getting legislator detail for term: {}, name: {}", self.term, self.name)
        return await make_api_request(
            url=f"{BASE_URL}/legislators/{self.term}/{self.name}",
        )


class GetLegislatorProposeBillsRequest(BaseModel):
    term: int = Field(...)
    name: str = Field(...)
    # Bill search parameters
    bill_term: int | None = Field(default=None, serialization_alias=translate["term"])
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
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"term", "name"})
        logger.info("Getting legislator propose bills for term: {}, name: {}, params: {}", self.term, self.name, params)
        return await make_api_request(
            url=f"{BASE_URL}/legislators/{self.term}/{self.name}/propose_bills",
            params=params,
        )


class GetLegislatorCosignBillsRequest(BaseModel):
    term: int = Field(...)
    name: str = Field(...)
    # Bill search parameters
    bill_term: int | None = Field(default=None, serialization_alias=translate["term"])
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
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"term", "name"})
        logger.info("Getting legislator cosign bills for term: {}, name: {}, params: {}", self.term, self.name, params)
        return await make_api_request(
            url=f"{BASE_URL}/legislators/{self.term}/{self.name}/cosign_bills",
            params=params,
        )


class GetLegislatorMeetsRequest(BaseModel):
    term: int = Field(...)
    name: str = Field(...)
    # Meet search parameters
    meet_term: int | None = Field(default=None, serialization_alias=translate["term"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_type: str | None = Field(default=None, serialization_alias=translate["meeting_type"])
    member: str | None = Field(default=None, serialization_alias=translate["member"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    committee_code: int | None = Field(default=None, serialization_alias=translate["committee_code"])
    meet_id: str | None = Field(default=None, serialization_alias=translate["meet_id"])
    bill_no_nested: str | None = Field(default=None, serialization_alias=translate["bill_no_nested"])
    law_number_nested: str | None = Field(default=None, serialization_alias=translate["law_number_nested"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"term", "name"})
        logger.info("Getting legislator meets for term: {}, name: {}, params: {}", self.term, self.name, params)
        return await make_api_request(
            url=f"{BASE_URL}/legislators/{self.term}/{self.name}/meets",
            params=params,
        )


class ListMeetsRequest(BaseModel):
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_type: str | None = Field(default=None, serialization_alias=translate["meeting_type"])
    meeting_attendee: str | None = Field(default=None, serialization_alias=translate["meeting_attendee"])
    date: str | None = Field(default=None, serialization_alias=translate["date"])
    committee_code: int | None = Field(default=None, serialization_alias=translate["committee_code"])
    meeting_id: str | None = Field(default=None, serialization_alias=translate["meeting_id"])
    meeting_bills_bill_no: str | None = Field(default=None, serialization_alias=translate["meeting_bills_bill_no"])
    meeting_bills_law_no: str | None = Field(default=None, serialization_alias=translate["meeting_bills_law_no"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True)
        logger.info("Listing meets with parameters: {}", params)
        return await make_api_request(
            url=f"{BASE_URL}/meets",
            params=params,
        )


class GetMeetRequest(BaseModel):
    meet_id: str = Field(...)

    async def do(self) -> dict:
        logger.info("Getting meet detail for meet_id: {}", self.meet_id)
        return await make_api_request(
            url=f"{BASE_URL}/meets/{self.meet_id}",
        )


class GetMeetBillsRequest(BaseModel):
    meet_id: str = Field(...)
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
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"meet_id"})
        logger.info("Getting meet bills for meet_id: {}, params: {}", self.meet_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/meets/{self.meet_id}/bills",
            params=params,
        )


class GetMeetInterpellationsRequest(BaseModel):
    meet_id: str = Field(...)
    interpellation_member: str | None = Field(default=None, serialization_alias=translate["interpellation_member"])
    term: int | None = Field(default=None, serialization_alias=translate["term"])
    session: int | None = Field(default=None, serialization_alias=translate["session"])
    meeting_code: str | None = Field(default=None, serialization_alias=translate["meeting_code"])
    page: int = 1
    limit: int = 20
    output_fields: list[str] = Field(default_factory=list)

    async def do(self) -> dict:
        params = self.model_dump(exclude_none=True, by_alias=True, exclude={"meet_id"})
        logger.info("Getting meet interpellations for meet_id: {}, params: {}", self.meet_id, params)
        return await make_api_request(
            url=f"{BASE_URL}/meets/{self.meet_id}/interpellations",
            params=params,
        )
