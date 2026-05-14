---
name: ly
description: Use when answering Taiwan Legislative Yuan data requests with the `ly` CLI, including bills, laws, meetings, legislators, committees, gazettes, interpellations, IVOD recordings, amendment history, proposal records, and meeting agendas. Trigger when a user asks for Legislative Yuan information that maps to `ly bills`, `ly laws`, `ly meets`, `ly legislators`, `ly committees`, `ly gazettes`, `ly interpellations`, or `ly ivods`, and Codex should run the CLI and summarize the JSON result.
---

# ly

## Overview

Use `ly` to query Taiwan Legislative Yuan API v2 from the terminal and summarize the result for the user.

Prefer running the CLI over guessing from memory. The CLI returns JSON by default, so inspect the fields you need and synthesize a concise answer instead of dumping the full payload unless the user asks for raw output.

## Installation

If `ly` is not available, install it with:

```bash
uv tool install lymcp
```

## Command Selection

- Run `ly ...` directly when the command is installed.
- If `ly` is missing, install it with `uv tool install lymcp`, then retry the same `ly ...` command.
- If installation fails because `uv` is missing, network access is restricted, package resolution fails, or the published version does not include `ly`, report the prerequisite clearly.

## Command Map

- Use `stat` for API statistics.
- Use `bills list` to find bills by term, session, bill type, proposer, date, status, law number, or other bill filters.
- Use `bills get BILL_NO` after a bill number is known.
- Use `bills related BILL_NO`, `bills meets BILL_NO`, and `bills doc-html BILL_NO` for related bills, deliberation records, and bill document HTML.
- Use `laws list` to resolve a law number or law ID from a law name, category, status, authority, or latest version date.
- Use `laws get LAW_ID`, `laws progress LAW_ID`, `laws bills LAW_ID`, and `laws versions LAW_ID` after a law ID is known.
- Use `law-versions list`, `law-versions get LAW_VERSION_ID`, and `law-versions contents LAW_VERSION_ID` for amendment/version workflows.
- Use `law-contents list` and `law-contents get LAW_CONTENT_ID` for article text and article-level lookups.
- Use `meets list` for meeting discovery by term, session, meeting type, date, committee code, attendee, or meeting ID.
- Use `meets get MEET_ID`, `meets bills MEET_ID`, `meets interpellations MEET_ID`, and `meets ivods MEET_ID` after a meeting ID is known.
- Use `legislators list` to resolve legislators by term, party, district, ID, or name.
- Use `legislators get TERM NAME`, `legislators propose-bills TERM NAME`, `legislators cosign-bills TERM NAME`, `legislators meets TERM NAME`, and `legislators interpellations TERM NAME` for legislator-scoped workflows.
- Use `committees list`, `committees get COMT_CD`, and `committees meets COMT_CD` for committee workflows.
- Use `gazettes list`, `gazettes get GAZETTE_ID`, `gazettes agendas GAZETTE_ID`, `gazette-agendas list`, and `gazette-agendas get GAZETTE_AGENDA_ID` for gazette workflows.
- Use `interpellations list` and `interpellations get INTERPELLATION_ID` for interpellation workflows.
- Use `ivods list` and `ivods get IVOD_ID` for Legislative Yuan video records.

## Query Workflow

1. Choose the narrowest command group from the user's domain: bills, laws, meets, legislators, committees, gazettes, interpellations, or IVODs.
2. If the user gives a name but the CLI command needs an ID, run the relevant `list` command first with narrow filters and a small `--limit`.
3. Use IDs returned by list commands in detail or nested-resource commands.
4. For date-sensitive meeting questions, compare Asia/Taipei dates:
   - `latest known`: use upstream ordering and do not remove scheduled future records.
   - `latest occurred`: only use records whose relevant date is on or before the reference date.
   - `next scheduled`: only use records whose relevant date is after the reference date.
5. Use `--fields` to request upstream output fields when you need a smaller payload.
6. Use `--compact` when piping JSON to another tool. Use `--output PATH` when saving a successful response to a file.
7. Summarize the result in the user's language. Include the exact command when reproducibility helps.

## Output And Error Handling

- Successful CLI calls print JSON to stdout.
- Failed API calls print a JSON error envelope to stderr and exit non-zero.
- Do not invent unsupported flags or commands. Run `ly --help` or `ly <group> <command> --help` when unsure.
- If a command returns no useful records, report that result and show which filters were used. Do not broaden filters silently unless the user asked for exploration.

## Examples

- "列出第 11 屆法律案" -> `ly bills list --term 11 --bill-type 法律案 --limit 10`
- "查勞動基準法修法歷程" -> `ly laws list --fields 法律編號,名稱 --limit 10`, then `ly laws versions LAW_ID --limit 20`
- "最近已發生的院會討論哪些議案？" -> `ly meets list --meeting-type 院會 --term 11 --limit 20`, choose the latest occurred meeting by date, then `ly meets bills MEET_ID --limit 50`
- "查韓國瑜提案紀錄" -> `ly legislators propose-bills 11 韓國瑜 --limit 20`
- "查某委員會會議" -> `ly committees list --fields 委員會代號,委員會名稱`, then `ly committees meets COMT_CD --term 11 --limit 20`
