import { useMutation } from "@tanstack/react-query";

import { authApi } from "../api/auth.api";
import type { RegisterRequest } from "../types/auth.types";
import { appToast } from "@/lib/toast";

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterRequest) => authApi.register(data),

    onSuccess: () => {
      appToast.success("Account created successfully");
    },

    onError: () => {
      appToast.error("Failed to create account");
    },
  });
}