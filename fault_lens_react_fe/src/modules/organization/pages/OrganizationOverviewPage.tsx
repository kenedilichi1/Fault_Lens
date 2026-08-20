import { Grid } from "@mui/material";
import { useNavigate, useOutletContext } from "react-router-dom";

import type { Organization } from "../types/organization.types";

import OrganizationOverviewHeader from "../components/OrganizationOverviewHeader";
import OrganizationInformation from "../components/OrganizationInformation";
import MembersSummary from "../components/MembersSummary";

import { useOrganizationUIStore } from "../store/organization.store";

interface OutletContext {
  organization: Organization;
}

export default function OrganizationOverviewPage() {
  const { organization } =
    useOutletContext<OutletContext>();

  const navigate = useNavigate();

  const openEditDialog =
    useOrganizationUIStore(
      (state) => state.openEditDialog
    );

  return (
    <>
      <OrganizationOverviewHeader
        organization={organization}
        onEdit={openEditDialog}
      />

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, md: 8 }}>
          <OrganizationInformation
            organization={organization}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <MembersSummary
            organization={organization}
            onViewMembers={() =>
              navigate(
                `/organizations/${organization.id}/members`
              )
            }
          />
        </Grid>
      </Grid>
    </>
  );
}