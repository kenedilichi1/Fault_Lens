import { useMutation, useQueryClient } from "@tanstack/react-query";

import { organizationService } from "../services/organization.service";
import { organizationKeys } from "./organization.query-keys";
import { UpdateOrganizationPayload } from "../types/organization.types";

export function useUpdateOrganization() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      organizationId,
      payload,
    }: {
      organizationId: string;
      payload: Partial<UpdateOrganizationPayload>
    }) =>
      organizationService.update(
        organizationId,
        payload
      ),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: organizationKeys.detail(
          variables.organizationId
        ),
      });
    },
  });
}