/** 32-bit FNV-1a hash. */
export function fnv1a(input: string): number {
  let hash = 0x811c9dc5;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

/**
 * Deterministically picks the daily challenge for a date (YYYY-MM-DD). The pool
 * is sorted first so the result doesn't depend on load order.
 */
export function pickDailyChallenge(slugs: readonly string[], dateKey: string): string | null {
  if (slugs.length === 0) return null;
  const pool = [...new Set(slugs)].sort();
  return pool[fnv1a(`codedrill:${dateKey}`) % pool.length] ?? null;
}
