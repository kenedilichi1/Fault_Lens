import { Box, Typography } from "@mui/material";
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";
import { Link as RouterLink } from "react-router-dom";
import type { SxProps, Theme } from "@mui/material";

interface ActionWidgetProps {
    readonly to: string;
    readonly label?: string;
    readonly sx?: SxProps<Theme>;
}

export function ActionWidget({ to, label = "View all", sx }: ActionWidgetProps) {
    return (
        <Box
            component={RouterLink}
            to={to}
            sx={{
                cursor: "pointer",
                color: "primary.main",
                textDecoration: "none",
                display: "inline-flex",
                alignItems: "center",
                gap: 0.5,
                "&:hover": {
                    color: "primary.dark",
                },
                ...sx,
            }}
        >
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                {label}
            </Typography>
            <ArrowRightAltIcon sx={{ fontSize: "1.15rem" }} />
        </Box>
    );
}
