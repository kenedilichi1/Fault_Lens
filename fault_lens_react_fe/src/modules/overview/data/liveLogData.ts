
type LogLevel = "ERROR" | "WARN" | "INFO";
export interface LiveLog {
    ts: string;
    level: LogLevel;
    service: string;
    msg: string;
}
export const logSamples: LiveLog[] = [
    { ts: "2026-08-20T14:32:18.441Z", level: "ERROR", service: "payment-service", msg: 'Stripe API timeout after 5000ms requestId="req_9Kx2mNpL"' },
    { ts: "2026-08-20T14:32:17.882Z", level: "WARN", service: "worker", msg: "Queue depth exceeded threshold queue=email_dispatch depth=4821" },
    { ts: "2026-08-20T14:32:16.109Z", level: "INFO", service: "api-gateway", msg: 'Request completed status=200 path=/v1/users latency=138ms traceId="4a9f..."' },
    { ts: "2026-08-20T14:32:15.661Z", level: "ERROR", service: "auth-service", msg: 'Token validation failed reason="expired" userId="usr_0xAB91"' },
    { ts: "2026-08-20T14:32:14.009Z", level: "INFO", service: "notification-service", msg: "Email dispatched to=1 template=invoice_paid duration=42ms" },
    { ts: "2026-08-20T14:32:13.724Z", level: "WARN", service: "payment-service", msg: "Retry attempt 2/3 for payment processor endpoint=stripe.charges.create" },
];