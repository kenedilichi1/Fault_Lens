import type { Metadata } from "next";
import { AppProvider } from "@/providers/AppProvider";


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
      <body>
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}