export const getSeverityColor = (severity: string) => {
    switch (severity) {
        case "critical":
            return "error.main";
        case "warning":
            return "warning.light";
        case "info":
            return "info.main";
        case "resolved":
            return "success.main";
        default:
            return "text.secondary";
    }
};

export const getStatusBadgeStyles = (status: string) => {
    switch (status) {
        case "open":
            return {
                backgroundColor: "rgba(239, 68, 68, 0.12)",
                color: "#EF4444",
            };
        case "investigating":
            return {
                backgroundColor: "rgba(217, 119, 6, 0.12)",
                color: "#D97706",
            };
        case "resolved":
            return {
                backgroundColor: "rgba(34, 197, 94, 0.12)",
                color: "#22C55E",
            };
        default:
            return {
                backgroundColor: "rgba(255, 255, 255, 0.08)",
                color: "text.secondary",
            };
    }
};

export const formatStatusLabel = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
};

export const getStatusColor = (status: string) => {
    switch (status) {
        case "healthy":
            return "success.light";
        case "warning":
            return "warning.light";
        case "degraded":
            return "warning.light";
        case "critical":
            return "error.light";
        default:
            return "text.secondary";
    }
};

export const getErrorRateColor = (errorRateStr: string) => {
    const val = parseFloat(errorRateStr.replace("%", ""));
    if (isNaN(val)) return "text.primary";
    if (val >= 1.0) return "error.light";
    if (val >= 0.15) return "warning.light";
    return "success.light";
};

export const getLevelBadgeStyles = (level: string) => {
    switch (level) {
        case "ERROR":
            return {
                backgroundColor: "rgba(239, 68, 68, 0.12)",
                color: "#F87171",
            };
        case "WARN":
            return {
                backgroundColor: "rgba(217, 119, 6, 0.12)",
                color: "#F59E0B",
            };
        case "INFO":
            return {
                backgroundColor: "rgba(59, 130, 246, 0.12)",
                color: "#60A5FA",
            };
        default:
            return {
                backgroundColor: "rgba(255, 255, 255, 0.08)",
                color: "text.secondary",
            };
    }
};