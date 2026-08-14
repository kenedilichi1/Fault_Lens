import { Box, Card, CardContent, Typography } from "@mui/material";

type SectionCardProps = {
    title: string;
    subtitle?: string;
    actions?: React.ReactNode;
    children: React.ReactNode;
};

export function SectionCard({
    title,
    subtitle,
    actions,
    children,
}: SectionCardProps) {
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
                    sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        mb: 3
                    }}
                >
                    <Box>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {title}
                        </Typography>

                        {subtitle && (
                            <Typography
                                variant="body2"
                                color="text.secondary"
                            >
                                {subtitle}
                            </Typography>
                        )}
                    </Box>

                    {actions}
                </Box>

                {children}
            </CardContent>
        </Card>
    );
}