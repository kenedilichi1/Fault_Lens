import { api } from "@/lib/api";

import type {
  LoginRequest,
  AuthResponse,
  RegisterRequest,
  User,
} from "../types/auth.types";

export const authApi = {
  login: async (payload: LoginRequest) => {
    const { data } = await api.post<AuthResponse>(
      "/auth/login",
      payload
    );

    return data;
  },

  register: async (payload: RegisterRequest) => {
    const { data } = await api.post<User>(
      "/auth/register",
      payload
    );

    return data;
  },

  logout: async () => {
    await api.post("/auth/logout");
  },

  refresh: async (refreshToken: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>(
      "/auth/refresh",
      {
        refresh_token: refreshToken
      }
    );

    return data;
  },

  me: async () => {
    const { data } = await api.get("/auth/me");

    return data;
  },
};