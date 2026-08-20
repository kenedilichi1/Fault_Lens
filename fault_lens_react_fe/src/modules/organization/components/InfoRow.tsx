import { Box, Typography } from "@mui/material";

export default function InfoRow({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: {
          xs: "100px 1fr",
          sm: "120px 1fr",
        },
        gap: 2,
        alignItems: "center",
      }}
    >
      <Typography
        variant="body2"
        color="text.secondary"
      >
        {label}
      </Typography>

      <Box>
        {typeof children === "string" ? (
          <Typography
            variant="body2"
            sx={{ fontWeight: 500 }}
          >
            {children}
          </Typography>
        ) : (
          children
        )}
      </Box>
    </Box>
  );
}