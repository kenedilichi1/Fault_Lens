import {
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
} from "@mui/material";

import { Link as RouterLink, useLocation } from "react-router-dom";

import type { NavigationItem } from "@/constants/navigation";

interface SidebarNavigationItemProps {
  readonly item: NavigationItem;
  readonly expanded: boolean;
  readonly isMobile: boolean;
  readonly onClose: () => void;
}

export function SidebarNavigationItem({
  item,
  expanded,
  isMobile,
  onClose,
}: SidebarNavigationItemProps) {
  const { pathname } = useLocation();

  const Icon = item.icon;

  const isActive =
    pathname === item.href || pathname.startsWith(`${item.href}/`);

  const button = (
    <ListItemButton
      component={RouterLink}
      to={item.href}
      selected={isActive}
      onClick={isMobile ? onClose : undefined}
      sx={{
        position: "relative",
        minHeight: 40,
        mx: expanded ? 2 : 0.75,
        mb: 0.3,
        px: expanded ? 1.5 : 1,
        borderRadius: expanded ? 1.5 : 1,

        justifyContent: expanded ? "initial" : "center",

        color: "text.secondary",

        transition: "all 0.2s ease",

        "&:hover": {
          backgroundColor: "rgba(255,255,255,0.04)",
          color: "text.primary",
        },

        "&.Mui-selected": {
          backgroundColor: "rgba(124, 58, 237, 0.15)",
          color: "primary.light",
        },

        "&.Mui-selected:hover": {
          backgroundColor: "rgba(124, 58, 237, 0.18)",
        },

        ...(isActive && expanded
          ? {
            "&::before": {
              content: '""',
              position: "absolute",
              left: 0,
              top: "50%",
              transform: "translateY(-50%)",
              width: 4,
              height: 40,
              borderRadius: "0 4px 4px 0",
              backgroundColor: "primary.light",
            },
          }
          : {}),
      }}
    >
      <ListItemIcon
        sx={{
          minWidth: 0,
          mr: expanded ? 2 : 0,
          color: "inherit",
          justifyContent: "center",

          "& svg": {
            fontSize: 20,
          },
        }}
      >
        <Icon />
      </ListItemIcon>

      <ListItemText
        primary={item.label}
        sx={{
          opacity: expanded ? 1 : 0,
          width: expanded ? "auto" : 0,
          overflow: "hidden",
          whiteSpace: "nowrap",
          transition: "opacity 0.2s ease",

          "& .MuiListItemText-primary": {
            fontSize: "caption.fontSize",
            fontWeight: isActive ? 500 : 400,
          },
        }}
      />
    </ListItemButton>
  );

  if (!expanded) {
    return (
      <Tooltip title={item.label} placement="right">
        {button}
      </Tooltip>
    );
  }

  return button;
}
