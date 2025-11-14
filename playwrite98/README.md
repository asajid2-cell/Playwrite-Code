# playwrite98

`playwrite98` is a local-first replacement for the Playwright MCP server. Instead of repeatedly calling MCP tools from an LLM, every browser interaction is described in a deterministic plan, executed entirely in code, and cached to disk for reuse. The design follows the upstream [`@playwright/mcp`](../playwright-mcp/README.md) contract but implements Anthropic's “98% in code” recommendation.

## Motivation

- **Token efficiency** – the model emits a single plan, and `playwrite98` executes the whole flow locally without incremental tool chatter.
- **Deterministic replay** – plans encode navigation, waits, assertions, and expected state; we can rerun the same steps at any time.
- **Artifacts as context** – snapshots, logs, and traces land in `artifacts/<runId>/`, so they can be shared in git instead of being trapped in a chat transcript.

## Architecture overview

```
plan.json ──▶ PlanLoader ──▶ ActionPlanner ──▶ ActionExecutor ──▶ Playwright
                 ▲                │                │                │
                 │                ▼                │                ▼
     SnapshotStore ◀──────────── EventBus ◀────────┴──▶ ResultWriter
```

1. **PlanLoader** – reads a JSON/YAML plan and validates it with Zod. Plans carry browser capabilities, env vars, and an ordered list of `ActionStep` items.
2. **ActionPlanner** – groups high-level macros (e.g., `loginUsingEnv`) into primitive steps so the executor can batch them.
3. **ActionExecutor** – drives a single Playwright browser context, emits deterministic artifacts, and minimizes observations (accessibility snapshots are reused via hashing).
4. **SnapshotStore** – caches snapshots keyed by URL + DOM hash so we can diff them or reuse them in future runs.
5. **ResultWriter** – persists logs, run summaries, and optional traces/PDFs for downstream inspection.

## Modules

| Path | Responsibility |
| --- | --- |
| `src/types/plan.ts` | Zod schemas and TypeScript types for plans, steps, and artifacts. |
| `src/actions/steps.ts` | Concrete implementations for each action type (navigate, click, fill, evaluate, assert, snapshot). |
| `src/actions/macros.ts` | Optional macros that expand shorthand instructions. |
| `src/snapshot/store.ts` | Accessibility snapshot capture, hashing, and disk persistence. |
| `src/orchestrator/session.ts` | Browser/context/page lifecycle plus capability flags (pdf/testing/tracing/media). |
| `src/orchestrator/executor.ts` | Plan runner that batches steps, stores outputs, and enforces “one request, many actions.” |
| `src/utils/logger.ts` | Structured logging helpers (JSON and pretty console). |
| `src/index.ts` | CLI entry point: `npx playwrite98 run plan.json --out artifacts/latest`. |

## Token reduction tactics

- **Action batching** – a single plan drives the entire UI flow; no per-step MCP tool usage.
- **Snapshot caching** – DOM state is hashed and stored locally; future runs can reuse context without reopening the page.
- **Deterministic waits** – post-conditions (role/name/selector) replace repeated “wait for selector” tool requests.
- **Script sandboxes** – `evaluate` steps let us inspect or mutate page state without serializing massive DOMs through the LM.
- **Artifact rehydration** – LMs read git-tracked artifacts instead of rerequesting screenshots.

## Implementation status

- [x] TypeScript project scaffold + CLI
- [x] Plan schema and executor
- [x] Snapshot store and logger
- [ ] Macro catalog (login, multi-input forms)
- [ ] Differential assertion helpers
- [ ] Snapshot-to-text explanation tooling

## Usage

```bash
cd playwrite98
npm install
npx tsx src/index.ts run plans/example.plan.json --out artifacts/run-001
```

Outputs:

- `artifacts/run-001/run.json` – per-step timings, errors, and artifact references.
- `artifacts/run-001/snapshots/` – cached accessibility trees + optional DOM dumps.
- `artifacts/run-001/log.ndjson` – (coming soon) structured event log for analysis.

## Next steps

1. Implement diff-based snapshot assertions so we can detect UI regressions without DOM re-capture.
2. Add `playwrite98 explain <snapshot>` to summarize cached trees for the LLM.
3. Integrate with the existing study/frontend suites so every UI PR runs deterministically in CI with zero MCP tool calls.
