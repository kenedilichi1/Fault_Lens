
export type OrganizationRole =
  | "OWNER"
  | "ADMIN"
  | "MEMBER"
  | "VIEWER";

export type OrganizationStatus =
  | "ACTIVE"
  | "INACTIVE";

export type OrganizationPlan =
  | "FREE"
  | "PRO"
  | "ENTERPRISE";

type Owner = {
  id: string;
  full_name: string;
  email: string;
  avatar: string;
}

type MemberSummary = {
  total_members: number;
  owners: number;
  admins: number;
  members: number;
  viewers: number
}

export type Organization = {
  id: string;
  name: string;
  slug: string;
  timezone: string;
  member_summary: MemberSummary;
  role: OrganizationRole;
  logo_url: string;
  plan: string;
  is_active: boolean;
  owner: Owner;
  created_at: Date;
  updated_at: Date
  status: OrganizationStatus
};

export type OrganizationList = {
  organization_id: string
  organization_name: string;
  slug: string;
  timezone: string;
  member_count: number;
  role: OrganizationRole;
}

export interface OrganizationMember {
  id: string;
  role: OrganizationRole;
  status: OrganizationStatus;
  organization_id: string;
  user: {
    id: string;
    full_name: string;
    email: string;
    avatar_url: string;
  }
  created_at: Date;
  updated_at: Date;
}

export type UpdateOrganizationPayload = {
  name: string;
  timezone: string;
  logo_url: string
}

export type CreateOrganizationPayload = {
  name: string
  timezone: string
  plan: string
}