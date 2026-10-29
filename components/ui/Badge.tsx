import type { Difficulty } from "@/lib/content/schema";

const COLORS: Record<Difficulty, string> = {
  Easy: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300",
  Medium: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300",
  Hard: "bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300",
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  return <span className={`inline-block rounded px-2 py-0.5 text-xs font-medium ${COLORS[difficulty]}`}>{difficulty}</span>;
}

export function Tag({ children }: { children: string }) {
  return (
    <span className="inline-block rounded bg-zinc-100 px-2 py-0.5 text-xs text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">{children}</span>
  );
}
