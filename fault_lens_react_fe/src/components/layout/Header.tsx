import {
  AppBar,
  Avatar,
  Box,
  IconButton,
  Toolbar,
  Typography,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import { useLocation } from "react-router-dom";

import { navigation } from "@/constants/navigation";

type HeaderProps = {
  onMenuClick: () => void;
};

export function Header({ onMenuClick }: HeaderProps) {
  const { pathname } = useLocation();

  const navigationItems = [
    ...navigation.basic,
    ...navigation.management,
  ];

  const currentPage = navigationItems.find(
    (item) => item.href === pathname
  );

  return (
    <AppBar
      position="sticky"
      elevation={0}
      color="inherit"
      sx={{
        height: 56,
        bgcolor: "#17151D",
        boxShadow: "none",
        borderBottom: "1px solid #302C36",
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <IconButton
            color="inherit"
            aria-label="open navigation"
            edge="start"
            onClick={onMenuClick}
            sx={{
              mr: 2,
              display: {
                xs: "flex",
                sm: "none",
              },
            }}
          >
            <MenuIcon />
          </IconButton>

          <Typography
            variant="h6"
            component="h1"
            sx={{ fontWeight: 600, fontSize: "h2.fontSize" }}
          >
            {currentPage?.label ?? "Overview"}
          </Typography>
        </Box>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2,
          }}
        >
          <IconButton>
            <Avatar />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}