import { useMutation } from "@tanstack/react-query";

import { authApi } from "../api/auth.api";
import type { RegisterRequest } from "../types/auth.types";
import { appToast } from "@/lib/toast";

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterRequest) => authApi.register(data),

    onSuccess: (data) => {
      appToast.success("Account created successfully");
    },

    onError: (error) => {
      appToast.error("Failed to create account");
    },
  });
}