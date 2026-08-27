import { Box } from "@mui/material";

export default function Sparkline({
    data = [],
    color = "#22C55E",
}: {
    readonly data?: number[];
    readonly color?: string;
}) {
    if (data.length < 2) {
        return null;
    }

    const width = 60;
    const height = 30;
    const padding = 1;

    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;

    const points = data
        .map((value, index) => {
            const x =
                padding +
                (index / (data.length - 1)) *
                (width - padding * 2);

            const y =
                height -
                padding -
                ((value - min) / range) *
                (height - padding * 2);

            return `${x},${y}`;
        })
        .join(" ");

    return (
        <Box
            component="svg"
            viewBox={`0 0 ${width} ${height}`}
            sx={{
                width,
                height,
                overflow: "visible",
            }}
        >
            <polyline
                points={points}
                fill="none"
                stroke={color}
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </Box>
    );
}