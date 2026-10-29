import { dayNumber, isDateKey } from "./dates";

export type Streak = { current: number; longest: number };

/**
 * Current and longest run of consecutive active days. The current streak stays
 * alive through `today` if the user was active yesterday but not yet today.
 */
export function computeStreak(activityDates: readonly string[], today: string): Streak {
  const days = [...new Set(activityDates.filter(isDateKey).map(dayNumber))].sort((a, b) => a - b);
  let longest = 0;
  let run = 0;
  let prev: number | undefined;
  for (const d of days) {
    run = prev !== undefined && d === prev + 1 ? run + 1 : 1;
    longest = Math.max(longest, run);
    prev = d;
  }

  const set = new Set(days);
  const t = dayNumber(today);
  let cursor = set.has(t) ? t : set.has(t - 1) ? t - 1 : undefined;
  let current = 0;
  while (cursor !== undefined && set.has(cursor)) {
    current++;
    cursor--;
  }
  return { current, longest };
}
