
import { useMutation } from "@tanstack/react-query";

import { authService } from "../services/auth.service";
import type { LoginRequest } from "../types/auth.types";
import { useAuthStore } from "../store/auth.store";
import { appToast } from "@/lib/toast";

export function useLogin() {
  const setTokens = useAuthStore((state) => state.setTokens);

  return useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),
    onSuccess: (data) => {
      setTokens(data);
      appToast.success("Welcome back!")
    },

    onError: () => {
      appToast.error("Invalid email or password.");
    },
  });
}