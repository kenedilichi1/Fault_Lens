
import { QueryProvider } from "./QueryProvider";
import { ThemeProvider } from "./ThemeProvider";
import { AuthProvider } from "./AuthProvider";
import { ToastProvider } from "./ToastProvider";

type Props = Readonly<{
  children: React.ReactNode;
}>;

export function AppProvider({ children }: Props) {
  return (
    <ThemeProvider>
      <QueryProvider>
        <AuthProvider>
          <ToastProvider />
          {children}
        </AuthProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}