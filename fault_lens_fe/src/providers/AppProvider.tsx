"use client";

import { Toaster } from "sonner";

import { QueryProvider } from "./QueryProvider";
import { ThemeProvider } from "./ThemeProvider";

type Props = Readonly<{
  children: React.ReactNode;
}>;

export function AppProvider({ children }: Props) {
  return (
    <ThemeProvider>
      <QueryProvider>
        {children}
        <Toaster richColors position="top-right" />
      </QueryProvider>
    </ThemeProvider>
  );
}