import { AppButton } from "@/components/common";
import {
    FormControl,
    MenuItem,
    Paper,
    Select,
    Stack,
    TextField,
    Typography,
} from "@mui/material";
import { useState } from "react";
import TimezoneSelect from "react-timezone-select";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { CreateOrganizationSchema } from "../schema/organization.schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCreateOrganization } from "../hooks/useCreateOrganization";

export default function CreateOrganizationForm() {
    const navigate = useNavigate();

    const [timezone, setTimezone] = useState({
        value: "Africa/Lagos",
        label: "Africa/Lagos",
    });

    const [plan, setPlan] = useState("");

    const createOrganizationMutation = useCreateOrganization();


    const {
        register,
        handleSubmit,
        setValue,
        formState: { errors },
    } = useForm<CreateOrganizationSchema>({
        resolver: zodResolver(CreateOrganizationSchema),
        defaultValues: {
            timezone: "Africa/Lagos",
        },
    })

    const onSubmit = (values: CreateOrganizationSchema) => {
        createOrganizationMutation.mutate(values, {
            onSuccess: () => {
                navigate("/organizations");
            },
        });
    };

    return (
        <Paper
            component="form"
            onSubmit={handleSubmit(onSubmit)}
            sx={{
                width: "100%",
                p: { xs: 2, sm: 3 },
            }}
        >
            <Stack spacing={4}>
                <Stack spacing={2}>
                    <Typography >
                        Organization Information
                    </Typography>

                    <TextField
                        {...register("name")}
                        placeholder="e.g. Kabuto Enterprises"
                        variant="outlined"
                        fullWidth
                        required
                        error={!!errors.name}
                        helperText={errors.name?.message}
                    />

                    <Stack spacing={1}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                            Timezone
                        </Typography>

                        <TimezoneSelect
                            value={timezone}
                            onChange={(value) => {
                                setTimezone(value);
                                setValue("timezone", value.value, { shouldValidate: true, shouldDirty: true });
                            }}

                        />
                    </Stack>
                </Stack>

                <Stack spacing={2}>

                    <FormControl fullWidth>
                        <Typography id="organization-plan-label">
                            Plan
                        </Typography>

                        <Select
                            labelId="organization-plan-label"
                            value={plan}
                            onChange={(event) => {
                                const value = event.target.value;

                                setPlan(value);

                                setValue("plan", value as CreateOrganizationSchema['plan'], {
                                    shouldValidate: true,
                                    shouldDirty: true,
                                });
                            }}
                        >
                            <MenuItem value="free">Free</MenuItem>
                            <MenuItem value="pro">Pro</MenuItem>
                        </Select>
                    </FormControl>
                </Stack>

                <Stack
                    direction={{ xs: "column-reverse", sm: "row" }}
                    spacing={2}
                    sx={{ justifyContent: "flex-end" }}
                >
                    <AppButton
                        variant="outlined"
                        color="inherit"
                        type="button"
                        onClick={() => navigate(-1)}
                    >
                        Cancel
                    </AppButton>

                    <AppButton
                        variant="contained"
                        color="secondary"
                        type="submit"
                        loading={createOrganizationMutation.isPending}
                    >
                        Create Organization
                    </AppButton>
                </Stack>
            </Stack>
        </Paper>
    );
}