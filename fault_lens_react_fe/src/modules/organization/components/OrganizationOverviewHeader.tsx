import { Box, Chip, Stack, Typography } from "@mui/material";

import EditIcon from "@mui/icons-material/Edit";

import type { Organization } from "../types/organization.types";
import { AppButton } from "@/components/common";

interface Props {
  organization: Organization;
  onEdit: () => void;
}

export default function OrganizationOverviewHeader({
  organization,
  onEdit,
}: Props) {

  console.log(organization.role, "Role")
  return (
    <Stack
      direction={{
        xs: "column",
        sm: "row",
      }}

      sx={{
        justifyContent: "space-between",
        gap: 2,
        mb: 3,
        alignItems: {
          xs: "stretch",
          sm: "center",
        },
      }}
    >
      <Box>
        <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            {organization.name}
          </Typography>

          <Chip
            label={organization.role}
            size="small"
            color="secondary"
            sx={{
              height: 22,
              fontSize: 10,
              fontWeight: 700,
            }}
          />
        </Stack>

        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }} >
          {organization.slug}
        </Typography>
      </Box>

      <AppButton variant="outlined" startIcon={<EditIcon />} onClick={onEdit}>
        Edit Organization
      </AppButton>
    </Stack>
  );
}
