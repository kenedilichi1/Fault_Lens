import Grid from "@mui/material/Grid";
import BugReportOutlinedIcon from "@mui/icons-material/BugReportOutlined";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";

import { PageHeader } from "@/components/common/PageHeader";
import { StatCard } from "@/components/common/StatCard";
import { SectionCard } from "@/components/common/SectionCard";

export default function DashboardPage() {
    return (
        <>
            <PageHeader
                title="Dashboard"
                subtitle="Monitor your systems and investigate incidents."
            />

            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6, lg: 3 }}>
                    <StatCard
                        title="Projects"
                        value={8}
                        subtitle="2 active today"
                        icon={<FolderOutlinedIcon />}
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 6, lg: 3 }}>
                    <StatCard
                        title="Active Incidents"
                        value={3}
                        subtitle="+1 this hour"
                        icon={<BugReportOutlinedIcon />}
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 6, lg: 3 }}>
                    <StatCard
                        title="Logs Today"
                        value="1.2M"
                        subtitle="+12%"
                        icon={<DescriptionOutlinedIcon />}
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 6, lg: 3 }}>
                    <StatCard
                        title="Alert Rules"
                        value={15}
                        subtitle="12 enabled"
                        icon={<NotificationsOutlinedIcon />}
                    />
                </Grid>
            </Grid>

            <Grid container spacing={3} sx={{ mt: 3 }}>
                <Grid size={{ xs: 12, lg: 7 }}>
                    <SectionCard title="Recent Incidents">
                        Coming Soon...
                    </SectionCard>
                </Grid>

                <Grid size={{ xs: 12, lg: 5 }}>
                    <SectionCard title="Log Volume">
                        Chart goes here...
                    </SectionCard>
                </Grid>

                <Grid size={12}>
                    <SectionCard title="Recent Logs">
                        Table goes here...
                    </SectionCard>
                </Grid>
            </Grid>
        </>
    );
}