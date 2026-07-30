import { Card, CardContent, Box, Typography } from "@mui/material";

type StatCardProps = {
    title: string;
    value: string | number;
    subtitle?: string;
    icon?: React.ReactNode;
};

export function StatCard({
    title,
    value,
    subtitle,
    icon,
}: StatCardProps) {
    return (
        <Card
            elevation={0}
            sx={{
                border: 1,
                borderColor: "divider",
                borderRadius: 3,
                height: "100%",
            }}
        >
            <CardContent>
                <Box
                    sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}
                >
                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        {title}
                    </Typography>

                    {icon}
                </Box>

                <Typography
                    variant="h4"
                    sx={{ fontWeight: 700 }}
                >
                    {value}
                </Typography>

                {subtitle && (
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ mt: 1 }}
                    >
                        {subtitle}
                    </Typography>
                )}
            </CardContent>
        </Card>
    );
}