import { Navigate } from "react-router-dom";

import { useAuthStore } from "../store/auth.store";

/**
 * Redirects from the root path "/" based on auth state.
 * Waits for Zustand store hydration before deciding the redirect target.
 */
export function RootRedirect() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const hasHydrated = useAuthStore((state) => state._hasHydrated);

  if (!hasHydrated) return null; // Wait for localStorage rehydration

  if (accessToken) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Navigate to="/login" replace />;
}
