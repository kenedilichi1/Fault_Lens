import { useQuery } from "@tanstack/react-query";
import { organizationService } from "../services/organization.service";
import { organizationKeys } from "./organization.query-keys";

export function useOrganizationMembers(
  organizationId: string
) {
  return useQuery({
    queryKey: organizationKeys.members(
      organizationId
    ),

    queryFn: () =>
      organizationService.getMembers(
        organizationId
      ),

    enabled: Boolean(organizationId),

    staleTime: 2 * 60 * 1000,
  });
}