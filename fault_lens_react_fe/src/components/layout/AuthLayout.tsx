import { Outlet } from "react-router-dom";
import { PublicRoute } from "@/modules/auth/guards/PublicRoute";
import { Box, Container } from "@mui/material";

export default function AuthLayout() {
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
          <Outlet />
        </PublicRoute>
      </Box>
    </Container>
  );
}
