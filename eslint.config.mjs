import next from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const config = [
  ...next,
  ...nextTs,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
    },
  },
  {
    // Architecture rule: UI code never touches storage or runtimes directly.
    files: ["components/**/*.{ts,tsx}", "app/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-globals": ["error", { name: "localStorage", message: "Use ProgressStore (lib/progress)." }],
      "no-restricted-imports": [
        "error",
        { paths: ["sql.js", "pyodide"], patterns: ["@/lib/runners/*/engine*", "@/lib/runners/*/*.worker*"] },
      ],
    },
  },
  { ignores: [".next/**", "node_modules/**", "public/vendor/**", "next-env.d.ts"] },
];

export default config;
