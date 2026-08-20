import { useQuery } from "@tanstack/react-query";
import { organizationService } from "../services/organization.service";
import { organizationKeys } from "./organization.query-keys";

export function useOrganizations() {
    return useQuery({
        queryKey: organizationKeys.all,
        queryFn: () => organizationService.fetchOrganizations(),
        staleTime: 2 * 60 * 1000,
    });
}