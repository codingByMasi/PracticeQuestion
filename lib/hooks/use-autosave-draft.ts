"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useProgress } from "@/lib/progress/ProgressProvider";

/** Editor state for `key`, initialised from the saved draft and autosaved (debounced). */
export function useAutosaveDraft(key: string, initial: string, delayMs = 400) {
  const { store } = useProgress();
  const [code, setCodeState] = useState(() => store.getDraft(key) ?? initial);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const latest = useRef(code);

  const flush = useCallback(() => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = null;
    store.saveDraft(key, latest.current);
  }, [key, store]);

  const setCode = useCallback(
    (next: string) => {
      latest.current = next;
      setCodeState(next);
      if (timer.current) clearTimeout(timer.current);
      timer.current = setTimeout(flush, delayMs);
    },
    [delayMs, flush],
  );

  useEffect(() => {
    const onHide = () => {
      if (timer.current) flush();
    };
    window.addEventListener("pagehide", onHide);
    return () => {
      window.removeEventListener("pagehide", onHide);
      onHide();
    };
  }, [flush]);

  return [code, setCode] as const;
}
