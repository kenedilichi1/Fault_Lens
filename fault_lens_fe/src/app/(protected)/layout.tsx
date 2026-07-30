
import { ProtectedRoute } from "@/modules/auth/guards/ProtectedRoute";

type Props = Readonly<{
    children: React.ReactNode;
}>;

export default function ProtectedLayout({ children }: Props) {
    return <ProtectedRoute>{children}</ProtectedRoute>;
}