import "server-only";
import { loadContent } from "./load";

export * from "./load";

/** Cached content for server components (content is static per build). */
let cache: ReturnType<typeof loadContent> | undefined;
export function getContent() {
  cache ??= loadContent();
  return cache;
}
