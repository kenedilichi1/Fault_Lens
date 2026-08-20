import z from "zod";

export const CreateOrganizationSchema = z.object({
    name: z.string().min(3, "Organization name must be at least 3 characters"),
    timezone: z.string().min(3, "Timezone is required"),
    plan: z.enum(["free", "pro"]),
});

export type CreateOrganizationSchema = z.infer<typeof CreateOrganizationSchema>;