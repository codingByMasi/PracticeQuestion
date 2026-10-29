"use client";

import Editor, { type BeforeMount, type OnMount } from "@monaco-editor/react";
import { useTheme } from "next-themes";
import { useEffect, useRef } from "react";

/** Built-in themes with comment colours raised to WCAG AA contrast. */
const defineThemes: BeforeMount = (monaco) => {
  monaco.editor.defineTheme("codedrill-light", { base: "vs", inherit: true, rules: [{ token: "comment", foreground: "5c6b78" }], colors: {} });
  monaco.editor.defineTheme("codedrill-dark", { base: "vs-dark", inherit: true, rules: [{ token: "comment", foreground: "86b077" }], colors: {} });
};

type Props = {
  value: string;
  onChange: (value: string) => void;
  language: string;
  /** Ctrl/Cmd+Enter */
  onRun?: () => void;
  /** Ctrl/Cmd+Shift+Enter */
  onSubmit?: () => void;
  ariaLabel?: string;
  height?: string;
};

export function CodeEditor({ value, onChange, language, onRun, onSubmit, ariaLabel = "Code editor", height = "100%" }: Props) {
  const { resolvedTheme } = useTheme();
  const runRef = useRef(onRun);
  const submitRef = useRef(onSubmit);
  useEffect(() => {
    runRef.current = onRun;
    submitRef.current = onSubmit;
  }, [onRun, onSubmit]);

  const handleMount: OnMount = (editor, monaco) => {
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => runRef.current?.());
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => submitRef.current?.());
  };

  return (
    <Editor
      height={height}
      language={language}
      value={value}
      onChange={(v) => onChange(v ?? "")}
      beforeMount={defineThemes}
      onMount={handleMount}
      theme={resolvedTheme === "dark" ? "codedrill-dark" : "codedrill-light"}
      loading={<div className="p-4 text-sm text-zinc-500 dark:text-zinc-400">Loading editor…</div>}
      options={{
        ariaLabel,
        minimap: { enabled: false },
        fontSize: 14,
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: language === "python" ? 4 : 2,
        wordWrap: "on",
        padding: { top: 8 },
        accessibilitySupport: "auto",
      }}
    />
  );
}
