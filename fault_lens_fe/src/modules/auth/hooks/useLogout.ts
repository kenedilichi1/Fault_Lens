import { useMutation } from "@tanstack/react-query";
import { authService } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";
import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { appToast } from "@/lib/toast";

export function useLogout() {
    const logout = useAuthStore((state) => state.logout);
    const queryClient = useQueryClient();
    const router = useRouter();
    return useMutation({
        mutationFn: () => authService.logout(),
        onSettled: () => {
            logout();
            queryClient.clear();
            router.replace("/login");
            appToast.success("Logged out successfully")
        },
    });
}
