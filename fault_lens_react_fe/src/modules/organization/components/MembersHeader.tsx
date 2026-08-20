import {
    Box,
    Stack,
    Typography,
} from "@mui/material";

import PersonAddIcon from "@mui/icons-material/PersonAdd";

import { AppButton } from "@/components/common";

interface Props {
    onAddMember: () => void;
}

export default function MembersHeader({
    onAddMember,
}: Props) {
    return (
        <Stack
            direction={{
                xs: "column",
                sm: "row",
            }}
            sx={{
                justifyContent: "space-between",
                alignItems: {
                    xs: "stretch",
                    sm: "center",
                },
                gap: 2,
                mb: 3,
            }}
        >
            <Box>
                <Typography
                    variant="h5"
                    sx={{
                        fontWeight: 600,
                    }}
                >
                    Members
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                        mt: 0.5,
                    }}
                >
                    Manage the members of this organization
                </Typography>
            </Box>

            <AppButton
                startIcon={<PersonAddIcon />}
                onClick={onAddMember}
            >
                Add Member
            </AppButton>
        </Stack>
    );
}