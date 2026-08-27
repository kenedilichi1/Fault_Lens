
type Env = "development" | "production" | "staging" | "test" | "preprod" | "qa";
type Status = "healthy" | "degraded" | "warning" | "critical";

export type Service = {
    name: string;
    env: Env;
    status: Status;
    latency: string;
    errorRate: string;
    uptime: string;
};

export const services: Service[] = [
    { name: "API Gateway", env: "production", status: "healthy" as const, latency: "142ms", errorRate: "0.12%", uptime: "99.99%" },
    { name: "Auth Service", env: "production", status: "healthy" as const, latency: "38ms", errorRate: "0.04%", uptime: "100%" },
    { name: "Payment Service", env: "production", status: "degraded" as const, latency: "521ms", errorRate: "1.8%", uptime: "99.71%" },
    { name: "Notification Service", env: "production", status: "healthy" as const, latency: "29ms", errorRate: "0.09%", uptime: "100%" },
    { name: "Worker", env: "production", status: "warning" as const, latency: "890ms", errorRate: "0.62%", uptime: "99.84%" },
    { name: "Database", env: "production", status: "healthy" as const, latency: "4ms", errorRate: "0.00%", uptime: "100%" },
];