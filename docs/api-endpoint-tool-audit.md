# API Endpoint to MCP Tool Audit

This audit maps Legislative Yuan API v2 endpoints from `swagger.yaml` to the MCP tools exposed by `src/lymcp/server.py`.

## Endpoint Coverage

| API endpoint | MCP tool | Status |
| --- | --- | --- |
| `/stat` | `get_stat` | covered |
| `/bills` | `list_bills` | covered |
| `/bills/{billNo}` | `get_bill` | covered |
| `/bills/{billNo}/related_bills` | `get_bill_related_bills` | covered |
| `/bills/{billNo}/doc_html` | `get_bill_doc_html` | covered |
| `/bills/{billNo}/meets` | `get_bill_meets` | covered |
| `/committees` | `list_committees` | covered |
| `/committees/{comtCd}` | `get_committee` | covered |
| `/committees/{comtCd}/meets` | `get_committee_meets` | covered |
| `/gazettes` | `list_gazettes` | covered |
| `/gazettes/{id}` | `get_gazette` | covered |
| `/gazettes/{id}/agendas` | `get_gazette_agendas` | covered |
| `/gazette_agendas` | `list_gazette_agendas` | covered |
| `/gazette_agendas/{id}` | `get_gazette_agenda` | covered |
| `/interpellations` | `list_interpellations` | covered |
| `/interpellations/{id}` | `get_interpellation` | covered |
| `/ivods` | `list_ivods` | covered |
| `/ivods/{id}` | `get_ivod` | covered |
| `/laws` | `list_laws` | covered |
| `/laws/{id}` | `get_law` | covered |
| `/laws/{id}/progress` | `get_law_progress` | covered |
| `/laws/{id}/bills` | `get_law_bills` | covered |
| `/laws/{id}/versions` | `get_law_versions` | covered |
| `/law_contents` | `list_law_contents` | covered |
| `/law_contents/{id}` | `get_law_content` | covered |
| `/law_versions` | `list_law_versions` | covered |
| `/law_versions/{id}` | `get_law_version` | covered |
| `/law_versions/{id}/contents` | `get_law_version_contents` | covered |
| `/legislators` | `list_legislators` | covered |
| `/legislators/{term}/{name}` | `get_legislator` | covered |
| `/legislators/{term}/{name}/propose_bills` | `get_legislator_propose_bills` | covered |
| `/legislators/{term}/{name}/cosign_bills` | `get_legislator_cosign_bills` | covered |
| `/legislators/{term}/{name}/meets` | `get_legislator_meets` | covered |
| `/legislators/{term}/{name}/interpellations` | `get_legislator_interpellations` | covered |
| `/meets` | `list_meets` | covered |
| `/meets/{id}` | `get_meet` | covered |
| `/meets/{id}/ivods` | `get_meet_ivods` | covered |
| `/meets/{id}/bills` | `get_meet_bills` | covered |
| `/meets/{id}/interpellations` | `get_meet_interpellations` | covered |

## Filter Field Decisions

The MCP tools expose stable, high-value query fields as first-class parameters. All list-style tools also keep `output_fields` so users can request specific response fields supported by the upstream API.

| Category | Field | Decision | Notes |
| --- | --- | --- | --- |
| Bills | `提案單位/提案委員` | first-class parameter | Added as `proposal_unit_or_member` on `list_bills` because live responses advertise it in `supported_filter_fields`. |
| Bills | Other `supported_filter_fields` already listed in `swagger.yaml` | first-class parameters | Covered by existing bill request models where applicable. |
| Laws | Law version filters: `法律編號`, `版本編號`, `日期`, `動作`, `歷程.主提案`, `歷程.進度`, `現行版本` | first-class parameters | Covered by `list_law_versions` and existing nested `get_law_versions`. |
| Law contents | `法律編號`, `版本編號`, `順序`, `條號`, `現行版`, `版本追蹤` | first-class parameters | Covered by `list_law_contents` and `get_law_version_contents`. |
| Meetings, IVODs, legislators | Fields represented by current request models | first-class parameters | No new missing high-value fields were promoted in this pass. |
| Any endpoint | Response-only fields not accepted as filters | deferred | Keep accessible through `output_fields`; promote only after `swagger.yaml` or live `supported_filter_fields` confirms filter support. |

## Verification

- `rg "^  /" swagger.yaml` lists 39 endpoints.
- `rg "@mcp.tool" src/lymcp/server.py` lists 39 MCP tools.
- `tests/test_api_mock.py` covers URL and parameter serialization for all request classes, including top-level Law Version endpoints.
- `tests/test_server_mock.py` covers tool-to-request wiring for all tools, including Law Version tools.
- Live smoke verified `list_law_versions`, `get_law_version`, and `get_law_version_contents` with version ID `90481:1944-02-29-制定`.
- Live smoke verified that the upstream API accepts the bill filter `提案單位/提案委員`.
