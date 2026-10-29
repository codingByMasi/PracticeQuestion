import { z } from "zod";
import { toLocalDateKey } from "./dates";
import type { LastVisited, ProgressStore, Status } from "./types";

export type StorageLike = Pick<Storage, "getItem" | "setItem">;

export const STORAGE_KEY = "codedrill:progress";

const ProblemRecordSchema = z.object({
  status: z.enum(["unsolved", "attempted", "solved"]),
  attempts: z.number().int().nonnegative(),
  failedAttempts: z.number().int().nonnegative(),
  solvedAt: z.string().optional(),
  lastAttemptAt: z.string().optional(),
  lastCode: z.string().optional(),
});

const ProgressDataSchema = z.object({
  version: z.literal(1),
  problems: z.record(z.string(), ProblemRecordSchema),
  lessons: z.record(z.string(), z.string()),
  activity: z.record(z.string().regex(/^\d{4}-\d{2}-\d{2}$/), z.number().int().nonnegative()),
  drafts: z.record(z.string(), z.string()),
  lastVisited: z.object({ href: z.string(), title: z.string(), at: z.string() }).nullable(),
});
export type ProgressData = z.infer<typeof ProgressDataSchema>;

function emptyData(): ProgressData {
  return { version: 1, problems: {}, lessons: {}, activity: {}, drafts: {}, lastVisited: null };
}

export function parseProgress(json: string): ProgressData {
  return ProgressDataSchema.parse(JSON.parse(json));
}

export class LocalStorageProgressStore implements ProgressStore {
  private data: ProgressData;
  private version = 0;
  private listeners = new Set<() => void>();

  constructor(
    private readonly storage: StorageLike,
    private readonly now: () => Date = () => new Date(),
  ) {
    this.data = this.read();
  }

  private read(): ProgressData {
    try {
      const raw = this.storage.getItem(STORAGE_KEY);
      return raw ? parseProgress(raw) : emptyData();
    } catch {
      return emptyData();
    }
  }

  private commit(): void {
    try {
      this.storage.setItem(STORAGE_KEY, JSON.stringify(this.data));
    } catch {
      // Quota exceeded or storage disabled: keep working in memory.
    }
    this.notify();
  }

  private notify(): void {
    this.version++;
    for (const l of this.listeners) l();
  }

  /** Re-read storage (e.g. after another tab changed it). */
  reload(): void {
    this.data = this.read();
    this.notify();
  }

  private recordActivity(): void {
    const key = toLocalDateKey(this.now());
    this.data.activity[key] = (this.data.activity[key] ?? 0) + 1;
  }

  getProblemStatus(slug: string): Status {
    return this.data.problems[slug]?.status ?? "unsolved";
  }

  getFailedAttempts(slug: string): number {
    return this.data.problems[slug]?.failedAttempts ?? 0;
  }

  saveAttempt(slug: string, code: string, passed: boolean): void {
    const at = this.now().toISOString();
    const prev = this.data.problems[slug] ?? { status: "unsolved", attempts: 0, failedAttempts: 0 };
    const solved = prev.status === "solved" || passed;
    this.data.problems[slug] = {
      ...prev,
      status: solved ? "solved" : "attempted",
      attempts: prev.attempts + 1,
      failedAttempts: prev.failedAttempts + (passed ? 0 : 1),
      lastAttemptAt: at,
      lastCode: code,
      solvedAt: prev.solvedAt ?? (passed ? at : undefined),
    };
    this.recordActivity();
    this.commit();
  }

  getLessonDone(id: string): boolean {
    return id in this.data.lessons;
  }

  markLessonDone(id: string): void {
    if (this.getLessonDone(id)) return;
    this.data.lessons[id] = this.now().toISOString();
    this.recordActivity();
    this.commit();
  }

  getActivityDates(): string[] {
    return Object.keys(this.data.activity).sort();
  }

  getActivityCounts(): Record<string, number> {
    return { ...this.data.activity };
  }

  getDraft(slug: string): string | null {
    return this.data.drafts[slug] ?? null;
  }

  saveDraft(slug: string, code: string): void {
    if (this.data.drafts[slug] === code) return;
    this.data.drafts[slug] = code;
    this.commit();
  }

  getLastVisited(): LastVisited | null {
    return this.data.lastVisited;
  }

  setLastVisited(href: string, title: string): void {
    if (this.data.lastVisited?.href === href) return;
    this.data.lastVisited = { href, title, at: this.now().toISOString() };
    this.commit();
  }

  export(): string {
    return JSON.stringify(this.data, null, 2);
  }

  import(json: string): void {
    this.data = parseProgress(json);
    this.commit();
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getVersion(): number {
    return this.version;
  }
}

/** In-memory Storage, used during server rendering and in tests. */
export class MemoryStorage implements StorageLike {
  private map = new Map<string, string>();
  getItem(key: string): string | null {
    return this.map.get(key) ?? null;
  }
  setItem(key: string, value: string): void {
    this.map.set(key, value);
  }
}
