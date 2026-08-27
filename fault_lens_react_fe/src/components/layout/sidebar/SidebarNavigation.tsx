import { Box, List, Typography } from "@mui/material";

import { navigation } from "@/constants/navigation";

import { SidebarNavigationItem } from "./SidebarNavigationItem";

interface SidebarNavigationProps {
  readonly expanded: boolean;
  readonly isMobile: boolean;
  readonly onClose: () => void;
}

export function SidebarNavigation({
  expanded,
  isMobile,
  onClose,
}: SidebarNavigationProps) {
  return (
    <Box
      sx={{
        pt: 3,
      }}
    >
      <List disablePadding>
        {navigation.basic.map((item) => (
          <SidebarNavigationItem
            key={item.href}
            item={item}
            expanded={expanded}
            isMobile={isMobile}
            onClose={onClose}
          />
        ))}
      </List>

      {expanded && (
        <Typography
          variant="caption"
          sx={{
            display: "block",
            px: 3,
            mt: 3,
            mb: 1.5,
            color: "text.secondary",
            fontSize: "body2.fontSize",
            fontWeight: 600,
            letterSpacing: 1.2,
          }}
        >
          MANAGEMENT
        </Typography>
      )}

      <List disablePadding>
        {navigation.management.map((item) => (
          <SidebarNavigationItem
            key={item.href}
            item={item}
            expanded={expanded}
            isMobile={isMobile}
            onClose={onClose}
          />
        ))}
      </List>
    </Box>
  );
}
