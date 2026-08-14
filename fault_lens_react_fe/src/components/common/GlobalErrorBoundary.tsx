import { useRouteError, isRouteErrorResponse, Link } from "react-router-dom";
import { Box, Typography, Button } from "@mui/material";

export function GlobalErrorBoundary() {
    const error = useRouteError();
    console.error(error);

    let errorMessage = "An unexpected error occurred.";
    if (isRouteErrorResponse(error)) {
        errorMessage = error.statusText || error.data?.message || "Not Found";
    } else if (error instanceof Error) {
        errorMessage = error.message;
    }

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
                p: 3,
                textAlign: "center",
            }}
        >
            <Typography variant="h4" color="error" gutterBottom>
                Oops! Something went wrong.
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                {errorMessage}
            </Typography>
            <Button variant="contained" component={Link} to="/">
                Return to Home
            </Button>
        </Box>
    );
}
