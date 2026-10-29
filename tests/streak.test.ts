import { describe, expect, it } from "vitest";
import { computeStreak } from "@/lib/progress/streak";
import { addDays, toLocalDateKey } from "@/lib/progress/dates";

describe("computeStreak", () => {
  it("is zero with no activity", () => {
    expect(computeStreak([], "2026-03-10")).toEqual({ current: 0, longest: 0 });
  });

  it("counts consecutive days ending today", () => {
    expect(computeStreak(["2026-03-08", "2026-03-09", "2026-03-10"], "2026-03-10")).toEqual({ current: 3, longest: 3 });
  });

  it("keeps the streak alive when the last activity was yesterday", () => {
    expect(computeStreak(["2026-03-08", "2026-03-09"], "2026-03-10")).toEqual({ current: 2, longest: 2 });
  });

  it("resets after a missed day", () => {
    expect(computeStreak(["2026-03-07", "2026-03-08"], "2026-03-10")).toEqual({ current: 0, longest: 2 });
  });

  it("tracks the longest run separately from the current one", () => {
    const dates = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-03-09", "2026-03-10"];
    expect(computeStreak(dates, "2026-03-10")).toEqual({ current: 2, longest: 4 });
  });

  it("ignores duplicates, ordering and invalid keys", () => {
    const dates = ["2026-03-10", "2026-03-09", "2026-03-10", "garbage", "2026-02-30"];
    expect(computeStreak(dates, "2026-03-10")).toEqual({ current: 2, longest: 2 });
  });

  it("crosses month, year and leap-day boundaries", () => {
    expect(computeStreak(["2025-12-31", "2026-01-01"], "2026-01-01").current).toBe(2);
    expect(computeStreak(["2028-02-28", "2028-02-29", "2028-03-01"], "2028-03-01").current).toBe(3);
  });

  it("works across a DST change", () => {
    // US DST started 2026-03-08; calendar arithmetic must not drift.
    expect(computeStreak(["2026-03-07", "2026-03-08", "2026-03-09"], "2026-03-09").current).toBe(3);
  });
});

describe("date helpers", () => {
  it("adds days on calendar keys", () => {
    expect(addDays("2026-02-28", 1)).toBe("2026-03-01");
    expect(addDays("2026-01-01", -1)).toBe("2025-12-31");
  });
  it("formats local dates", () => {
    expect(toLocalDateKey(new Date(2026, 0, 5, 23, 59))).toBe("2026-01-05");
  });
});
