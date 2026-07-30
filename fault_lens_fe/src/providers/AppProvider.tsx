"use client";

import { Toaster } from "sonner";

import { QueryProvider } from "./QueryProvider";
import { ThemeProvider } from "./ThemeProvider";
import { AuthProvider } from "./AuthProvider";

type Props = Readonly<{
  children: React.ReactNode;
}>;

export function AppProvider({ children }: Props) {
  return (
    <ThemeProvider>
      <QueryProvider>
        <AuthProvider>
        {children}
        </AuthProvider>
        <Toaster richColors position="top-right" />
      </QueryProvider>
    </ThemeProvider>
  );
}