import { useMutation, useQueryClient } from "@tanstack/react-query";
import { organizationService } from "../services/organization.service";
import { CreateOrganizationSchema } from "../schema/organization.schema";
import { organizationKeys } from "./organization.query-keys";
import { useToast } from "@/components/common/useToast";

export function useCreateOrganization() {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    return useMutation({
        mutationFn: (data: CreateOrganizationSchema) => organizationService.createOrganization(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: organizationKeys.all });
            toast({
                title: "Organization created successfully",
                variant: "success",
            });
        },
        onError: (error) => {
            toast({
                title: "Failed to create organization",
                description: error.message,
                variant: "error",
            });
        },
    });
}
