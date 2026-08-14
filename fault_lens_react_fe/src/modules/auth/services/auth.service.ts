import { authApi } from "../api/auth.api";
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
} from "../types/auth.types";

export const authService = {
  async login(payload: LoginRequest): Promise<AuthResponse> {
    return authApi.login(payload);
  },

  async register(payload: RegisterRequest): Promise<User> {
    return authApi.register(payload);
  },

  async me(): Promise<User> {
    return authApi.me();
  },

  async logout(): Promise<void> {
    await authApi.logout();
  },
};