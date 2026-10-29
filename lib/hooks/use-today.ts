"use client";

import { toLocalDateKey } from "@/lib/progress/dates";
import { useIsClient } from "./use-is-client";

/** Today's local date (YYYY-MM-DD), or null during server render/hydration. */
export function useToday(): string | null {
  const isClient = useIsClient();
  return isClient ? toLocalDateKey(new Date()) : null;
}
