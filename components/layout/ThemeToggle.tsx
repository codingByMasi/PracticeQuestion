"use client";

import { useTheme } from "next-themes";
import { useIsClient } from "@/lib/hooks/use-is-client";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const isClient = useIsClient();
  const dark = isClient && resolvedTheme === "dark";
  return (
    <button
      type="button"
      onClick={() => setTheme(dark ? "light" : "dark")}
      className="rounded-md p-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
      aria-label={dark ? "Switch to light theme" : "Switch to dark theme"}
      title="Toggle theme"
    >
      <span aria-hidden="true">{dark ? "☀︎" : "☾"}</span>
    </button>
  );
}
