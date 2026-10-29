import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl px-4 py-20 text-center">
      <h1 className="text-3xl font-bold">Page not found</h1>
      <p className="mt-2 text-zinc-600 dark:text-zinc-400">That page doesn&apos;t exist (yet).</p>
      <Link href="/" className="mt-6 inline-block rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500">
        Back to the dashboard
      </Link>
    </div>
  );
}
