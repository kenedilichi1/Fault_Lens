import Grid from "@mui/material/Grid";
import { PageHeader, StatCard, SectionCard, ActionWidget } from "@/components/common";
import { statCards } from "../data/statsData";
import ServicesOverview from "../components/ServicesOverview";
import RecentIncidents from "../components/RecentIncidents";
import LiveLogs from "../components/LiveLogs";

export default function OverviewPage() {
    return (
        <>
            <PageHeader
                title="Overview"
                subtitle="System health across all services · Updated just now"
            />

            <Grid container spacing={1.5}>
                {statCards.map((stat) => (
                    <Grid
                        key={stat.title}
                        size={{
                            xs: 12,
                            sm: 6,
                            md: 4,
                            lg: 2,
                        }}
                    >
                        <StatCard {...stat} />
                    </Grid>
                ))}
            </Grid>

            <Grid container spacing={3} sx={{ mt: 3 }}>
                <Grid size={{ xs: 12, md: 8, }}>
                    <SectionCard
                        title="Services"
                        actions={<ActionWidget to="/services" />}
                    >
                        <ServicesOverview />
                    </SectionCard>
                </Grid>

                <Grid size={{ xs: 12, md: 4, }}>
                    <SectionCard title="Recent Incidents" actions={<ActionWidget to="/incidents" />}>
                        <RecentIncidents />
                    </SectionCard>
                </Grid>

                <Grid size={12}>
                    <SectionCard title="Live Log Stream" isLive={true} actions={<ActionWidget label="Open Logs" to="/logs" />}>
                        <LiveLogs />
                    </SectionCard>
                </Grid>
            </Grid>
        </>
    );
}