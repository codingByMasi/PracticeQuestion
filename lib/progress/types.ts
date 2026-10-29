export type Status = "unsolved" | "attempted" | "solved";

export type LastVisited = { href: string; title: string; at: string };

/**
 * All progress access goes through this interface. The launch implementation is
 * LocalStorageProgressStore; a cloud-backed store can implement the same API.
 */
export interface ProgressStore {
  getProblemStatus(slug: string): Status;
  /** Number of failed submissions (used to unlock the reference solution). */
  getFailedAttempts(slug: string): number;
  saveAttempt(slug: string, code: string, passed: boolean): void;
  getLessonDone(id: string): boolean;
  markLessonDone(id: string): void;
  /** Local dates (YYYY-MM-DD) with any activity, ascending. */
  getActivityDates(): string[];
  /** Activity count per local date. */
  getActivityCounts(): Record<string, number>;
  getDraft(slug: string): string | null;
  saveDraft(slug: string, code: string): void;
  getLastVisited(): LastVisited | null;
  setLastVisited(href: string, title: string): void;
  export(): string;
  /** Replaces all progress with the given export. Throws on invalid input. */
  import(json: string): void;
  /** Subscribe to changes; returns an unsubscribe function. */
  subscribe(listener: () => void): () => void;
  /** Monotonic counter that changes whenever data changes. */
  getVersion(): number;
}
