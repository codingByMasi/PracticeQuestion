# Decisions

Choices made where the spec was silent or where reality forced a deviation. Newest concerns are grouped by area, not by date.

## Stack and build

1. **Next.js 16 (App Router, Turbopack), React 19, Tailwind v4, zod v4, Vitest.** Latest stable versions at build time.
2. **Every page is statically generated.** Content is read with `fs` at build time (`lib/content/loader.ts`, `server-only`), and problem/lesson routes use `generateStaticParams` with `dynamicParams = false`. Nothing needs a server at runtime, so Vercel serves static files plus the default Next runtime.
3. **The Python worker is bundled separately with esbuild** (`scripts/build-workers.mjs` → `public/workers/python.worker.js`, run on `predev`, `prebuild` and `postinstall`). Pyodide 314 refuses to run in classic workers, and the Next/Turbopack build emits classic workers even when `{ type: "module" }` is passed. The SQL worker has no such constraint and is bundled by Next (`new Worker(new URL("./sql.worker.ts", import.meta.url))`).
4. **Pyodide is pinned to 314.0.7** (`lib/runners/python/config.ts`) and loaded from `https://cdn.jsdelivr.net/pyodide/v314.0.7/full/`. `NEXT_PUBLIC_PYODIDE_BASE_URL` overrides the base URL for self-hosting. `validate:content` fails if the constant and the installed `pyodide` package drift apart.
5. **sql.js's WASM is copied to `public/vendor/sql-wasm.wasm`** on `postinstall` and served same-origin.
6. **Monaco loads from jsDelivr** (the `@monaco-editor/react` default). Custom `codedrill-light`/`codedrill-dark` themes raise comment contrast to WCAG AA.
7. **Theme:** `next-themes` with the `class` strategy, defaulting to the system preference.
8. **Lint guards the architecture:** ESLint forbids `localStorage` and direct `sql.js`/`pyodide`/engine/worker imports in `app/` and `components/`, plus `eval`/`new Function` everywhere.

## Runners

9. **Runner interface additions.** `getStatus()`/`onStatus()` drive loading indicators. `RunInput` is `{ code, setup?, harness?, echoLastExpression? }`; `RunResult` adds `stderr` and `cases` (per-test outcomes). One generic `WorkerRunner` implements the interface for any worker speaking `lib/runners/worker-protocol.ts`.
10. **Timeout semantics.** The 10 s limit covers execution only. Downloading the runtime (`init`) and on-demand packages like numpy/pandas (`prepare`) have a separate 120 s limit, so a slow first download isn't reported as an infinite loop. On timeout the worker is terminated and lazily recreated.
11. **Runs are serialized per runner** (a queue), so a schema query and a submission can't interleave.
12. **Engines are shared with Node.** `executeSql` and `executePython` are pure functions of a loaded runtime, used by both the browser workers and `validate:content`, so the validator judges exactly like the app.
13. **Python sandboxing (best effort).** Each run gets a fresh namespace with guarded builtins: importing `js`, `pyodide`, `pyodide_js`, `micropip` raises `ImportError`; `open()` in write/append mode raises `PermissionError`; `input()` raises. Output is capped at 64 KB. Pyodide's filesystem is an in-memory FS inside the worker, so it can't touch the user's disk anyway, and WASM has no sockets. This is not a security boundary against a determined user, who is only attacking their own browser.
14. **Test arguments are deep-copied** before each call, so mutating an argument can't affect later tests. Return values are converted to JSON (tuples → lists, sets → sorted lists, dict keys → strings, other objects → `repr`).
15. **Playground and lesson snippets echo the last expression** (REPL style). Problems don't.

## Judging

16. **SQL Run vs Submit.** Both run the user query and the reference query on identical fresh databases and compare. *Run* doesn't record an attempt and, when wrong, shows the expected result table as the "visible example". *Submit* records the attempt and shows only the diff. There are no separate hidden SQL datasets in v1.
17. **SQL comparison rules** (`lib/judge/sql-compare.ts`): column names compare case-insensitively; the same columns in a different order are accepted and realigned; numbers compare with relative tolerance 1e-6; `3` equals `3.0`, but a number never equals a numeric string; NULL only equals NULL; unordered results compare as multisets (both sides sorted). Diffs report the first of column mismatch, row-count mismatch, or first differing row.
18. **The SQL result is the last statement that returns rows**, so setup statements before a final `SELECT` work. A query that returns nothing is an error with a hint.
19. **Python Run uses visible tests, Submit uses all tests.** Hidden tests show pass/fail and, on error, only the exception's last line, never inputs or expected values.
20. **Hidden tests are hidden in the UI only.** With no server, problem files (including hidden tests and reference solutions) ship to the browser. Moving judging server-side later would fix this without content changes.
21. **Reference solution unlocks** after solving, or after 3 failed submissions (`SOLUTION_UNLOCK_FAILURES`).

## Content

22. **Python problems have an extra `referenceSolution` field** (code), since the spec's shape had no machine-checkable solution. `solutionMd` is the human explanation shown to learners.
23. **Problem schemas are selected by the track's `runnerId`** (`problemSchemaByRunner`), so a new track on an existing runner needs no code. The loader adds a `kind` discriminator for type-safe narrowing. Schemas are strict: unknown keys (typos) are errors.
24. **Datasets live in `content/datasets/<id>.json` (metadata) + `<id>.sql`** (schema and rows).
25. **Lessons**: optional `datasetId` in frontmatter for SQL snippets; runnable snippets are fenced blocks tagged `sql-run` / `python-run` (`<editorLanguage>-run`); lesson ids are unique per track and progress is keyed as `track/id`; `exerciseSlugs` must reference 2 to 5 problems from the same track.
26. **`validate:content` checks more than references:** schema and cross-references, every reference solution passes its own tests, starter code does *not* pass, every lesson snippet runs without error, and the Pyodide version matches.
27. **Python expected values were generated** by running each reference with CPython when authoring; `validate:content` re-verifies them in Pyodide.
28. **Content size:** 500 SQL problems (166 Easy, 205 Medium, 129 Hard) and 500 Python problems (166 Easy, 211 Medium, 123 Hard), 8 lessons per track, 9 datasets (employees, ecommerce, movies, plus library, school, flights, music, bank and stocks). The original 25 + 25 hand-written problems are kept unchanged.
29. **Bulk problems are generated, then checked.** `tools/content-gen` holds compact Python authoring modules; the builders run each reference in SQLite or CPython to derive expected columns and values, and reject empty results, non-deterministic row order (checked with `PRAGMA reverse_unordered_selects`), duplicate or constant tests, and colliding titles. The generated JSON is committed, so the app and `validate:content` never need Python. Hand-written problems still work by dropping in one JSON file.
30. **Beginner to advanced ordering via an optional `order` field** on problems (global per track, difficulty first, then a concept ladder). The problem list sorts by it, and shows 50 rows at a time with a Show more button, since 1,000 rows made the page heavy.
31. **Python tree problems take level-order lists** (`[3, 9, 20, None, None, 15, 7]`) because tests must be JSON; the reference solution contains the `build_tree` helper, and the statement says so.
32. **SQL problems never have an empty reference result.** sql.js returns no result set for a zero-row SELECT, which the judge treats as an error; the generator rejects such problems instead of changing the judge.

## Progress

33. **ProgressStore additions:** `getFailedAttempts`, `getActivityCounts` (heatmap), `getLastVisited`/`setLastVisited` (dashboard "continue"), `subscribe`/`getVersion` (React re-render via `useSyncExternalStore`). Storage is one JSON blob under `codedrill:progress`, validated with zod on read and import; corrupt data falls back to empty progress. Cross-tab changes are picked up via the `storage` event.
34. **Statuses** are `unsolved`, `attempted`, `solved`. The list's "Unsolved" filter includes attempted problems. Solved is sticky.
35. **Activity** = a submission (pass or fail) or a lesson completion, on the user's local date. Runs don't count.
36. **Streaks:** the current streak survives until the end of the day after the last active day (active yesterday but not yet today still counts). Longest is the longest consecutive run ever.
37. **Lesson completion** is an explicit "Mark lesson complete" button.
38. **Daily challenge:** FNV-1a hash of `codedrill:<YYYY-MM-DD>` modulo the number of problems (sorted by slug), using the user's **local** date, so everyone sees the same problem on the same calendar date. Adding problems reshuffles future picks, which is acceptable.
39. **Import replaces** all progress (after validation and a confirm dialog) rather than merging.
40. **Drafts** autosave 400 ms after the last keystroke and flush on `pagehide`. Playground drafts use keys `playground:sql:<dataset>` and `playground:python`.

## UX

41. **Split panes are a small custom component** (pointer and keyboard resizable, `role="separator"`), stacking vertically below the `lg` breakpoint: description, then editor, then results.
42. **Shortcuts:** Ctrl/⌘+Enter runs, Ctrl/⌘+Shift+Enter submits.
43. **Runtimes load lazily:** SQLite when a SQL problem/playground opens, Pyodide only on Python pages; lesson snippets load their runtime on first Run.
44. **Accessibility:** audited with axe-core (WCAG 2 A/AA) in light and dark mode; remaining findings are Monaco-internal (dimmed line numbers).

## Not done / limitations

45. **Not deployed.** Deploying needs the owner's Vercel account; `vercel.json` is ready.
46. **CDN URLs weren't reachable from the build sandbox**, so the browser tests served Monaco and Pyodide from local copies of the same versions. The jsDelivr URLs follow the documented pattern but weren't fetched live.
