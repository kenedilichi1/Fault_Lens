import { useState } from "react";
import { Box, useMediaQuery, useTheme } from "@mui/material";

import { Header } from "./Header";
import { Sidebar } from "./sidebar/Sidebar";
import { SIDEBAR_WIDTH } from "@/constants/layout";

type Props = Readonly<{
    children: React.ReactNode;
}>;

export function AppShell({ children }: Props) {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
    const [mobileOpen, setMobileOpen] = useState(false);
    const [desktopOpen, setDesktopOpen] = useState(true);

    const handleDrawerToggle = () => {
        if (isMobile) {
            setMobileOpen(!mobileOpen);
        } else {
            setDesktopOpen(!desktopOpen);
        }
    };

    return (
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
            <Sidebar 
                mobileOpen={mobileOpen}
                desktopOpen={desktopOpen}
                onClose={() => setMobileOpen(false)}
                onDesktopToggle={() => setDesktopOpen(!desktopOpen)}
            />

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    display: "flex",
                    flexDirection: "column",
                    width: { 
                        xs: '100%', 
                        sm: `calc(100% - ${desktopOpen ? SIDEBAR_WIDTH : 65}px)` 
                    },
                    transition: theme.transitions.create(['width', 'margin'], {
                        easing: theme.transitions.easing.sharp,
                        duration: desktopOpen 
                            ? theme.transitions.duration.enteringScreen 
                            : theme.transitions.duration.leavingScreen,
                    }),
                }}
            >
                <Header onMenuClick={handleDrawerToggle} />
                <Box
                    sx={{
                        flexGrow: 1,
                        p: 3,
                    }}
                >
                    {children}
                </Box>
            </Box>
        </Box>
    );
}