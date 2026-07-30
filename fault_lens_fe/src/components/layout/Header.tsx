"use client";

import {
    AppBar,
    Avatar,
    Box,
    IconButton,
    Toolbar,
    Typography,
} from "@mui/material";

export function Header() {
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
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Dashboard
                </Typography>

                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                    <IconButton>
                        <Avatar />
                    </IconButton>
                </Box>
            </Toolbar>
        </AppBar>
    );
}