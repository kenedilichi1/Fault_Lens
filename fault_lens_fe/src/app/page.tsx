"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Box, CircularProgress } from "@mui/material";

import { useAuthStore } from "@/modules/auth/store/auth.store";

export default function Home() {
  const router = useRouter();
  const accessToken = useAuthStore((state) => state.accessToken);
  const hasHydrated = useAuthStore((state) => state._hasHydrated);

  useEffect(() => {
    if (!hasHydrated) return;

    if (accessToken) {
      router.replace("/dashboard");
    } else {
      router.replace("/login");
    }
  }, [accessToken, hasHydrated, router]);

  // Always render the same spinner on server and client first pass
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <CircularProgress />
    </Box>
  );
}