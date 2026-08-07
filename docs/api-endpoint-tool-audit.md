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
| `/votes` | `list_votes` | covered |
| `/votes/{id}` | `get_vote` | covered |
| `/votes/{id}/meets` | `get_vote_meets` | covered |

## Filter Field Decisions

The MCP tools expose stable, high-value query fields as first-class parameters. All list-style tools also keep `output_fields` so users can request specific response fields supported by the upstream API.

| Category | Field | Decision | Notes |
| --- | --- | --- | --- |
| Bills | `提案單位/提案委員` | first-class parameter | Exposed as `proposal_unit_or_member` on all five Swagger bill-listing paths. |
| Bills | Other `supported_filter_fields` already listed in `swagger.yaml` | first-class parameters | Covered by existing bill request models where applicable. |
| Gazette agendas | `期`, `冊別` | first-class parameters | Exposed as `issue` and `booklet` on both gazette agenda list paths. |
| Gazette agendas | `公報編號` on `/gazettes/{id}/agendas` | first-class parameter | Exposed as `gazette_number` so it remains distinct from the required `gazette_id` path value. |
| Votes | `屆`, `會議代碼`, `表決型態`, `表決時間`, `投票委員`, `贊成`, `反對`, `棄權`, `公報文件代碼` | first-class parameters | Covered by `list_votes`; Vote meeting relations expose all documented meeting filters. |
| Laws | Law version filters: `法律編號`, `版本編號`, `日期`, `動作`, `歷程.主提案`, `歷程.進度`, `現行版本` | first-class parameters | Covered by `list_law_versions` and existing nested `get_law_versions`. |
| Law contents | `法律編號`, `版本編號`, `順序`, `條號`, `現行版`, `版本追蹤` | first-class parameters | Covered by `list_law_contents` and `get_law_version_contents`. |
| Bill meetings | All 13 query fields on `/bills/{billNo}/meets` | first-class parameters | Meeting, attendee, committee, nested bill/law, pagination, and output-field filters are distinct from the required bill path value. |
| Meetings, IVODs, legislators | Fields represented by current request models | first-class parameters | All query fields declared by the current Swagger contract are serialized. |
| Any endpoint | Response-only fields not accepted as filters | deferred | Keep accessible through `output_fields`; promote only after `swagger.yaml` or live `supported_filter_fields` confirms filter support. |

## Verification

- `swagger.yaml` lists 42 endpoints, and the server registers 42 MCP tools.
- `tests/test_swagger_coverage.py` maps every Swagger path to one MCP tool, one CLI command path, and one request model.
- The Swagger serialization audit verifies all 298 endpoint/query-parameter slots are present in emitted request parameters.
- `tests/test_api_mock.py` covers URL and parameter serialization for all request classes, including distinct path/query identifiers.
- `tests/test_server_mock.py` covers tool-to-request wiring and response contracts for all tools.
- Live smoke covers Vote list/detail/meeting relations and the nested bill and gazette filters.
