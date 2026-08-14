import { Outlet } from "react-router-dom";
import { ProtectedRoute } from "@/modules/auth/guards/ProtectedRoute";
import { AppShell } from "@/components/layout";

export default function ProtectedLayout() {
  return (
    <ProtectedRoute>
      <AppShell>
        <Outlet />
      </AppShell>
    </ProtectedRoute>
  );
}
