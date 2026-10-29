# CodeDrill

Practice SQL and Python in the browser with instant feedback. All code runs client-side: SQL in SQLite (sql.js) and Python in Pyodide, each inside a Web Worker. There is no backend.

- **Problems**: 500 SQL + 500 Python, ordered beginner to advanced (166 / 205 / 129 Easy / Medium / Hard in SQL, 166 / 211 / 123 in Python), filterable by track, difficulty, tag and status. Run against examples, submit against hidden tests, reveal hints one at a time, unlock the solution after solving or 3 failed submissions.
- **Lessons**: 8 per track, with editable runnable examples and 2 to 5 exercises each.
- **Playgrounds**: SQL with nine sample datasets and a schema browser; Python with stdout/stderr and on-demand numpy/pandas.
- **Daily challenge, streaks and an activity heatmap**; dashboard with "continue where you left off" and solved counts.
- **Progress** in `localStorage`, with JSON export/import.

See [`docs/SPEC.md`](docs/SPEC.md) for the product spec, [`CLAUDE.md`](CLAUDE.md) for architecture rules, and [`docs/DECISIONS.md`](docs/DECISIONS.md) for choices made along the way.

## Running it

Requires Node 20.9+ (tested on Node 22).

```bash
npm install          # also copies the SQLite wasm and builds the Python worker
npm run dev          # http://localhost:3000
```

| Command | What it does |
| --- | --- |
| `npm run dev` | Dev server |
| `npm run build` / `npm start` | Production build / serve it |
| `npm run lint` | ESLint (includes architecture guard rules) |
| `npx tsc --noEmit` | Type check |
| `npm run test` | Vitest unit tests |
| `npm run validate:content` | Validates all content and runs every reference solution against its tests |

The first visit to a Python page downloads Pyodide (~10 MB) from jsDelivr; the browser caches it afterwards. To self-host it, copy `node_modules/pyodide/*` to a public location and set `NEXT_PUBLIC_PYODIDE_BASE_URL` (for example `/pyodide/`) before building.

## Deploying to Vercel

1. Push the repo to GitHub and import it in Vercel (framework is detected as Next.js).
2. `vercel.json` runs `npm ci`, then `npm run validate:content && npm run build`, so broken content fails the deploy.
3. No environment variables are required. Optionally set `NEXT_PUBLIC_PYODIDE_BASE_URL` to self-host Pyodide.

Or from the CLI: `npx vercel` (preview) and `npx vercel --prod`.

## Project layout

```
app/                 routes (all statically generated)
components/          UI only: editor, problem, results, lesson, playground, dashboard, ui
lib/
  content/           zod schemas, file loader, snippet helpers
  runners/           Runner interface, WorkerRunner, sql/ and python/ engines + workers, registry
  judge/             result-set comparison, Python comparison, per-runner judges
  progress/          ProgressStore interface, LocalStorageProgressStore, streaks, heatmap, dates
  daily.ts           daily challenge selection
content/
  tracks/<id>.json
  datasets/<id>.json + <id>.sql
  problems/<track>/<slug>.json
  lessons/<track>/<nn-slug>.md
scripts/             validate-content.ts, build-workers.mjs, copy-wasm.mjs
tools/content-gen/   Python generators that produced the bulk problem set (see below)
tests/               Vitest suites
```

## Adding a problem

No code changes needed: add one JSON file, then run `npm run validate:content`.

**SQL** (`content/problems/sql/<slug>.json`; the file name must equal `slug`):

```json
{
  "slug": "cheap-products",
  "track": "sql",
  "title": "Cheap products",
  "difficulty": "Easy",
  "tags": ["where"],
  "statementMd": "List products cheaper than 20.\n\nExpected columns: `name`, `price`.",
  "hints": ["Use `WHERE price < 20`."],
  "solutionMd": "```sql\nSELECT name, price FROM products WHERE price < 20;\n```",
  "starterCode": "SELECT\n",
  "datasetId": "ecommerce",
  "expected": { "query": "SELECT name, price FROM products WHERE price < 20;", "orderMatters": false }
}
```

`expected.query` is the reference; the user's result is compared against it on the same fresh database. Use `setupSql` to add rows or tables for just this problem. If `orderMatters` is true, make sure the reference ordering has no ties.

**Python** (`content/problems/python/<slug>.json`):

```json
{
  "slug": "double-it",
  "track": "python",
  "title": "Double it",
  "difficulty": "Easy",
  "tags": ["basics"],
  "statementMd": "Return `n` times two.",
  "hints": ["Multiply by 2."],
  "solutionMd": "Multiply the argument by two.",
  "starterCode": "def double(n):\n    pass\n",
  "functionName": "double",
  "referenceSolution": "def double(n):\n    return n * 2\n",
  "tests": [
    { "args": [2], "expected": 4, "hidden": false },
    { "args": [-3], "expected": -6, "hidden": true }
  ]
}
```

`args` is the list of positional arguments. Return values are compared as JSON (tuples become lists, floats use a 1e-6 tolerance). Every problem needs at least one visible and one hidden test.

To use a problem as a lesson exercise, add its slug to a lesson's `exerciseSlugs`.

## Adding a lesson

Create `content/lessons/<track>/<nn-slug>.md`:

~~~markdown
---
id: views
title: Views
order: 9
datasetId: employees        # SQL lessons only: dataset for runnable snippets
exerciseSlugs: [high-earners, employee-departments]
---

Prose in Markdown. A fenced block tagged `sql-run` (or `python-run`) becomes an editable, runnable example:

```sql-run
SELECT * FROM employees LIMIT 3;
```
~~~

`validate:content` runs every snippet and fails if one errors.

## Adding a track

**On an existing runner** (say, "SQL interview prep" or "Python data structures"), it's content only:

1. Add `content/tracks/<id>.json` with `runnerId: "sql"` or `"python"`, an `editorLanguage`, and an `order`.
2. Add problems under `content/problems/<id>/` and lessons under `content/lessons/<id>/`.

**With a new language** (for example JavaScript):

1. Implement the engine and worker in `lib/runners/<lang>/` (the worker calls `serveRunner` from `lib/runners/worker-host.ts`), and a `create<Lang>Runner()` that returns a `WorkerRunner`.
2. Register it in `lib/runners/registry.ts`.
3. Add its problem schema to `problemSchemaByRunner` in `lib/content/schema.ts` and extend the `Problem` union.
4. Add a judge in `lib/judge/` and a case in `judgeProblem` (`lib/judge/index.ts`).
5. Add an executor for it in `scripts/validate-content.ts` so its reference solutions get verified.
6. Then add the track JSON and content as above. The UI (lists, editor, results, lessons, dashboard) is track-agnostic.

## Swapping the progress backend

Components only use the `ProgressStore` interface (`lib/progress/types.ts`) via `useProgress()`. A Supabase or other cloud store implements the same interface and is created in `lib/progress/ProgressProvider.tsx`.

## Bulk content generation

The 1,000 problems were authored in compact Python modules under `tools/content-gen/` and compiled to the JSON files in `content/problems/`. The generators *execute every reference solution* (SQLite for SQL, CPython for Python), so expected columns, rows and test values are never hand-typed, and they reject ambiguous problems (non-deterministic row order, empty results, duplicate tests, hard-codable tests, titles that collide).

```bash
cd tools/content-gen
python3 datasets.py      # regenerates content/datasets/{library,school,flights,music,bank,stocks}.{json,sql}
python3 build_sql.py     # sql/*.py  -> content/problems/sql/*.json
python3 build_py.py      # py/*.py   -> content/problems/python/*.json
cd ../.. && npm run validate:content
```

Each problem gets an `order` number (difficulty first, then a concept ladder such as select, where, group-by, join, window functions) that the problem list uses for the beginner to advanced progression. You do not need the generators to add problems by hand; they are only a faster way to author many at once. Note the generators rewrite every generated JSON file (not the original 50), so edit the `.py` source rather than the JSON for generated problems.
