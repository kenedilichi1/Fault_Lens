import {
    Alert,
    CircularProgress,
    Container,
    Stack,
} from "@mui/material";

import {
    Navigate,
    Outlet,
    useParams,
} from "react-router-dom";

import { useOrganization } from "../hooks/useOrganization";

import OrganizationBreadcrumbs from "../components/OrganizationBreadCrumb";
import OrganizationTabs from "../components/OrganizationTabs";

export default function OrganizationDetailsLayout() {
    const { organizationId } = useParams();

    if (!organizationId) {
        return <Navigate to="/organizations" />;
    }

    const {
        data: organization,
        isLoading,
        isError,
    } = useOrganization(organizationId);

    if (isLoading) {
        return (
            <Stack
                sx={{
                    alignItems: "center",
                    py: 10,
                }}
            >
                <CircularProgress />
            </Stack>
        );
    }

    if (isError || !organization) {
        return (
            <Container maxWidth="lg">
                <Alert severity="error">
                    Organization could not be found.
                </Alert>
            </Container>
        );
    }

    return (
        <Container maxWidth="lg">
            <OrganizationBreadcrumbs
                organization={organization}
            />

            <OrganizationTabs
                organizationId={organization.id}
            />

            <Outlet
                context={{
                    organization,
                }}
            />
        </Container>
    );
}