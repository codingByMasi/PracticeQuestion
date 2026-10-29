"use client";

import { useMemo } from "react";
import { toLocalDateKey } from "./dates";
import { useProgress } from "./ProgressProvider";
import { computeStreak, type Streak } from "./streak";

export function useStreak(): Streak {
  const { store, ready } = useProgress();
  const dates = ready ? store.getActivityDates() : [];
  const key = dates.join(",");
  // eslint-disable-next-line react-hooks/exhaustive-deps
  return useMemo(() => computeStreak(dates, toLocalDateKey(new Date())), [key]);
}
