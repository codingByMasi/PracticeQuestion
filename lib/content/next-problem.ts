import type { Lesson, ProblemSummary } from "./schema";

export type NextTarget = { href: string; label: string };

const difficultyRank = { Easy: 0, Medium: 1, Hard: 2 } as const;

function listOrder(a: ProblemSummary, b: ProblemSummary): number {
  return (
    (a.order ?? Number.MAX_SAFE_INTEGER) - (b.order ?? Number.MAX_SAFE_INTEGER) ||
    difficultyRank[a.difficulty] - difficultyRank[b.difficulty] ||
    a.title.localeCompare(b.title)
  );
}

/**
 * Where "Next" leads after a problem. Inside a lesson it walks the lesson's exercises, then the
 * next lesson's first exercise, then back to the track's lesson list. Problems that belong to
 * no lesson follow the problem-list order within their track.
 */
export function getNextTarget(problems: ProblemSummary[], lessons: Lesson[], slug: string): NextTarget | null {
  const current = problems.find((p) => p.slug === slug);
  if (!current) return null;

  const trackLessons = lessons.filter((l) => l.track === current.track).sort((a, b) => a.order - b.order);
  const lessonIndex = trackLessons.findIndex((l) => l.exerciseSlugs.includes(slug));
  const lesson = trackLessons[lessonIndex];
  if (lesson) {
    const next = lesson.exerciseSlugs[lesson.exerciseSlugs.indexOf(slug) + 1];
    if (next) return { href: `/problems/${next}`, label: "Next exercise" };
    const nextLesson = trackLessons[lessonIndex + 1];
    if (nextLesson) return { href: `/learn/${nextLesson.track}/${nextLesson.id}`, label: `Next lesson: ${nextLesson.title}` };
    return { href: `/learn/${current.track}`, label: "Back to lessons" };
  }

  const ordered = problems.filter((p) => p.track === current.track).sort(listOrder);
  const next = ordered[ordered.findIndex((p) => p.slug === slug) + 1];
  return next ? { href: `/problems/${next.slug}`, label: "Next problem" } : { href: "/problems", label: "Back to problems" };
}
