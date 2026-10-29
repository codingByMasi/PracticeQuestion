"use client";

import { createContext, useContext, useEffect, useState, useSyncExternalStore, type ReactNode } from "react";
import { LocalStorageProgressStore, MemoryStorage, STORAGE_KEY } from "./local-storage-store";
import type { ProgressStore } from "./types";

const ProgressContext = createContext<ProgressStore | null>(null);

function createStore(): LocalStorageProgressStore {
  if (typeof window === "undefined") return new LocalStorageProgressStore(new MemoryStorage());
  try {
    return new LocalStorageProgressStore(window.localStorage);
  } catch {
    return new LocalStorageProgressStore(new MemoryStorage());
  }
}

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [store] = useState(createStore);

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY) store.reload();
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, [store]);

  return <ProgressContext.Provider value={store}>{children}</ProgressContext.Provider>;
}

/**
 * Returns the ProgressStore and re-renders on change. `ready` is false during
 * server rendering and hydration, when stored progress is not yet available.
 */
export function useProgress(): { store: ProgressStore; ready: boolean } {
  const store = useContext(ProgressContext);
  if (!store) throw new Error("useProgress must be used inside ProgressProvider");
  const version = useSyncExternalStore(
    (cb) => store.subscribe(cb),
    () => store.getVersion(),
    () => -1,
  );
  return { store, ready: version !== -1 };
}
