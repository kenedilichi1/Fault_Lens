import { organizationApi } from "../api/organization.api";
import { CreateOrganizationPayload, UpdateOrganizationPayload } from "../types/organization.types";

export const organizationService = {
  createOrganization: async (payload: CreateOrganizationPayload) => {
    return organizationApi.createOrganization(payload);
  },

  fetchOrganization: async (organizationId: string) => {
    const organization = await organizationApi.getOrganization(organizationId);

    return organization;
  },

  fetchOrganizations: async () => {
    const organizations = await organizationApi.getOrganizations();

    return organizations;
  },


  getMembers(organizationId: string) {
    return organizationApi.getOrganizationMembers(organizationId);
  },

  update(
    organizationId: string,
    payload: Partial<UpdateOrganizationPayload>
  ) {
    return organizationApi.updateOrganization(
      organizationId,
      payload
    );
  },
};
