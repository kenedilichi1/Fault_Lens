import {
  Container,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import { EmptyState } from "@/components/common/EmptyState";
import BusinessIcon from "@mui/icons-material/Business";
import { AppButton, FullPageLoader, PageHeader } from "@/components/common";
import AddIcon from "@mui/icons-material/Add";
import OrganizationCard from "./OrganizationCard";
import { useNavigate } from "react-router-dom";
import { useOrganizations } from "../hooks/useOrganizations";

export default function OrganizationList() {
  const navigate = useNavigate();
  const { data: organizations, isPending } = useOrganizations();

  const handleViewOrg = (id: string) => {
    navigate(`/organizations/${id}`);
  };

  return (
    <Container maxWidth="lg">
      <Grid
        container
        spacing={2}
        sx={{
          justifyContent: "space-between",
          alignItems: "center",
          flexDirection: { xs: "column", sm: "row" },
          mb: 3,
        }}
      >
        <Grid size={{ xs: 12, sm: "auto" }}>
          <PageHeader
            title="Organizations"
            subtitle="Manage your organizations and their members."
          />
        </Grid>

        <Grid size={{ xs: 12, sm: "auto" }}>
          <AppButton
            variant="contained"
            color="secondary"
            onClick={() => navigate("/organizations/new")}
            startIcon={<AddIcon />}
            fullWidth={false}
            sx={{ display: !organizations || organizations.length === 0 ? 'none' : 'flex' }}
          >
            Create Organization
          </AppButton>
        </Grid>
      </Grid>

      {isPending ? (
        <Stack sx={{
          alignItems: "center", py: 10
        }}>
          <FullPageLoader />
        </Stack>
      ) : !organizations || organizations.length === 0 ? (
        <EmptyState
          title="No organization yet"
          description="You haven't created or joined any organization"
          icon={<BusinessIcon />}
          action={
            <AppButton
              variant="contained"
              color="secondary"
              onClick={() => navigate("/organizations/new")}
              startIcon={<AddIcon />}
              fullWidth={false}
            >
              Create Organization
            </AppButton>
          }
        />
      ) : (
        <>
          <Stack
            sx={{
              border: "1px solid",
              borderColor: "divider",
              borderRadius: 2,
              overflow: "hidden",
            }}
          >
            {organizations.map((org, index) => (
              <OrganizationCard
                key={org.organization_id}
                org={org}
                index={index}
                dataLength={organizations.length}
                handleViewOrg={handleViewOrg}
              />
            ))}
          </Stack>

          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ display: "block", mt: 1 }}
          >
            Showing {organizations.length} organizations
          </Typography>
        </>
      )}
    </Container>
  );
}