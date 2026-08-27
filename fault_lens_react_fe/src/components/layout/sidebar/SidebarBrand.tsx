import {
  Box,
  IconButton,
  Typography,
} from "@mui/material";

import LightModeTwoToneIcon from "@mui/icons-material/LightModeTwoTone";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

import { Link as RouterLink } from "react-router-dom";

interface SidebarBrandProps {
  readonly expanded: boolean;
  readonly isMobile: boolean;
  readonly onToggle: () => void;
}

export function SidebarBrand({
  expanded,
  isMobile,
  onToggle,
}: SidebarBrandProps) {
  return (
    <Box
      sx={{
        height: 56,
        px: 3,
        display: "flex",
        alignItems: "center",
        justifyContent: expanded ? "space-between" : "center",
        borderBottom: 1,
        borderColor: "divider",
      }}
    >
      {expanded ? (
        <Box
          component={RouterLink}
          to="/"
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.5,
            color: "inherit",
            textDecoration: "none",
          }}
        >
          <Box
            sx={{
              width: 36,
              height: 36,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: 1,
              backgroundColor: "primary.main",
            }}
          >
            <LightModeTwoToneIcon
              sx={{
                fontSize: "1.5rem",
                color: "white",
              }}
            />
          </Box>

          <Typography
            variant="h6"

            sx={{
              color: "text.primary",
              letterSpacing: -0.5,
              fontWeight: "h6.fontWeight",
              fontSize: "body2.fontSize"
            }}
          >
            FaultLens
          </Typography>
        </Box>
      ) : (
        <IconButton
          component={RouterLink}
          to="/"
          aria-label="FaultLens home"
        >
          <LightModeTwoToneIcon color="primary" />
        </IconButton>
      )}

      {!isMobile && (
        <IconButton
          onClick={onToggle}
          size="small"
          sx={{
            color: "text.secondary",
            textAlign: 'end'
          }}
        >
          {expanded ? (
            <ChevronLeftIcon />
          ) : (
            <ChevronRightIcon />
          )}
        </IconButton>
      )}
    </Box>
  );
}