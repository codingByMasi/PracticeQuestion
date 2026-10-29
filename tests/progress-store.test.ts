import { describe, expect, it } from "vitest";
import { LocalStorageProgressStore, MemoryStorage } from "@/lib/progress/local-storage-store";

function makeStore(date = new Date(2026, 9, 29, 12)) {
  const storage = new MemoryStorage();
  let now = date;
  const store = new LocalStorageProgressStore(storage, () => now);
  return { store, storage, setNow: (d: Date) => (now = d) };
}

describe("LocalStorageProgressStore", () => {
  it("tracks attempts and status", () => {
    const { store } = makeStore();
    expect(store.getProblemStatus("p")).toBe("unsolved");
    store.saveAttempt("p", "x", false);
    expect(store.getProblemStatus("p")).toBe("attempted");
    expect(store.getFailedAttempts("p")).toBe(1);
    store.saveAttempt("p", "y", true);
    expect(store.getProblemStatus("p")).toBe("solved");
    store.saveAttempt("p", "z", false);
    expect(store.getProblemStatus("p")).toBe("solved");
  });

  it("records activity on local dates", () => {
    const { store, setNow } = makeStore();
    store.saveAttempt("p", "x", true);
    setNow(new Date(2026, 9, 30, 9));
    store.markLessonDone("sql/intro");
    expect(store.getActivityDates()).toEqual(["2026-10-29", "2026-10-30"]);
    expect(store.getLessonDone("sql/intro")).toBe(true);
  });

  it("persists and reloads from storage", () => {
    const { store, storage } = makeStore();
    store.saveDraft("p", "SELECT 1;");
    const again = new LocalStorageProgressStore(storage);
    expect(again.getDraft("p")).toBe("SELECT 1;");
  });

  it("round-trips export and import", () => {
    const a = makeStore().store;
    a.saveAttempt("p", "x", true);
    a.setLastVisited("/problems/p", "P");
    const b = makeStore().store;
    b.import(a.export());
    expect(b.getProblemStatus("p")).toBe("solved");
    expect(b.getLastVisited()?.href).toBe("/problems/p");
  });

  it("rejects invalid imports without losing data", () => {
    const { store } = makeStore();
    store.saveAttempt("p", "x", true);
    expect(() => store.import("{}")).toThrow();
    expect(() => store.import("not json")).toThrow();
    expect(store.getProblemStatus("p")).toBe("solved");
  });

  it("recovers from corrupt storage", () => {
    const storage = new MemoryStorage();
    storage.setItem("codedrill:progress", "{broken");
    expect(new LocalStorageProgressStore(storage).getActivityDates()).toEqual([]);
  });

  it("notifies subscribers", () => {
    const { store } = makeStore();
    let calls = 0;
    const off = store.subscribe(() => calls++);
    store.saveDraft("p", "a");
    off();
    store.saveDraft("p", "b");
    expect(calls).toBe(1);
  });
});
