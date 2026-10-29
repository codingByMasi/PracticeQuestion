/** Fenced code blocks tagged `<language>-run` are rendered as runnable snippets. */
export const RUNNABLE_SUFFIX = "-run";

export type Snippet = { language: string; code: string };

export function extractRunnableSnippets(markdown: string): Snippet[] {
  const re = /^```([a-z0-9]+)-run[^\n]*\n([\s\S]*?)^```/gm;
  return [...markdown.matchAll(re)].map((m) => ({ language: m[1] ?? "", code: (m[2] ?? "").trimEnd() }));
}

/** Maps a snippet's language tag to a runner id via the track list. */
export function runnerForLanguage(language: string, tracks: { runnerId: string; editorLanguage: string }[]): string | undefined {
  return tracks.find((t) => t.editorLanguage === language || t.runnerId === language)?.runnerId;
}
