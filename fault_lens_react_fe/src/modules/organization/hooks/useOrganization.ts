import { useQuery } from "@tanstack/react-query";
import { organizationService } from "../services/organization.service";
import { organizationKeys } from "./organization.query-keys";

export function useOrganization(
  organizationId: string
) {
  return useQuery({
    queryKey: organizationKeys.detail(
      organizationId
    ),

    queryFn: () =>
      organizationService.fetchOrganization(
        organizationId
      ),

    enabled: Boolean(organizationId),

    staleTime: 5 * 60 * 1000,
  });
}