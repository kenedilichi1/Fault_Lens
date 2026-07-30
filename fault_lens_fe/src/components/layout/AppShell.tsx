"use client";

import { Box } from "@mui/material";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

type Props = Readonly<{
    children: React.ReactNode;
}>;

export function AppShell({ children }: Props) {
    return (
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
            <Sidebar />

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <Header />
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