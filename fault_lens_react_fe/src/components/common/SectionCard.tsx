import { Box, Card, CardContent, Divider, Icon, Typography, keyframes } from "@mui/material";
import CircleIcon from '@mui/icons-material/Circle';

const blink = keyframes`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
  100% {
    opacity: 1;
  }
`;

type SectionCardProps = {
    readonly title: string;
    readonly subtitle?: string;
    readonly actions?: React.ReactNode;
    readonly children: React.ReactNode;
    readonly isLive?: boolean;
};

export function SectionCard({
    title,
    subtitle,
    actions,
    children,
    isLive,
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
                        mb: 1
                    }}
                >
                    <Box>
                        <Typography variant="h6" sx={{ fontWeight: 500, fontSize: "1.2rem" }}>
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

                    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                        {isLive && (
                            <Box
                                sx={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 1,
                                }}
                            >
                                <Icon
                                    color="success"
                                    sx={{
                                        animation: `${blink} 1.5s infinite ease-in-out`,
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <CircleIcon sx={{ fontSize: "0.625rem" }} />
                                </Icon>
                                <Typography variant="body2" color="success.main" sx={{ fontWeight: 500 }}>
                                    Live
                                </Typography>
                            </Box>
                        )}

                        {actions}
                    </Box>
                </Box>
                <Divider />


                {children}
            </CardContent>
        </Card>
    );
}