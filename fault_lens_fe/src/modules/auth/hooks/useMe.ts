import { useQuery } from "@tanstack/react-query";

import { authService } from "../services/auth.service";
import { User } from "../types/auth.types";

type UseMeOptions = {
  enabled?: boolean;
};
    
export function useMe(options?: UseMeOptions) {
    
  return useQuery<User>({
    queryKey: ["me"],
    queryFn: authService.me,
    enabled: options?.enabled,
  });
}