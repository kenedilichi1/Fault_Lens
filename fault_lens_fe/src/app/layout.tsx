import type { Metadata } from "next";
import { AppProvider } from "@/providers/AppProvider";

import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
});
export const metadata: Metadata = {
  title: "FaultLens",
  description: "AI-powered observability platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}