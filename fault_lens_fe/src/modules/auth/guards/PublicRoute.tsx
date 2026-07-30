"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Box, CircularProgress } from "@mui/material";

import { useAuthStore } from "../store/auth.store";

type Props = Readonly<{
  children: React.ReactNode;
}>;

export function PublicRoute({ children }: Props) {
  const router = useRouter();

  const accessToken = useAuthStore((state) => state.accessToken);
  const hasHydrated = useAuthStore((state) => state._hasHydrated);

  useEffect(() => {
    if (hasHydrated && accessToken) {
      router.replace("/dashboard");
    }
  }, [accessToken, hasHydrated, router]);

  // Wait for localStorage rehydration before deciding
  if (!hasHydrated) {
    return (
      <Box sx={{ minHeight: "100vh", display: "flex", justifyContent: "center", alignItems: "center" }}>
        <CircularProgress />
      </Box>
    );
  }

  if (accessToken) {
    return null;
  }

  return <>{children}</>;
}