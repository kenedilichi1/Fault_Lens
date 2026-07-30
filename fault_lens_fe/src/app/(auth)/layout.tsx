import { PublicRoute } from "@/modules/auth/guards/PublicRoute";
import { Box, Container } from "@mui/material";

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <PublicRoute>
          {children}
        </PublicRoute>
      </Box>
    </Container>
  );
}