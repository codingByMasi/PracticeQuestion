"use client";

export default function ErrorPage({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="mx-auto max-w-xl px-4 py-20 text-center">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="mt-2 font-mono text-sm text-zinc-600 dark:text-zinc-400">{error.message}</p>
      <button type="button" onClick={reset} className="mt-6 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500">
        Try again
      </button>
    </div>
  );
}
