import {
  Box,
  Drawer,
  useMediaQuery,
  useTheme,
} from "@mui/material";

import { SIDEBAR_WIDTH } from "@/constants/layout";

import { SidebarBrand } from "./SidebarBrand";
import { SidebarFooter } from "./SidebarFooter";
import { SidebarNavigation } from "./SidebarNavigation";

const SIDEBAR_COLLAPSED_WIDTH = 72;

interface SidebarProps {
  readonly mobileOpen: boolean;
  readonly desktopOpen: boolean;
  readonly onClose: () => void;
  readonly onDesktopToggle: () => void;
}

export function Sidebar({
  mobileOpen,
  desktopOpen,
  onClose,
  onDesktopToggle,
}: SidebarProps) {
  const theme = useTheme();

  const isMobile = useMediaQuery(
    theme.breakpoints.down("sm")
  );

  const expanded = desktopOpen || isMobile;

  const content = (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "background.paper",
        color: "text.primary",
      }}
    >
      <SidebarBrand
        expanded={desktopOpen}
        isMobile={isMobile}
        onToggle={onDesktopToggle}
      />

      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          overflowX: "hidden",

          "&::-webkit-scrollbar": {
            width: 4,
          },

          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "rgba(255,255,255,0.1)",
            borderRadius: 4,
          },
        }}
      >
        <SidebarNavigation
          expanded={expanded}
          isMobile={isMobile}
          onClose={onClose}
        />
      </Box>

      <SidebarFooter
        expanded={expanded}
      />
    </Box>
  );

  return (
    <Box
      component="nav"
      sx={{
        width: {
          sm: desktopOpen
            ? SIDEBAR_WIDTH
            : SIDEBAR_COLLAPSED_WIDTH,
        },
        flexShrink: 0,
      }}
    >
      {/* Mobile */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onClose}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: {
            xs: "block",
            sm: "none",
          },

          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: SIDEBAR_WIDTH,
            border: 0,
          },
        }}
      >
        {content}
      </Drawer>

      {/* Desktop */}
      <Drawer
        variant="permanent"
        open
        sx={{
          display: {
            xs: "none",
            sm: "block",
          },

          "& .MuiDrawer-paper": {
            boxSizing: "border-box",

            width: desktopOpen
              ? SIDEBAR_WIDTH
              : SIDEBAR_COLLAPSED_WIDTH,

            borderRight: 1,
            borderColor: "divider",

            overflowX: "hidden",

            transition: theme.transitions.create(
              "width",
              {
                easing: theme.transitions.easing.sharp,
                duration: desktopOpen
                  ? theme.transitions.duration.enteringScreen
                  : theme.transitions.duration.leavingScreen,
              }
            ),
          },
        }}
      >
        {content}
      </Drawer>
    </Box>
  );
}