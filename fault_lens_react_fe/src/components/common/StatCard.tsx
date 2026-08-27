import type { ReactNode } from "react";

import { Box, Card, CardContent, Typography } from "@mui/material";

import Sparkline from "./Sparkline";

type StatCardProps = {
  readonly title: string;
  readonly value: string | number;
  readonly subtitle?: string;
  readonly icon?: ReactNode;

  readonly trend?: {
    value: string;
    positive?: boolean;
  };

  readonly status?: "healthy" | "warning" | "critical" | "neutral";

  readonly sparkline?: number[];
};

const statusColors = {
  healthy: "#22C55E",
  warning: "#F59E0B",
  critical: "#EF4444",
  neutral: "#71717A",
} as const;

export function StatCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  status = "neutral",
  sparkline,
}: StatCardProps) {
  const statusColor = statusColors[status];

  const trendColor = trend?.positive === false ? "#EF4444" : "#22C55E";

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: "16px",
        border: "1px solid",
        borderColor: "#34313C",
        backgroundColor: "#201E26",
        boxShadow: "none",
        height: 140,

      }}
    >
      <CardContent
        sx={{
          height: "100%",
          boxSizing: "border-box",
          p: 1.5,

          "&:last-child": {
            pb: 1.5,
          },
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Typography
            sx={{
              fontSize: "body2.fontSize",
              lineHeight: 1.25,
              fontWeight: 500,
              color: "#9490A0",
            }}
          >
            {title}
          </Typography>

          {icon ?? (
            <Box
              sx={{
                width: 12,
                height: 12,
                flexShrink: 0,
                borderRadius: "50%",
                backgroundColor: statusColor,
              }}
            />
          )}
        </Box>

        {/* Main value */}
        <Typography
          sx={{
            mt: 2.75,
            lineHeight: 1,
            fontSize: "h3.fontSize",
            fontWeight: 600,
            letterSpacing: "-0.04em",
            color: "#F1F0F5",
          }}
        >
          {value}
        </Typography>

        {/* Subtitle */}
        {subtitle && (
          <Typography
            sx={{
              mt: 1,
              fontSize: "caption.fontSize",
              lineHeight: 1.25,
              fontWeight: 400,
              color: "#686473",
            }}
          >
            {subtitle}
          </Typography>
        )}

        {/* Bottom section */}
        {(sparkline || trend) && (
          <Box
            sx={{
              mt: "auto",

              display: "flex",
              alignItems: "flex-end",
              justifyContent: "space-between",
              gap: 2,
            }}
          >
            {sparkline ? (
              <Box
                sx={{
                  width: 125,
                  height: 20,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <Sparkline data={sparkline} color={trendColor} />
              </Box>
            ) : (
              <Box />
            )}

            {trend && (
              <Typography
                sx={{
                  fontSize: "16px",
                  lineHeight: 1,
                  fontWeight: 500,
                  color: trendColor,
                  whiteSpace: "nowrap",
                }}
              >
                {trend.value}
              </Typography>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
