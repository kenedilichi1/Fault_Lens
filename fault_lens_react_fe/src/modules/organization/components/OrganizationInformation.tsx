import { Chip, Paper, Stack, Typography } from "@mui/material";

import type { Organization } from "../types/organization.types";
import InfoRow from "./InfoRow";

interface Props {
  organization: Organization;
}

export default function OrganizationInformation({ organization }: Props) {
  return (
    <Paper
      variant="outlined"
      sx={{
        borderRadius: 2,
        p: 2.5,
        height: "100%",
      }}
    >
      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2.5 }}>
        Organization Information
      </Typography>

      <Stack spacing={1.75}>
        <InfoRow label="Name">{organization.name}</InfoRow>

        <InfoRow label="Slug">{organization.slug}</InfoRow>

        <InfoRow label="Timezone">{organization.timezone}</InfoRow>

        <InfoRow label="Plan">{organization.plan}</InfoRow>

        <InfoRow label="Status">
          <Chip
            label={organization.status}
            color={organization.status === "ACTIVE" ? "success" : "default"}
            sx={{
              height: 25,
              fontSize: 11,
              fontWeight: 600,
            }}
          />
        </InfoRow>

        <InfoRow label="Created">
          {new Date(organization.created_at).toLocaleDateString()}
        </InfoRow>

        <InfoRow label="Owner">{organization.owner.email}</InfoRow>
      </Stack>
    </Paper>
  );
}
