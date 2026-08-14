"use client";

import { Box } from "@mui/material";

type DataTableToolbarProps = {
    search?: React.ReactNode;
    actions?: React.ReactNode;
};

export function DataTableToolbar({
    search,
    actions,
}: DataTableToolbarProps) {
    return (
        <Box
            sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2, gap: 2 }}
        >
            <Box sx={{ flex: 1 }}>{search}</Box>

            <Box sx={{ display: "flex", gap: 2 }}>
                {actions}
            </Box>
        </Box>
    );
}