import { Box, Stack, Typography } from "@mui/material";
import { logSamples } from "../data/liveLogData";
import { timeFormatter } from "@/utils";
import { getLevelBadgeStyles } from "../utils";



export default function LiveLogs() {
    return (
        <Stack sx={{ mt: 1, gap: 1 }}>
            {logSamples.map((log, index) => (
                <Box
                    key={index}
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 2,
                        fontSize: "0.75rem",
                        px: 1,
                        cursor: 'pointer',
                        borderRadius: "4px",
                        transition: "all 0.2s ease",
                        "&:hover": {
                            backgroundColor: "action.hover",
                        },
                    }}
                >
                    {/* Timestamp */}
                    <Typography
                        variant="caption"
                        sx={{
                            fontFamily: "inherit",
                            fontSize: "inherit",
                            color: "text.secondary",
                            opacity: 0.7,
                            width: "82px",
                            flexShrink: 0,
                        }}
                    >
                        {timeFormatter(new Date(log.ts))}
                    </Typography>

                    {/* Log Level */}
                    <Box
                        sx={{
                            width: "48px",
                            display: "inline-flex",
                            justifyContent: "center",
                            alignItems: "center",
                            py: 0.25,
                            borderRadius: "4px",
                            fontSize: "0.6875rem",
                            fontWeight: 700,
                            lineHeight: 1,
                            flexShrink: 0,
                            ...getLevelBadgeStyles(log.level),
                        }}
                    >
                        {log.level}
                    </Box>

                    {/* Log Detail */}
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1, minWidth: 0, overflow: "hidden" }}>
                        <Typography
                            component="span"
                            sx={{
                                fontFamily: "inherit",
                                fontSize: "inherit",
                                color: "primary.light",
                                fontWeight: 500,
                                flexShrink: 0,
                            }}
                        >
                            {log.service}
                        </Typography>
                        <Typography
                            component="span"
                            sx={{
                                fontFamily: "inherit",
                                fontSize: "inherit",
                                color: "text.primary",
                                opacity: 0.9,
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                whiteSpace: "nowrap",
                            }}
                        >
                            {log.msg}
                        </Typography>
                    </Box>
                </Box>
            ))}
        </Stack>
    );
}