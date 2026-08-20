import {
    Breadcrumbs,
    Link,
    Typography,
} from "@mui/material";

import NavigateNextIcon from "@mui/icons-material/NavigateNext";

import {
    Link as RouterLink,
} from "react-router-dom";

import type { Organization } from "../types/organization.types";

interface Props {
    organization: Organization;
}

export default function OrganizationBreadcrumbs({
    organization,
}: Props) {
    return (
        <Breadcrumbs
            separator={
                <NavigateNextIcon fontSize="small" />
            }
            sx={{ mb: 3 }}
        >
            <Link
                component={RouterLink}
                to="/organizations"
                underline="hover"
                color="inherit"
            >
                Organizations
            </Link>

            <Typography color="text.primary">
                {organization.name}
            </Typography>
        </Breadcrumbs>
    );
}