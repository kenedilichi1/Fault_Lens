

type Severity = "critical" | "warning" | "info" | "resolved";
type Status = "open" | "investigating" | "resolved";

export interface Incident {
    id: string;
    title: string;
    severity: Severity;
    status: Status;
    started: string;
    services: string[];
    aiAnalysis: string | null;
}


export const recentIncidents: Incident[] = [
    {
        id: "INC-0341",
        title: "Payment Service elevated latency",
        severity: "critical" as const,
        status: "open" as const,
        started: "14 min ago",
        services: ["Payment Service"],
        aiAnalysis: "DB connection pool saturation after v2.14.1 deploy.",
    },
    {
        id: "INC-0340",
        title: "Worker queue backlog > threshold",
        severity: "warning" as const,
        status: "open" as const,
        started: "1h 22m ago",
        services: ["Worker"],
        aiAnalysis: null,
    },
    {
        id: "INC-0339",
        title: "Auth Service elevated 401 rate",
        severity: "critical" as const,
        status: "investigating" as const,
        started: "2h 7m ago",
        services: ["Auth Service", "API Gateway"],
        aiAnalysis: "JWT secret rotation out of sync with API Gateway cached key.",
    },
    {
        id: "INC-0338",
        title: "Notification Service cold start delay",
        severity: "info" as const,
        status: "resolved" as const,
        started: "6h ago",
        services: ["Notification Service"],
        aiAnalysis: null,
    },
];