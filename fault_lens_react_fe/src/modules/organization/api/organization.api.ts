import { api } from "@/lib/api";
import {
  CreateOrganizationPayload,
  Organization,
  OrganizationList,
  OrganizationMember,
  UpdateOrganizationPayload,
} from "../types/organization.types";
import { isAxiosError } from "axios";

const BASE_PATH = "/organizations";

export const organizationApi = {
  getOrganizations: async () => {
    const { data } = await api.get<OrganizationList[]>(BASE_PATH);
    return data;
  },

  getOrganization: async (
    organizationId: string,
  ): Promise<Organization | null> => {
    try {
      const { data } = await api.get<Organization>(
        `${BASE_PATH}/${organizationId}`,
      );
      return data;
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 404) return null;
      throw err;
    }
  },

  getOrganizationMembers: async (
    organization_id: string,
  ): Promise<OrganizationMember[]> => {
    const { data } = await api.get<OrganizationMember[]>(
      `${BASE_PATH}/${organization_id}/members`,
    );
    return data;
  },

  createOrganization: async (
    payload: CreateOrganizationPayload,
  ): Promise<Organization> => {
    const { data } = await api.post<Organization>(BASE_PATH, payload);
    return data;
  },

  updateOrganization: async (
    organizationId: string,
    payload: Partial<UpdateOrganizationPayload>,
  ): Promise<Organization> => {
    const { data } = await api.patch<Organization>(
      `${BASE_PATH}/${organizationId}`,
      payload,
    );
    return data;
  },

  deleteOrganization: async (organizationId: string): Promise<void> => {
    await api.delete(`${BASE_PATH}/${organizationId}`);
  },
};
