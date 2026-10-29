# CodeDrill Product + Technical Spec

## 1. Goals
- Let learners practice SQL and Python in the browser with instant feedback.
- Zero server cost at launch; deployable as a static/edge site on Vercel.
- Extensible: new languages/tracks and new features (accounts, leaderboards) without rewrites.

## 2. Launch features (v1)
1. **Problem list + editor (LeetCode style)**
   - Filter by track (SQL/Python), difficulty (Easy/Medium/Hard), tag, status (unsolved/solved).
   - Problem page: description (Markdown), editor, Run button (runs against visible examples), Submit button (runs against hidden tests), results panel, hints (reveal one at a time), reference solution (unlocked after solving or after N failed attempts).
2. **Guided lessons + exercises**
   - Each track has ordered lessons (Markdown with embedded runnable snippets) followed by 2-5 exercises per lesson.
   - Lesson completion tracked; next/previous navigation; progress bar per track.
3. **Free playground**
   - SQL: choose a sample dataset (e.g., employees, ecommerce, movies), write queries, see tables with a schema browser sidebar.
   - Python: REPL-like editor with stdout/stderr display and common libs available (numpy, pandas loadable on demand via Pyodide with a loading indicator).
4. **Daily challenge + streaks**
   - One challenge per day chosen deterministically from the problem pool (hash of the date), same for all users.
   - Streak counter (current + longest), based on the user's local date. Calendar heatmap of activity.
5. **Dashboard/home**: continue where you left off, streak, daily challenge card, solved counts by difficulty and track.

## 3. Non-goals for v1
No login, no server, no payments, no social features, no AI hints. (Design so they can be added.)

## 4. Core abstractions

### Runner
```ts
interface Runner {
  id: "sql" | "python" | string
  init(): Promise<void>
  run(input: RunInput): Promise<RunResult>   // executes in a worker
  dispose(): void
}
type RunResult = {
  ok: boolean
  stdout?: string
  table?: { columns: string[]; rows: unknown[][] }
  error?: string
  durationMs: number
}
```

### Track
`{ id, title, description, runnerId, editorLanguage, order }`

### Problem (file: /content/problems/<track>/<slug>.json)
```
{
  slug, track, title, difficulty, tags[], statementMd, hints[], solutionMd,
  // SQL problems:
  datasetId, setupSql?, starterCode,
  expected: { query: "reference SQL", orderMatters: boolean },
  // Python problems:
  functionName, starterCode,
  tests: [{ args, expected, hidden: boolean }]
}
```

### Lesson (file: /content/lessons/<track>/<nn-slug>.md with frontmatter)
Frontmatter: id, title, order, exerciseSlugs[]

### ProgressStore
```ts
interface ProgressStore {
  getProblemStatus(slug): Status
  saveAttempt(slug, code, passed): void
  getLessonDone(id): boolean
  markLessonDone(id): void
  getActivityDates(): string[]
  getDraft(slug): string | null
  saveDraft(slug, code): void
  export(): string
  import(json: string): void
}
```
Launch implementation: `LocalStorageProgressStore`. Include Export/Import progress buttons (JSON) because localStorage is device-bound.

## 5. Judging logic
- **SQL:** run the user query and the reference query on the same SQLite DB, then compare result sets. Normalize column names case-insensitively, compare values with number tolerance, ignore row order unless orderMatters. Show a diff on failure (first mismatching row, column mismatch, row count mismatch).
- **Python:** run user code in the Pyodide worker, import the user's function by functionName, run each test case, capture stdout, compare to expected. Hidden tests show pass/fail only, not inputs. Timeout 10s per submission. Block network access and filesystem writes where feasible.
- Each run uses a fresh in-memory database built from the dataset, so destructive SQL (DROP, DELETE) never affects other runs.

## 6. Routes
- `/` dashboard
- `/problems` list + filters
- `/problems/[slug]` problem page
- `/learn` tracks overview
- `/learn/[track]` lesson list
- `/learn/[track]/[id]` lesson page
- `/playground/sql`
- `/playground/python`
- `/daily` today's challenge
- `/progress` stats, heatmap, export/import

## 7. UX requirements
- Split-pane layout (description | editor + results), resizable, keyboard shortcut Ctrl/Cmd+Enter to run.
- Loading states for Pyodide (about 10MB first load): show progress, rely on browser cache, load only when a Python page is opened.
- Autosave drafts per problem.
- Clean, minimal design; light/dark theme; accessible (keyboard nav, contrast).

## 8. Seed content (create for v1)
- SQL datasets: employees/departments, ecommerce (customers/orders/products), movies.
- SQL: 25 problems (SELECT/WHERE, ORDER BY, aggregates, GROUP BY/HAVING, JOINs, subqueries, CTEs, window functions) + 8 lessons.
- Python: 25 problems (basics, strings, lists/dicts, loops, functions, recursion, comprehensions, simple algorithms) + 8 lessons.
- Every problem must have a verified reference solution and tests. Add a script (`npm run validate:content`) that checks every problem's reference solution passes its own tests.

## 9. Extensibility (design for these, don't build)
- New tracks (Pandas, JavaScript, DSA, Bash) = new Runner + content folder.
- Supabase auth + cloud progress = new ProgressStore implementation.
- Leaderboards, AI hints, user-submitted problems, certificates.

## 10. Build phases
1. Project scaffold, theme, layout, content loader + zod schemas, ProgressStore, tests
2. SQL runner + problem page + judging + seed SQL content
3. Python runner + judging + seed Python content
4. Lessons and playgrounds
5. Dashboard, daily challenge, streaks, heatmap, export/import
6. Polish, accessibility, performance, README, deploy to Vercel
