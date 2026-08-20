import { create } from "zustand";
import { persist } from "zustand/middleware";

// TODO(security): `refreshToken` is currently persisted in localStorage via Zustand persist.
// This is vulnerable to XSS. The proper fix is to have the backend issue refresh tokens
// as httpOnly cookies, at which point `refreshToken` should be removed from this store entirely.
// Until then, this is a known security risk.

import type {AuthState } from "../types/auth.types";



export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      status: "unauthenticated",
      _hasHydrated: false,

      setTokens: (data) =>
        set({
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        }),

      setUser: (user) =>
        set({
          user,
        }),

      setStatus: (status) =>
        set({
          status,
        }),

      setHasHydrated: (value) =>
        set({
          _hasHydrated: value,
        }),

      logout: () =>
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          status: 'unauthenticated'
        }),
    }),
    {
      name: "faultlens-auth",
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true);
      },
    }
  )
);