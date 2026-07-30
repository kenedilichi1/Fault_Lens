import { create } from "zustand";
import { persist } from "zustand/middleware";


import type { User, AuthResponse } from "../types/auth.types";

type AuthStatus =
  | "loading"
  | "authenticated"
  | "unauthenticated";

type AuthState = {
  status: AuthStatus;
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;

  _hasHydrated: boolean;

  setUser: (user: User | null) => void;
  logout: () => void;
  setTokens: (data: AuthResponse) => void;
  setStatus: (status: AuthStatus) => void;
  setHasHydrated: (value: boolean) => void;
};

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