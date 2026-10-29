"use client";

import type { Runner } from "./types";
import { createSqlRunner } from "./sql";

/**
 * Runner factories by id. A new language = a new Runner implementation registered here.
 * Runners are created lazily, so a runtime only loads when a page needs it.
 */
const factories: Record<string, () => Runner> = {
  sql: createSqlRunner,
};

const instances = new Map<string, Runner>();

export function getRunner(id: string): Runner {
  let runner = instances.get(id);
  if (!runner) {
    const factory = factories[id];
    if (!factory) throw new Error(`No runner registered for "${id}"`);
    runner = factory();
    instances.set(id, runner);
  }
  return runner;
}
