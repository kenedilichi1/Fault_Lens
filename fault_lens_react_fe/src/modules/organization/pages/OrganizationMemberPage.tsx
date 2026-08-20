import {
    Alert,
    CircularProgress,
    Stack,
} from "@mui/material";

import { useParams } from "react-router-dom";

import { useOrganizationMembers } from "../hooks/useOrganizationMembers";

import MembersTable from "../components/MembersTable";

import { useOrganizationUIStore } from "../store/organization.store";
import MembersHeader from "../components/MembersHeader";


export default function OrganizationMembersPage() {
    const { organizationId } =
        useParams<{ organizationId: string }>();


    const openInviteDialog =
        useOrganizationUIStore(
            (state) => state.openInviteDialog
        );

    const {
        data: members = [],
        isLoading,
        isError,
    } = useOrganizationMembers(
        organizationId!
    );

    return (
        <>
            <MembersHeader
                onAddMember={openInviteDialog}
            />

            {isLoading && (
                <Stack
                    sx={{
                        alignItems: "center",
                        py: 5,
                    }}
                >
                    <CircularProgress />
                </Stack>
            )}

            {isError && (
                <Alert severity="error">
                    Failed to load members.
                </Alert>
            )}

            {!isLoading && !isError && (
                <MembersTable
                    members={members}
                />
            )}
        </>
    );
}