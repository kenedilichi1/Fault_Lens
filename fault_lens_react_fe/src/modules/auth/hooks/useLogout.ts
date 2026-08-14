import { useMutation } from "@tanstack/react-query";
import { authService } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";
import { useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { appToast } from "@/lib/toast";

export function useLogout() {
    const logout = useAuthStore((state) => state.logout);
    const queryClient = useQueryClient();
    const navigate = useNavigate();
    return useMutation({
        mutationFn: () => authService.logout(),
        onSettled: () => {
            logout();
            queryClient.clear();
            navigate("/login", { replace: true });
            appToast.success("Logged out successfully")
        },
    });
}
