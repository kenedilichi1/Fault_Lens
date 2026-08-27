import { Box, Divider, Stack, Typography } from "@mui/material";
import { recentIncidents } from "../data/incidentData";
import { formatStatusLabel, getSeverityColor, getStatusBadgeStyles } from "../utils";



export default function RecentIncidents() {
    return (
        <Stack divider={<Divider sx={{ borderColor: "divider" }} />} sx={{ mt: 1 }}>
            {recentIncidents.map((incident) => (
                <Box
                    key={incident.id}
                    sx={{
                        display: "flex",
                        alignItems: "flex-start",
                        gap: 1.5,
                        py: 2,
                        px: 1.5,
                        mx: -1.5,
                        borderRadius: 1.5,
                        cursor: "pointer",
                        transition: "all 0.2s ease",
                        "&:hover": {
                            backgroundColor: "action.hover",
                        },
                    }}
                >
                    {/* Status Dot */}
                    <Box
                        sx={{
                            width: 8,
                            height: 8,
                            borderRadius: "50%",
                            backgroundColor: getSeverityColor(incident.severity),
                            mt: 0.75,
                            flexShrink: 0,
                        }}
                    />

                    {/* Content Stack */}
                    <Stack sx={{ flexGrow: 1, minWidth: 0, gap: 0.5 }}>
                        {/* Title Row */}
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}>
                            <Typography
                                variant="body2"
                                sx={{
                                    fontWeight: 500,
                                    color: "text.primary",
                                    lineHeight: 1.4,
                                }}
                            >
                                {incident.title}
                            </Typography>

                            {incident.aiAnalysis && (
                                <Box
                                    sx={{
                                        display: "inline-flex",
                                        alignItems: "center",
                                        gap: 0.5,
                                        px: 1,
                                        py: 0.25,
                                        borderRadius: 1,
                                        border: "1px solid",
                                        borderColor: "rgba(167, 139, 250, 0.25)",
                                        backgroundColor: "rgba(124, 58, 237, 0.08)",
                                        color: "primary.light",
                                        fontSize: "0.6875rem",
                                        fontWeight: 600,
                                        lineHeight: 1,
                                    }}
                                >
                                    ★ AI
                                </Box>
                            )}
                        </Box>

                        {/* AI Analysis Description */}
                        {incident.aiAnalysis && (
                            <Typography
                                variant="caption"
                                sx={{
                                    color: "primary.light",
                                    opacity: 0.85,
                                    fontSize: "0.75rem",
                                    lineHeight: 1.4,
                                    textOverflow: "ellipsis",
                                    overflow: "hidden",
                                    whiteSpace: "nowrap",
                                    maxWidth: "100%",
                                }}
                            >
                                {incident.aiAnalysis}
                            </Typography>
                        )}

                        {/* Metadata Row */}
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mt: 0.5 }}>
                            {/* Status Badge */}
                            <Box
                                sx={{
                                    px: 1,
                                    py: 0.5,
                                    borderRadius: "4px",
                                    fontSize: "0.75rem",
                                    fontWeight: 500,
                                    lineHeight: 1,
                                    ...getStatusBadgeStyles(incident.status),
                                }}
                            >
                                {formatStatusLabel(incident.status)}
                            </Box>

                            {/* Incident ID */}
                            <Typography
                                variant="caption"
                                sx={{
                                    color: "text.secondary",
                                    opacity: 0.6,
                                    fontWeight: 500,
                                    fontSize: "0.75rem",
                                }}
                            >
                                {incident.id}
                            </Typography>

                            {/* Time ago */}
                            <Typography
                                variant="caption"
                                sx={{
                                    color: "text.secondary",
                                    opacity: 0.6,
                                    fontSize: "0.75rem",
                                }}
                            >
                                {incident.started}
                            </Typography>
                        </Box>
                    </Stack>
                </Box>
            ))}
        </Stack>
    );
}