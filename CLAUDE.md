# CodeDrill: SQL + Python practice platform

## What this is
A browser-based practice site for SQL and Python. All code runs client-side (no backend at launch). The platform will grow into more tracks later (Pandas, DSA, JavaScript, etc.), so every feature must be built around a generic "track" abstraction, never hardcoded to SQL or Python.

## Stack
- Next.js (App Router) + TypeScript (strict) + Tailwind CSS
- Monaco Editor (@monaco-editor/react) for code editing
- Pyodide (loaded lazily from CDN) running inside a Web Worker for Python
- sql.js (SQLite WASM) running inside a Web Worker for SQL
- localStorage for progress, behind a ProgressStore interface (Supabase may replace it later)
- Content stored as files in /content (JSON + Markdown), not in a database

## Architecture rules
1. Runners: every language implements a `Runner` interface (see docs/SPEC.md). UI code never imports Pyodide or sql.js directly.
2. Execution always happens in a Web Worker with a timeout (default 10s). On timeout, terminate and recreate the worker.
3. Storage: all progress access goes through `ProgressStore`. No direct localStorage calls in components.
4. Content: tracks, lessons, and problems are loaded from /content via a typed loader with schema validation (zod). Adding a new problem must require zero code changes.
5. Keep components small. Put logic in /lib, UI in /components, routes in /app.
6. Never run user code on the main thread. Never use eval.

## Conventions
- TypeScript strict, no `any`
- Tailwind only, no CSS files except globals.css
- Dark mode supported from day one
- Mobile-responsive (editor stacks above results on small screens)
- Write unit tests (Vitest) for: result-set comparison, streak logic, daily-challenge selection, content validation
- After each phase: run lint, typecheck, tests, and build. Fix before moving on.

## Commands
- dev: npm run dev
- test: npm run test
- lint: npm run lint
- typecheck: npx tsc --noEmit
- build: npm run build
- validate content: npm run validate:content
