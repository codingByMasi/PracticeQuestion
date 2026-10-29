"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ThemeToggle } from "./ThemeToggle";
import { StreakBadge } from "./StreakBadge";

const NAV = [
  { href: "/problems", label: "Problems" },
  { href: "/learn", label: "Learn" },
  { href: "/playground/sql", label: "SQL Playground", match: "/playground/sql" },
  { href: "/playground/python", label: "Python Playground", match: "/playground/python" },
  { href: "/daily", label: "Daily" },
  { href: "/progress", label: "Progress" },
];

export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const isActive = (href: string) => pathname === href || pathname.startsWith(`${href}/`);

  const links = NAV.map((n) => (
    <Link
      key={n.href}
      href={n.href}
      onClick={() => setOpen(false)}
      aria-current={isActive(n.match ?? n.href) ? "page" : undefined}
      className="rounded-md px-3 py-2 text-sm font-medium text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 aria-[current=page]:bg-zinc-100 aria-[current=page]:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white dark:aria-[current=page]:bg-zinc-800 dark:aria-[current=page]:text-white"
    >
      {n.label}
    </Link>
  ));

  return (
    <header className="sticky top-0 z-30 border-b border-zinc-200 bg-white/90 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/90">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:rounded focus:bg-indigo-600 focus:px-3 focus:py-2 focus:text-white"
      >
        Skip to content
      </a>
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-2 px-4">
        <Link href="/" className="mr-2 flex items-center gap-2 font-semibold tracking-tight">
          <span className="rounded bg-indigo-600 px-1.5 py-0.5 font-mono text-xs text-white">{"</>"}</span>
          CodeDrill
        </Link>
        <nav aria-label="Main" className="hidden flex-1 items-center gap-1 lg:flex">
          {links}
        </nav>
        <div className="ml-auto flex items-center gap-1">
          <StreakBadge />
          <ThemeToggle />
          <button
            type="button"
            className="rounded-md p-2 text-zinc-600 hover:bg-zinc-100 lg:hidden dark:text-zinc-300 dark:hover:bg-zinc-800"
            aria-expanded={open}
            aria-controls="mobile-nav"
            aria-label="Toggle navigation"
            onClick={() => setOpen((o) => !o)}
          >
            <span aria-hidden="true">☰</span>
          </button>
        </div>
      </div>
      {open && (
        <nav id="mobile-nav" aria-label="Main" className="flex flex-col gap-1 border-t border-zinc-200 px-4 py-2 lg:hidden dark:border-zinc-800">
          {links}
        </nav>
      )}
    </header>
  );
}
