"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
    Drawer,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography,
    Box,
} from "@mui/material";
import { navigation } from "@/constants/navigation";
import { SIDEBAR_WIDTH } from "@/constants/layout";



export function Sidebar() {
    const pathname = usePathname();

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: SIDEBAR_WIDTH,
                flexShrink: 0,

                "& .MuiDrawer-paper": {
                    width: SIDEBAR_WIDTH,
                    boxSizing: "border-box",
                },
            }}
        >
            <Toolbar>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    FaultLens
                </Typography>
            </Toolbar>

            <Box sx={{ overflow: "auto" }}>
                <List>
                    {navigation.map((item) => {
                        const Icon = item.icon;

                        return (
                            <ListItemButton
                                key={item.href}
                                component={Link}
                                href={item.href}
                                selected={pathname === item.href}
                            >
                                <ListItemIcon>
                                    <Icon />
                                </ListItemIcon>

                                <ListItemText primary={item.label} />
                            </ListItemButton>
                        );
                    })}
                </List>
            </Box>
        </Drawer>
    );
}