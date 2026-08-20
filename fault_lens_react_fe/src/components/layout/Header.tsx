"use client";

import {
    AppBar,
    Avatar,
    Box,
    IconButton,
    Toolbar,
    Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

type HeaderProps = {
    onMenuClick: () => void;
};

export function Header({ onMenuClick }: HeaderProps) {
    return (
        <AppBar
            position="sticky"
            elevation={1}
            color="inherit"
            sx={{
                borderBottom: 1,
                borderColor: "divider",
            }}
        >
            <Toolbar
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                }}
            >
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={onMenuClick}
                        sx={{ mr: 2, display: { sm: "none" } }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        
                    </Typography>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                    <IconButton>
                        <Avatar />
                    </IconButton>
                </Box>
            </Toolbar>
        </AppBar>
    );
}