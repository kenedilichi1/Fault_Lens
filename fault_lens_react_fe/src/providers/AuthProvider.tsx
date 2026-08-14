
import { useEffect } from "react";

import { useMe } from "@/modules/auth/hooks/useMe";
import { useAuthStore } from "@/modules/auth/store/auth.store";
import { FullPageLoader } from "@/components/common/FullPageLoader";

type Props = Readonly<{
  children: React.ReactNode;
}>;

export function AuthProvider({ children }: Props) {
  const accessToken = useAuthStore((state) => state.accessToken);
  const status = useAuthStore((state) => state.status);

  const setUser = useAuthStore((s) => s.setUser);
  const setStatus = useAuthStore((s) => s.setStatus);
  const logout = useAuthStore((s) => s.logout);

  const meQuery = useMe({
    enabled: !!accessToken,
  });

  useEffect(() => {
    if (!accessToken) {
      setStatus("unauthenticated");
      return;
    }

    if (meQuery.isPending) {
      setStatus("loading");
      return;
    }

    if (meQuery.isSuccess) {
      setUser(meQuery.data);
      setStatus("authenticated");
      return;
    }

    if (meQuery.isError) {
      logout();
    }
  }, [
    accessToken,
    meQuery.isPending,
    meQuery.isSuccess,
    meQuery.isError,
    meQuery.data,
    setStatus,
    setUser,
    logout,
  ]);

  if (status === "loading") {
    return <FullPageLoader />;
  }
  return <>{children}</>;
}
