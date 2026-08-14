import { Box, Typography } from "@mui/material";

type PageHeaderProps = {
    title: string;
    subtitle?: string;
    actions?: React.ReactNode;
};

export function PageHeader({
    title,
    subtitle,
    actions,
}: PageHeaderProps) {
    return (
        <Box
            sx={{
                mb: 4,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                gap: 2,
            }}
        >
            <Box>
                <Typography
                    variant="h4"
                    gutterBottom
                    sx={{ fontWeight: 700 }}
                >
                    {title}
                </Typography>

                {subtitle && (
                    <Typography
                        variant="body1"
                        color="text.secondary"
                    >
                        {subtitle}
                    </Typography>
                )}
            </Box>

            {actions && (
                <Box sx={{ display: "flex", gap: 2 }}>
                    {actions}
                </Box>
            )}
        </Box>
    );
}