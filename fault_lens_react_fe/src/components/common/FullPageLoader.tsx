import { Box, CircularProgress } from "@mui/material";

export function FullPageLoader() {
  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: "100vw",
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "background.default",
        overflow: "hidden",
      }}
    >
      <CircularProgress />
    </Box>
  );
}