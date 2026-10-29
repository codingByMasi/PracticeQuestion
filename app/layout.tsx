import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { ThemeProvider } from "@/components/layout/ThemeProvider";
import { ProgressProvider } from "@/lib/progress/ProgressProvider";

export const metadata: Metadata = {
  title: { default: "CodeDrill", template: "%s · CodeDrill" },
  description: "Practice SQL and Python in your browser with instant feedback.",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#09090b" },
  ],
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen">
        <ThemeProvider>
          <ProgressProvider>
            <Header />
            <main id="main">{children}</main>
          </ProgressProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
