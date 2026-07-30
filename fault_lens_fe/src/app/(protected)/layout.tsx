
import { ProtectedRoute } from "@/modules/auth/guards/ProtectedRoute";
import { AppShell } from "@/components/layout";
type Props = Readonly<{
    children: React.ReactNode;
}>;

export default function ProtectedLayout({ children }: Props) {
    return (
        <ProtectedRoute>
            <AppShell>
                {children}
            </AppShell>
        </ProtectedRoute>);
}