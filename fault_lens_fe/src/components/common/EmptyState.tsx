import { Box, Typography } from "@mui/material";

type EmptyStateProps = {
    title: string;
    description?: string;
    icon?: React.ReactNode;
    action?: React.ReactNode;
};

export function EmptyState({
    title,
    description,
    icon,
    action,
}: EmptyStateProps) {
    return (
        <Box
            sx={{
                py: 8,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textAlign: "center",
            }}
        >
            {icon && (
                <Box
                    sx={{
                        mb: 3,
                        color: "text.secondary",
                    }}
                >
                    {icon}
                </Box>
            )}

            <Typography
                variant="h6"
                sx={{ fontWeight: 600 }}
            >
                {title}
            </Typography>

            {description && (
                <Typography
                    color="text.secondary"
                    sx={{
                        mt: 1,
                        maxWidth: 450,
                    }}
                >
                    {description}
                </Typography>
            )}

            {action && (
                <Box sx={{ mt: 4 }}>
                    {action}
                </Box>
            )}
        </Box>
    );
}