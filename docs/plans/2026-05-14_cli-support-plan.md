## Goal

讓 `lymcp` 另外提供一個以 `ly` 開頭的 Typer CLI，讓 agents 可以直接從 terminal 查詢立法院 API v2 資料，並能搭配 agent skills 穩定產生、執行、解析指令。成功條件是使用者可安裝套件後執行 `ly ...`，用一致的 command tree 查詢統計、議案、法律、會議、委員、公報、質詢與 IVOD 資料，且輸出預設為 agent-friendly JSON。

## Context

目前 `src/lymcp/api.py` 已有每個 endpoint 的 Pydantic request class 與 `.do()` 方法，`src/lymcp/server.py` 只是把這些 request class 包成 MCP tools。CLI 應重用 `api.py`，不要再建立第二套 HTTP client 或 query serialization。

目前 `pyproject.toml` 只有 `lymcp = "lymcp.server:main"` console script。新增 CLI 時，應保留 MCP server script，另外新增 `ly = "lymcp.cli:app"` 或等價入口。

## Architecture

CLI 採三層結構：

- `src/lymcp/cli.py`：Typer app 與 command wiring，只負責參數、輸出格式、exit code。
- `src/lymcp/cli_runner.py` 或 `src/lymcp/cli_output.py`：共用 async 執行、JSON pretty print、錯誤轉 exit code 的小型 helper。
- `src/lymcp/api.py`：既有 Request class 繼續作為唯一 API access layer。

Command tree 以資料領域分組，保留與 MCP tools 接近的命名，讓 agent skills 可以從 MCP tool 名稱直覺映射到 CLI：

```text
ly stat

ly bills list [filters]
ly bills get BILL_NO
ly bills related BILL_NO [--page N --limit N]
ly bills meets BILL_NO [filters]
ly bills doc-html BILL_NO

ly committees list [filters]
ly committees get COMT_CD
ly committees meets COMT_CD [filters]

ly gazettes list [filters]
ly gazettes get GAZETTE_ID
ly gazettes agendas GAZETTE_ID [filters]
ly gazette-agendas list [filters]
ly gazette-agendas get GAZETTE_AGENDA_ID

ly interpellations list [filters]
ly interpellations get INTERPELLATION_ID

ly ivods list [filters]
ly ivods get IVOD_ID

ly laws list [filters]
ly laws get LAW_ID
ly laws progress LAW_ID
ly laws bills LAW_ID [filters]
ly laws versions LAW_ID [filters]
ly law-versions list [filters]
ly law-versions get LAW_VERSION_ID
ly law-versions contents LAW_VERSION_ID [filters]
ly law-contents list [filters]
ly law-contents get LAW_CONTENT_ID

ly legislators list [filters]
ly legislators get TERM NAME
ly legislators propose-bills TERM NAME [filters]
ly legislators cosign-bills TERM NAME [filters]
ly legislators meets TERM NAME [filters]
ly legislators interpellations TERM NAME [filters]

ly meets list [filters]
ly meets get MEET_ID
ly meets bills MEET_ID [filters]
ly meets interpellations MEET_ID [filters]
ly meets ivods MEET_ID [filters]
```

Command 設計原則：

- 用 plural noun group 對應 list/get workflow，例如 `ly bills list`、`ly bills get`。
- 子資源用自然名詞或動詞片語，例如 `related`、`meets`、`doc-html`、`versions`。
- ID 採 positional argument，filters 採 options，方便 agents 組指令時分清必填與選填。
- filter option 名稱沿用 Python/MCP 參數的英文 snake/kebab 語意，例如 `--bill-type`、`--proposal-date`、`--committee-code`。
- 預設輸出 pretty JSON；全域提供 `--compact` 產生單行 JSON，`--output PATH` 寫入檔案，`--fields a,b,c` 對應 `output_fields`。
- 錯誤輸出沿用目前 MCP 的 JSON error envelope，CLI exit code 非 0，讓 agents 能可靠判斷失敗。

## Tech Stack

- 新增 runtime dependency：`typer`，用 `uv add typer` 更新 `pyproject.toml` 與 `uv.lock`。
- 使用 Typer `app = typer.Typer(...)` 建立多層 command app。
- 使用 `asyncio.run()` 執行既有 async request `.do()`。
- 測試使用 `typer.testing.CliRunner`，搭配既有 monkeypatch / fixture pattern。

## Non-Goals

- 不在第一階段做自然語言查詢或 LLM planning；CLI 只提供明確 command 與 filters。
- 不做 table、CSV、Markdown 等人類閱讀輸出；第一版先以 JSON 作為 agent-friendly contract。
- 不改 MCP tool 名稱或既有 MCP server 行為。
- 不做 live API smoke 作為預設測試；live tests 仍只放在 `just test-live`。

## Assumptions

- `ly` 這個 console script 名稱可以被此套件占用，且比 `lymcp` 更適合 terminal 查詢。
- Agents 會偏好穩定、可解析、完整的 JSON，而不是表格摘要。
- CLI command coverage 第一版應對齊現有 MCP tools，而不是只做少量 high-level shortcuts。

## Unknowns

- 是否需要 `ly prompts ...` 或 `ly workflows ...` 這類 command 來輸出 agent skill guidance；先在 README/skill 文件中描述 CLI usage，若 agents 需要可再新增。
- 是否要支援 `--jq` 或內建欄位投影；第一版只做 upstream `output_fields` 與 JSON output，避免引入額外 dependency 或自製查詢語法。

## Plan

- [ ] 新增 Typer dependency 與 console script：執行 `uv add typer`，在 `pyproject.toml` 加入 `ly = "lymcp.cli:app"`，並確認 `uv lock` 已更新；verify with `uv run ly --help` 可啟動且 `git diff -- pyproject.toml uv.lock` 只含預期 dependency/script 變更。
- [ ] 建立 `src/lymcp/cli.py` 的 root app、全域輸出 options 與 `ly stat` command，重用 `GetStatRequest().do()` 並輸出 JSON；verify with `uv run ly stat` against a monkeypatched offline test and `uv run ly --help` showing the root command.
- [ ] 建立 CLI 共用執行與輸出 helper，將 successful dict pretty-print 成 UTF-8 JSON，將 `LymcpApiError` 與 unexpected exceptions 轉為既有 JSON error envelope 與非零 exit code；verify with `uv run pytest -v -s tests/test_cli_mock.py -k error`.
- [ ] 實作第一組 list/get command groups：`bills`、`laws`、`meets`、`legislators`，每個 group 至少包含 `list` 與 `get`，並涵蓋常用 filters；verify with `CliRunner` tests asserting request class kwargs and JSON stdout for fixture-backed responses.
- [ ] 實作剩餘 command groups：`committees`、`gazettes`、`gazette-agendas`、`interpellations`、`ivods`、`law-versions`、`law-contents`，讓 CLI coverage 對齊所有 MCP tools；verify with a parametrized test comparing expected command inventory to the 39 existing tool-equivalent operations.
- [ ] 為 agent-friendly usage 補上 README CLI 區塊，包含安裝後 `ly --help`、三到五個穩定範例、JSON output contract、錯誤 envelope、以及 MCP tool 到 CLI command 的映射規則；verify with `rg -n "ly bills list|ly laws versions|JSON" README.md`.
- [ ] 若需要 agent skill 支援，新增或規劃 repo-local skill 文件，描述 command selection、date semantics、ID resolution workflow、以及何時改用 MCP tools；verify with skill file review or an explicit follow-up plan if repo does not yet want a skill in this PR.
- [ ] 增加 CLI offline tests 到 `tests/test_cli_mock.py`，覆蓋 help、success JSON、error JSON、required argument failures、list filters、detail positional IDs、`--compact` 或 `--output` 行為；verify with `uv run pytest -v -s tests/test_cli_mock.py`.
- [ ] 跑完整品質檢查，確認 CLI 變更沒有破壞 MCP server；verify with `just lint`, `just type`, and `just test`.

## Risks

- Command 數量接近 MCP tools，若一次手寫大量 Typer wiring 容易出現參數漏接或命名不一致；用 parametrized tests 與明確 command inventory 降低風險。
- Typer option 預設會把 snake_case 轉成 kebab-case，需在 README 與 tests 中固定使用 `--bill-type` 這類 kebab-case，避免 agent skills 產生錯誤指令。
- `output_fields` 是 list 參數，CLI UX 可能有 `--field A --field B` 與 `--fields A,B` 的取捨；第一版需選一種並寫入 docs/tests。
- 使用 `ly` 作為短 command 可能與使用者環境其他 binary 撞名；若發現衝突，保留 `lymcp` server script 並可考慮額外提供 `lymcp-cli` 作為 fallback。

## Rollback / Recovery

- 若 Typer CLI scope 過大，可保留 `typer` dependency 與 `ly stat` 作為最小可用 CLI，把完整 39-command coverage 拆成後續 PR。
- 若 `ly` 名稱衝突，回退 `pyproject.toml` 的 `ly` script，改用 `lymcp-cli`，不影響既有 `lymcp` MCP server script。
- 若 CLI tests 暴露 Request class 與 MCP wrapper 命名不一致，優先修 CLI mapping，不改既有 API request 或 MCP tools。

## Completion Checklist

- [ ] `ly` console script 可用，並由 `uv run ly --help` 與 `pyproject.toml` 的 `[project.scripts]` 證明。
- [ ] CLI commands 覆蓋既有 39 個 MCP tool-equivalent operations，並由 command inventory test 證明。
- [ ] CLI 成功輸出與失敗輸出都是 agent-friendly JSON，並由 `tests/test_cli_mock.py` success/error cases 證明。
- [ ] CLI 使用既有 `src/lymcp/api.py` request classes，且沒有新增第二套 HTTP client，並由 code review 或 targeted tests 證明。
- [ ] README 已記錄 `ly` 安裝與使用方式、範例 commands、輸出 contract 與日期/ID 查詢注意事項，並由 README diff 證明。
- [ ] 品質檢查 `just lint`, `just type`, and `just test` 全部通過。
