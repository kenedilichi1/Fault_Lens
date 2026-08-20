import {
  Box,
  Button,
  Card,
  CardActions,
  Stack,
  Typography,
} from "@mui/material";

import type { Organization } from "../types/organization.types";
import InfoRow from "./InfoRow";

interface Props {
  organization: Organization;
  onViewMembers: () => void;
}

export default function MembersSummary({ organization, onViewMembers }: Props) {
  const { total_members, owners, admins, members, viewers } =
    organization.member_summary;

  return (
    <Card
      variant="outlined"
      sx={{
        borderRadius: 2,
        p: 2,
        height: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
        Member Summary
      </Typography>

      <Box sx={{ mb: 2.5 }}>
        <Typography
          sx={{
            fontSize: 28,
            lineHeight: 1.2,
            fontWeight: 500,
          }}
        >
          {total_members}
        </Typography>

        <Typography variant="body2" color="text.secondary">
          Members
        </Typography>
      </Box>

      <Stack spacing={1.5}>
        <InfoRow label="Owners">{owners}</InfoRow>

        <InfoRow label="Admins">{admins}</InfoRow>

        <InfoRow label="Members">{members}</InfoRow>

        <InfoRow label="Viewers">{viewers}</InfoRow>
      </Stack>

      <CardActions
        sx={{
          p: 0,
          mt: "auto",
          pt: 2.5,
        }}
      >
        <Button
          color="secondary"
          variant="outlined"
          fullWidth
          onClick={onViewMembers}
        >
          View all members
        </Button>
      </CardActions>
    </Card>
  );
}
