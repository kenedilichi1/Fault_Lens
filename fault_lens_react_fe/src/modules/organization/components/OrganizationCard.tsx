import { getInitials } from "@/utils";
import {
  Avatar,
  Box,
  Chip,
  Divider,
  IconButton,
  Stack,
  Typography,
} from "@mui/material";
import PeopleIcon from "@mui/icons-material/People";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import LanguageIcon from "@mui/icons-material/Language";
import { OrganizationList } from "../types/organization.types";

type organizationCardProp = {
  org: OrganizationList;
  index: number;
  dataLength: number;
  handleViewOrg: (id: string) => void | Promise<void>;
};

export default function OrganizationCard({
  org,
  index,
  dataLength,
  handleViewOrg,
}: organizationCardProp) {

  console.log(org, "Organizationß")
  return (
    <Box key={org.organization_id} onClick={() => handleViewOrg(org.organization_id)}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
          px: 2,
          py: 2,
          cursor: "pointer",

          "&:hover": {
            bgcolor: "action.hover",
          },
        }}
      >
        {/* Avatar */}
        <Avatar
          variant="rounded"
          sx={{
            width: 44,
            height: 44,
            bgcolor: "primary.50",
            color: "primary.main",
            fontSize: 14,
            fontWeight: 600,
          }}
        >
          {getInitials(org.organization_name)}
        </Avatar>

        {/* Organization information */}
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography
            variant="body1"

            sx={{
              mb: 0.5,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              fontWeight: 600,
            }}
          >
            {org.organization_name}
          </Typography>

          {/* Metadata */}
          <Stack
            direction="row"
            spacing={2}
            sx={{
              alignItems: "center",
              flexWrap: "wrap",
            }}
            useFlexGap
          >
            <Stack direction="row" spacing={0.5} sx={{ alignItems: "center" }}>
              <PeopleIcon sx={{ fontSize: 15, color: "text.secondary" }} />

              <Typography variant="caption" color="text.secondary">
                {org.slug}
              </Typography>
            </Stack>

            <Stack direction="row" spacing={0.5} sx={{ alignItems: "center" }}>
              <LanguageIcon sx={{ fontSize: 15, color: "text.secondary" }} />

              <Typography variant="caption" color="text.secondary">
                {org.timezone}
              </Typography>
            </Stack>

            <Stack direction="row" spacing={0.5} sx={{ alignItems: "center" }}>
              <PeopleIcon sx={{ fontSize: 15, color: "text.secondary" }} />

              <Typography variant="caption" color="text.secondary">
                {org.member_count} members
              </Typography>
            </Stack>
          </Stack>
        </Box>

        {/* Role */}
        <Chip
          label={org.role}
          size="small"
          sx={{
            fontSize: 11,
            fontWeight: 600,
            height: 24,
            borderRadius: 1,
          }}
        />

        {/* Arrow */}
        <IconButton size="small">
          <ChevronRightIcon />
        </IconButton>
      </Box>

      {index < dataLength - 1 && <Divider />}
    </Box>
  );
}
