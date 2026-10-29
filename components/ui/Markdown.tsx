"use client";

import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ children, components, className = "" }: { children: string; components?: Components; className?: string }) {
  return (
    <div
      className={`prose prose-zinc max-w-none dark:prose-invert prose-pre:bg-zinc-100 prose-pre:text-zinc-800 dark:prose-pre:bg-zinc-900 dark:prose-pre:text-zinc-100 prose-code:before:content-none prose-code:after:content-none prose-code:rounded prose-code:bg-zinc-100 prose-code:px-1 prose-code:py-0.5 prose-code:font-normal dark:prose-code:bg-zinc-800 [&_pre_code]:bg-transparent [&_pre_code]:p-0 ${className}`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
