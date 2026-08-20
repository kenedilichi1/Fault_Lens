import {
  Avatar,
  Box,
  Chip,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableContainer,
  TableHead,
  Typography,
} from "@mui/material";

import { StyledTableCell, StyledTableRow } from "../styles/MembersTable.styles";

import type { OrganizationMember } from "../types/organization.types";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import type { ReactElement } from "react";

interface Props {
  readonly members: readonly OrganizationMember[];
}

export default function MembersTable({ members }: Readonly<Props>): ReactElement {
  return (
    <TableContainer component={Paper} variant="outlined">
      <Table>
        <TableHead>
          <StyledTableRow>
            <StyledTableCell>Member</StyledTableCell>
            <StyledTableCell>Role</StyledTableCell>
            <StyledTableCell>Status</StyledTableCell>
            <StyledTableCell>Joined</StyledTableCell>
            <StyledTableCell>Action</StyledTableCell>
          </StyledTableRow>
        </TableHead>

        <TableBody>
          {members.map((member) => (
            <StyledTableRow key={member.id}>
              <StyledTableCell>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1.5,
                  }}
                >
                  <Avatar
                    src={member.user.avatar_url}
                    sx={{
                      width: 50,
                      height: 50,
                    }}
                  >
                    {member.user.full_name.charAt(0)}
                  </Avatar>

                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {member.user.full_name}
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                      {member.user.email}
                    </Typography>
                  </Box>
                </Box>
              </StyledTableCell>

              <StyledTableCell>
                <Chip label={member.role} size="small" />
              </StyledTableCell>

              <StyledTableCell>
                <Chip
                  label={member.status}
                  size="small"
                  color={member.status === "ACTIVE" ? "success" : "default"}
                />
              </StyledTableCell>

              <StyledTableCell>
                {new Date(member.created_at).toLocaleDateString()}
              </StyledTableCell>

              <StyledTableCell>
                <IconButton
                  size="small"
                  onClick={() => {
                    // open menu for this member
                  }}
                >
                  <MoreHorizIcon />
                </IconButton>
              </StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
