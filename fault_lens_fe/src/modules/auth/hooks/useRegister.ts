import { useMutation } from "@tanstack/react-query";

import { authApi } from "../api/auth.api";
import type { RegisterRequest } from "../types/auth.types";

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterRequest) => authApi.register(data),

    onSuccess: (data) => {
      console.log("SUCCESS", data);
    },

    onError: (error) => {
      console.log("ERROR", error);
    },
  });
}