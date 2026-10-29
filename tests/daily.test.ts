import { describe, expect, it } from "vitest";
import { fnv1a, pickDailyChallenge } from "@/lib/daily";
import { addDays } from "@/lib/progress/dates";

const pool = Array.from({ length: 50 }, (_, i) => `problem-${i}`);

describe("pickDailyChallenge", () => {
  it("returns null for an empty pool", () => {
    expect(pickDailyChallenge([], "2026-10-29")).toBeNull();
  });

  it("is deterministic for a date", () => {
    expect(pickDailyChallenge(pool, "2026-10-29")).toBe(pickDailyChallenge(pool, "2026-10-29"));
  });

  it("does not depend on pool order", () => {
    const shuffled = [...pool].reverse();
    expect(pickDailyChallenge(shuffled, "2026-10-29")).toBe(pickDailyChallenge(pool, "2026-10-29"));
  });

  it("always picks from the pool", () => {
    for (let i = 0; i < 100; i++) expect(pool).toContain(pickDailyChallenge(pool, addDays("2026-01-01", i)));
  });

  it("varies across days", () => {
    const picks = new Set(Array.from({ length: 60 }, (_, i) => pickDailyChallenge(pool, addDays("2026-01-01", i))));
    expect(picks.size).toBeGreaterThan(20);
  });

  it("uses a stable hash", () => {
    expect(fnv1a("")).toBe(0x811c9dc5);
    expect(fnv1a("a")).toBe(0xe40c292c);
  });
});
