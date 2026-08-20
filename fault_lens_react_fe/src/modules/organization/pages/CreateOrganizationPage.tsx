import CreateOrganizationForm from "../components/CreateOrganizationForm"
import { Container, Stack } from "@mui/material";
import { PageHeader } from "@/components/common";

export default function CreateOrganizationPage() {
    return (
        <Container maxWidth="lg">

            <PageHeader
                title="Create Organization"
                subtitle="Create a new organization to get started"
            />

            <Stack
                sx={{
                    mt: 3,
                }}
            >
                <CreateOrganizationForm />
            </Stack>
        </Container>
    )
}