# 🏛️ ly-mcp

[![PyPI version](https://img.shields.io/pypi/v/lymcp)](https://pypi.org/project/lymcp/)
[![Python](https://img.shields.io/pypi/pyversions/lymcp)](https://pypi.org/project/lymcp/)
[![CI](https://github.com/narumiruna/ly-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/narumiruna/ly-mcp/actions/workflows/ci.yml)
[![Docker](https://github.com/narumiruna/ly-mcp/actions/workflows/docker.yml/badge.svg)](https://github.com/narumiruna/ly-mcp/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ly-mcp 是一個串接台灣立法院 API v2 的 Model Context Protocol (MCP) 伺服器，提供議案、委員會、公報、會議紀錄與相關文件等資料查詢能力。

## ✨ 功能

此 MCP 伺服器提供 9 大類、共 39 個工具：

### 📊 統計

- **get_stat**：取得立法院 API 的統計與概覽資訊。

### 📄 議案

- **list_bills**：列出議案，可依屆期、會期、類別、提案人等條件篩選。
- **get_bill**：取得特定議案的完整資訊，回傳完整 JSON。
- **get_bill_related_bills**：查詢相關議案與其關聯。
- **get_bill_meets**：取得議案在各會議中的審議紀錄。
- **get_bill_doc_html**：取得特定議案的 HTML 文件內容。

### 🏢 委員會

- **list_committees**：列出立法院委員會，可搭配篩選條件。
- **get_committee**：取得特定委員會的詳細資訊。
- **get_committee_meets**：取得委員會會議紀錄與議事內容。

### 📰 公報

- **list_gazettes**：列出立法院公報，可依卷期與公報編號篩選。
- **get_gazette**：取得特定公報的詳細資訊。
- **get_gazette_agendas**：取得特定公報中的議程或目錄內容。
- **list_gazette_agendas**：列出公報目錄，可依屆期、會議日期等條件篩選。
- **get_gazette_agenda**：取得特定公報目錄項目的詳細資訊。

### 🎙️ 質詢

- **list_interpellations**：列出質詢資料，可依委員、屆期、會期與會議代碼篩選。
- **get_interpellation**：取得特定質詢的詳細資訊。
- **get_legislator_interpellations**：取得特定立法委員作為質詢委員的質詢資料。

### 🎥 IVOD（網路電視）

- **list_ivods**：列出 IVOD 影片，可依屆期、會期、委員會、委員與影片類型篩選。
- **get_ivod**：取得特定 IVOD 影片的詳細資訊，包含影片網址、逐字稿與公報內容。
- **get_meet_ivods**：取得特定會議相關的 IVOD 影片。

### ⚖️ 法律

- **list_laws**：列出法律，可依法律編號、類別（母法或子法）、母法編號、狀態與主管機關篩選。
- **get_law**：取得特定法律的完整資訊，包含基本資料、法條與版本資訊。
- **get_law_progress**：取得特定法律的未議決進度列表。
- **get_law_bills**：取得特定法律相關的議案，可搭配篩選條件。
- **get_law_versions**：取得特定法律的歷史版本紀錄，包含修正內容、提案人與進度。
- **list_law_versions**：跨法律列出法律版本，可依法律編號、版本編號、日期、動作、進度與現行版本狀態篩選。
- **get_law_version**：依版本 ID 取得特定法律版本的詳細資訊。
- **get_law_version_contents**：取得特定法律版本包含的法條內容。
- **list_law_contents**：列出法條內容，可依法律編號、版本 ID、條號、現行版狀態與版本追蹤篩選。
- **get_law_content**：依法條內容 ID 取得特定法條的詳細資訊。

### 🗓️ 會議

- **list_meets**：列出立法院會議，可依屆期、會期、會議種類、出席委員、日期、委員會代號與會議編號篩選。
- **get_meet**：依會議 ID 或代碼取得特定會議的詳細資訊。
- **get_meet_ivods**：取得特定會議相關的 IVOD 影片，可搭配篩選條件。
- **get_meet_bills**：取得特定會議討論的議案，可依議案條件篩選。
- **get_meet_interpellations**：取得特定會議中的質詢資料，可搭配篩選條件。

### 👤 立法委員

- **list_legislators**：列出立法委員，可依屆期、黨籍、選區、委員 ID 與姓名篩選。
- **get_legislator**：依屆期與姓名取得特定立法委員的詳細資訊。
- **get_legislator_propose_bills**：取得特定立法委員作為提案人的議案，可依議案條件篩選。
- **get_legislator_cosign_bills**：取得特定立法委員作為連署人的議案，可依議案條件篩選。
- **get_legislator_meets**：取得特定立法委員出席的會議，可依會議條件篩選。
- **get_legislator_interpellations**：取得特定立法委員的質詢資料，可搭配篩選條件。

## 🔗 API 來源

此 MCP 伺服器使用 [立法院 API v2](https://ly.govapi.tw/v2) 作為資料來源，提供台灣立法院議案與議事資料。

## 📦 工具回應格式

MCP 工具呼叫成功時，會回傳立法院 API 的原始 JSON payload。呼叫失敗時，會回傳可由程式判讀的 JSON 錯誤封包：

```json
{
  "ok": false,
  "error": {
    "type": "http_status",
    "message": "Upstream API returned HTTP 404 for https://ly.govapi.tw/v2/bills/invalid_bill_number",
    "url": "https://ly.govapi.tw/v2/bills/invalid_bill_number",
    "status_code": 404,
    "response_excerpt": "not found"
  }
}
```

目前的錯誤 `type` 包含 `http_status`、`timeout`、`network_error`、`invalid_json` 與 `unexpected_error`。

## 🚀 安裝與使用

### ⚡ 快速開始

使用 `uvx` 安裝並執行伺服器：

```bash
uvx lymcp@latest
```

### 🧩 MCP Client 設定

將此伺服器加入你的 MCP client 設定，例如 Claude Desktop。

#### PyPI

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uvx",
      "args": ["lymcp@latest"]
    }
  }
}
```

#### GitHub

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/ly-mcp",
        "lymcp"
      ]
    }
  }
}
```

#### 本機開發

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/ly-mcp",
        "lymcp"
      ]
    }
  }
}
```

#### Docker

```json
{
  "mcpServers": {
    "lymcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "narumi/ly-mcp:latest"
      ]
    }
  }
}
```

## 💬 範例提示

連上 MCP 伺服器後，可以向 LLM 提出這類問題：

- 「列出第11屆的所有法律提案」
- 「查詢立法委員王美花的提案紀錄」
- 「以今天的台北日期為準，最近已發生的院會討論了哪些議案？」
- 「下一場已排程的院會是什麼時候？」
- 「查詢勞動基準法的修法歷程」
- 「第11屆第1會期有哪些委員會會議？」

處理和日期有關的問題時，請區分：

- `latest known`：使用上游預設排序，包含未來已排程的紀錄。
- `latest occurred`：只考慮相關日期在參考日期當天或之前的紀錄。
- `next scheduled`：只考慮相關日期晚於參考日期的紀錄。

伺服器也提供常見工作流程用的 MCP prompts：
`latest_plenary_meeting_bills`、`law_amendment_history`、
`legislator_proposal_record`、`legislator_interpellations` 與
`committee_meeting_lookup`。可閱讀 `lymcp://query-semantics` 與
`lymcp://workflow-reference`，取得日期語意、篩選條件、ID 欄位與工作流程步驟的精簡指引。

## 🛠️ 開發

### ✅ 需求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 套件管理器
- [just](https://github.com/casey/just) 命令執行器

### ⚙️ 設定

```bash
git clone https://github.com/narumiruna/ly-mcp
cd ly-mcp
uv sync
```

### 🤖 使用 Codex CLI

此 repository 已包含供本機 Codex CLI 開發使用的 `.codex/config.toml`。從 repository root 啟動 Codex CLI 時，可透過 `uv run lymcp` 使用已設定的 `lymcp` MCP server。

### 🔍 執行 MCP Inspector

```bash
just dev
```

### 🧪 執行測試

```bash
# 執行預設離線測試套件並產生 coverage
just test

# 直接執行預設離線測試套件
uv run pytest -v -s

# 手動執行會呼叫立法院 API 的 live tests
just test-live
```

預設 pytest 設定會排除標記為 `live` 的測試，因此 CI 與一般本機執行會使用 `tests/data` 中的 fixture-backed samples。只有在上游 API 回應形狀改變時，才應有意識地更新這些 JSON samples。

### 🧹 程式碼品質

```bash
# 執行 linter
just lint

# 執行 type checker
just type
```

## 📜 授權

MIT
