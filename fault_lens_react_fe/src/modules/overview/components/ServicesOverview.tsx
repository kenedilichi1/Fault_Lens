import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { services } from "../data/servicesData";
import { formatStatusLabel, getErrorRateColor, getStatusColor, } from "../utils";



export default function ServicesOverview() {
    return (
        <TableContainer>
            <Table size="small">
                <TableHead>
                    <TableRow
                        sx={{
                            "& th": {
                                color: "text.secondary",
                                fontWeight: 500,
                                fontSize: "0.8125rem",
                                borderBottom: 1,
                                borderColor: "divider",
                                py: 1.5,
                                "&:first-of-type": { pl: 0 },
                                "&:last-of-type": { pr: 0 },
                            }
                        }}
                    >
                        <TableCell>Service</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Latency</TableCell>
                        <TableCell>Error Rate</TableCell>
                        <TableCell>Uptime</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody
                    sx={{
                        "& td": {
                            py: 1.75,
                            borderBottom: 1,
                            borderColor: "divider",
                            fontSize: "0.875rem",
                            "&:first-of-type": { pl: 0 },
                            "&:last-of-type": { pr: 0 },
                            cursor: "pointer",
                            transition: "all 0.2s ease",
                        },
                        "& tr:hover": {
                            backgroundColor: "action.hover",
                        },
                        "& tr:last-child td": {
                            borderBottom: 0,
                        }
                    }}
                >
                    {services.map((ser) => (
                        <TableRow key={ser.name}>
                            <TableCell sx={{ color: "text.primary", fontWeight: 600 }}>
                                {ser.name}
                            </TableCell>
                            <TableCell>
                                <Box sx={{ display: "flex", alignItems: "center" }}>
                                    <Box
                                        sx={{
                                            width: 6,
                                            height: 6,
                                            borderRadius: "50%",
                                            backgroundColor: getStatusColor(ser.status),
                                            mr: 1.25,
                                        }}
                                    />
                                    <Typography
                                        variant="body2"
                                        component="span"
                                        sx={{
                                            color: getStatusColor(ser.status),
                                            fontWeight: 500,
                                            fontSize: "inherit",
                                        }}
                                    >
                                        {formatStatusLabel(ser.status)}
                                    </Typography>
                                </Box>
                            </TableCell>
                            <TableCell sx={{ color: "text.secondary" }}>
                                {ser.latency}
                            </TableCell>
                            <TableCell sx={{ color: getErrorRateColor(ser.errorRate), fontWeight: 500 }}>
                                {ser.errorRate}
                            </TableCell>
                            <TableCell sx={{ color: "text.secondary" }}>
                                {ser.uptime}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}