"use client";

import Editor, { type OnMount } from "@monaco-editor/react";
import { useTheme } from "next-themes";
import { useEffect, useRef } from "react";

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
      onMount={handleMount}
      theme={resolvedTheme === "dark" ? "vs-dark" : "light"}
      loading={<div className="p-4 text-sm text-zinc-500">Loading editor…</div>}
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
