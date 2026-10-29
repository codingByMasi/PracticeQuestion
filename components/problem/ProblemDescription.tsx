"use client";

import { useState } from "react";
import type { Problem } from "@/lib/content/schema";
import { DifficultyBadge, Tag } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Markdown } from "@/components/ui/Markdown";
import { formatPython } from "@/lib/judge/python-compare";
import type { Status } from "@/lib/progress/types";

export const SOLUTION_UNLOCK_FAILURES = 3;

type Props = {
  problem: Problem;
  status: Status;
  failedAttempts: number;
  schema?: React.ReactNode;
};

export function ProblemDescription({ problem, status, failedAttempts, schema }: Props) {
  const [hintsShown, setHintsShown] = useState(0);
  const [showSolution, setShowSolution] = useState(false);
  const unlocked = status === "solved" || failedAttempts >= SOLUTION_UNLOCK_FAILURES;
  const remaining = Math.max(0, SOLUTION_UNLOCK_FAILURES - failedAttempts);

  return (
    <article className="h-full space-y-5 overflow-auto p-4">
      <header className="space-y-2">
        <h1 className="text-xl font-bold">{problem.title}</h1>
        <div className="flex flex-wrap items-center gap-2">
          <DifficultyBadge difficulty={problem.difficulty} />
          {problem.tags.map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
          {status === "solved" && <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">✓ Solved</span>}
        </div>
      </header>

      <Markdown>{problem.statementMd}</Markdown>

      {problem.kind === "python" && (
        <section aria-labelledby="examples-h" className="space-y-2">
          <h2 id="examples-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Examples
          </h2>
          {problem.tests
            .filter((t) => !t.hidden)
            .map((t, i) => (
              <pre key={i} tabIndex={0} className="overflow-auto rounded bg-zinc-100 p-2 font-mono text-xs dark:bg-zinc-900">
                {`>>> ${problem.functionName}(${t.args.map(formatPython).join(", ")})\n${formatPython(t.expected)}`}
              </pre>
            ))}
        </section>
      )}

      {schema && (
        <section aria-labelledby="schema-h" className="space-y-2">
          <h2 id="schema-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Schema
          </h2>
          {schema}
        </section>
      )}

      {problem.hints.length > 0 && (
        <section aria-labelledby="hints-h" className="space-y-2">
          <h2 id="hints-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Hints
          </h2>
          <ol className="list-decimal space-y-1 pl-5 text-sm">
            {problem.hints.slice(0, hintsShown).map((h, i) => (
              <li key={i}>
                <Markdown className="prose-sm">{h}</Markdown>
              </li>
            ))}
          </ol>
          {hintsShown < problem.hints.length && (
            <Button onClick={() => setHintsShown((n) => n + 1)}>
              Show hint {hintsShown + 1} of {problem.hints.length}
            </Button>
          )}
        </section>
      )}

      <section aria-labelledby="solution-h" className="space-y-2">
        <h2 id="solution-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
          Solution
        </h2>
        {!unlocked ? (
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            🔒 Unlocks after you solve the problem or after {remaining} more failed submission{remaining === 1 ? "" : "s"}.
          </p>
        ) : showSolution ? (
          <Markdown>{problem.solutionMd}</Markdown>
        ) : (
          <Button onClick={() => setShowSolution(true)}>Reveal solution</Button>
        )}
      </section>
    </article>
  );
}
