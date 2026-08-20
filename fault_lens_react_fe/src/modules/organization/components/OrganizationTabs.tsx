import {
    Tab,
    Tabs,
} from "@mui/material";

import {
    Link as RouterLink,
    useLocation,
} from "react-router-dom";

interface Props {
    organizationId: string;
}

export default function OrganizationTabs({
    organizationId,
}: Props) {
    const location = useLocation();

    const basePath =
        `/organizations/${organizationId}`;

    const pathParts = location.pathname.split("/");
    const lastPart = pathParts[pathParts.length - 1];
    const currentTab = lastPart === organizationId ? "overview" : (lastPart || "overview");

    return (
        <Tabs
            value={currentTab}
            sx={{
                borderBottom: 1,
                borderColor: "divider",
                mb: 3,
            }}
        >
            <Tab
                label="Overview"
                value="overview"
                component={RouterLink}
                to={`${basePath}/overview`}
            />

            <Tab
                label="Members"
                value="members"
                component={RouterLink}
                to={`${basePath}/members`}
            />

            <Tab
                label="Settings"
                value="settings"
                component={RouterLink}
                to={`${basePath}/settings`}
            />

            <Tab
                label="Billing"
                value="billing"
                component={RouterLink}
                to={`${basePath}/billing`}
            />
        </Tabs>
    );
}