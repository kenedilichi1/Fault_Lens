import { Avatar, Box, IconButton, Typography } from "@mui/material";

import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";

interface SidebarFooterProps {
  readonly expanded: boolean;
}

export function SidebarFooter({ expanded }: SidebarFooterProps) {
  if (!expanded) {
    return (
      <Box
        sx={{
          borderTop: 1,
          borderColor: "divider",
          py: 2,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Avatar
          sx={{
            width: 16,
            height: 16,
            bgcolor: "rgba(124, 58, 237, 0.15)",
            color: "primary.light",
            border: 1,
            borderColor: "primary.dark",
          }}
        >
          A
        </Avatar>

        <Avatar
          sx={{
            width: 40,
            height: 40,
            bgcolor: "primary.main",
            color: "white",
          }}
        >
          J
        </Avatar>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        borderTop: 1,
        borderColor: "divider",
        p: 3,
      }}
    >
      {/* Organization */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          mb: 3,
        }}
      >
        <Avatar
          variant="rounded"
          sx={{
            width: 48,
            height: 48,
            bgcolor: "rgba(124, 58, 237, 0.12)",
            color: "primary.light",
            border: 1,
            borderColor: "rgba(124, 58, 237, 0.5)",
          }}
        >
          A
        </Avatar>

        <Box
          sx={{
            flex: 1,
            minWidth: 0,
          }}
        >
          <Typography sx={{ fontWeight: 600 }} noWrap>
            Acme Corp
          </Typography>

          <Typography variant="body2" color="text.secondary" noWrap>
            Production
          </Typography>
        </Box>

        <IconButton
          size="small"
          sx={{
            color: "text.secondary",
          }}
        >
          <KeyboardArrowDownIcon />
        </IconButton>
      </Box>

      {/* Current user */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
        }}
      >
        <Avatar
          sx={{
            width: 48,
            height: 48,
            bgcolor: "primary.main",
            color: "white",
          }}
        >
          J
        </Avatar>

        <Box>
          <Typography sx={{ fontWeight: 500 }}>Jamie Chen</Typography>

          <Typography variant="body2" color="text.secondary">
            Admin
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
