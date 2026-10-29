"use client";

import Link from "next/link";
import { useEffect } from "react";
import type { Components } from "react-markdown";
import { Button } from "@/components/ui/Button";
import { DifficultyBadge } from "@/components/ui/Badge";
import { Markdown } from "@/components/ui/Markdown";
import { lessonKey, type ProblemSummary } from "@/lib/content/schema";
import { RUNNABLE_SUFFIX, runnerForLanguage } from "@/lib/content/snippets";
import { useProgress } from "@/lib/progress/ProgressProvider";
import { RunnableSnippet } from "./RunnableSnippet";

type LessonLink = { id: string; title: string } | null;

type Props = {
  track: { id: string; title: string; runnerId: string; editorLanguage: string };
  tracks: { runnerId: string; editorLanguage: string }[];
  lesson: { id: string; title: string; order: number; bodyMd: string };
  total: number;
  datasetSql?: string;
  exercises: ProblemSummary[];
  prev: LessonLink;
  next: LessonLink;
};

export function LessonView({ track, tracks, lesson, total, datasetSql, exercises, prev, next }: Props) {
  const { store, ready } = useProgress();
  const key = lessonKey(track.id, lesson.id);
  const done = ready && store.getLessonDone(key);

  useEffect(() => {
    store.setLastVisited(`/learn/${track.id}/${lesson.id}`, `${track.title}: ${lesson.title}`);
  }, [store, track.id, track.title, lesson.id, lesson.title]);

  const components: Components = {
    pre({ children, node }) {
      const codeEl = node?.children[0];
      const className = codeEl && codeEl.type === "element" ? String((codeEl.properties.className as string[] | undefined)?.[0] ?? "") : "";
      const lang = className.replace(/^language-/, "");
      if (lang.endsWith(RUNNABLE_SUFFIX) && codeEl && codeEl.type === "element") {
        const language = lang.slice(0, -RUNNABLE_SUFFIX.length);
        const runnerId = runnerForLanguage(language, tracks);
        const text = codeEl.children.map((c) => (c.type === "text" ? c.value : "")).join("").replace(/\n$/, "");
        if (runnerId)
          return <RunnableSnippet code={text} runnerId={runnerId} language={language} setup={runnerId === "sql" ? datasetSql : undefined} />;
      }
      return <pre>{children}</pre>;
    },
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <nav aria-label="Breadcrumb" className="text-sm text-zinc-500 dark:text-zinc-400">
        <Link href="/learn" className="hover:underline">
          Learn
        </Link>{" "}
        /{" "}
        <Link href={`/learn/${track.id}`} className="hover:underline">
          {track.title}
        </Link>
      </nav>
      <p className="mt-4 text-sm font-medium text-indigo-600 dark:text-indigo-400">
        Lesson {lesson.order} of {total}
      </p>
      <h1 className="mt-1 text-3xl font-bold tracking-tight">{lesson.title}</h1>

      <Markdown className="mt-6" components={components}>
        {lesson.bodyMd}
      </Markdown>

      <section aria-labelledby="exercises-h" className="mt-10 space-y-3">
        <h2 id="exercises-h" className="text-xl font-semibold">
          Exercises
        </h2>
        <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
          {exercises.map((p) => {
            const solved = ready && store.getProblemStatus(p.slug) === "solved";
            return (
              <li key={p.slug} className="flex items-center gap-3 px-4 py-3">
                <span className={solved ? "text-emerald-600 dark:text-emerald-400" : "text-zinc-300 dark:text-zinc-700"} aria-hidden="true">
                  ✓
                </span>
                <Link href={`/problems/${p.slug}`} className="font-medium hover:text-indigo-600 hover:underline dark:hover:text-indigo-400">
                  {p.title}
                </Link>
                <span className="sr-only">{solved ? "(solved)" : "(not solved)"}</span>
                <span className="ml-auto">
                  <DifficultyBadge difficulty={p.difficulty} />
                </span>
              </li>
            );
          })}
        </ul>
      </section>

      <div className="mt-8 flex flex-wrap items-center gap-3">
        {done ? (
          <p className="font-medium text-emerald-600 dark:text-emerald-400">✓ Lesson complete</p>
        ) : (
          <Button variant="primary" onClick={() => store.markLessonDone(key)} disabled={!ready}>
            Mark lesson complete
          </Button>
        )}
      </div>

      <nav aria-label="Lesson navigation" className="mt-8 flex justify-between gap-4 border-t border-zinc-200 pt-6 text-sm dark:border-zinc-800">
        {prev ? (
          <Link href={`/learn/${track.id}/${prev.id}`} className="hover:underline">
            ← {prev.title}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link href={`/learn/${track.id}/${next.id}`} className="text-right hover:underline">
            {next.title} →
          </Link>
        ) : (
          <Link href={`/learn/${track.id}`} className="hover:underline">
            Back to {track.title} lessons
          </Link>
        )}
      </nav>
    </div>
  );
}
