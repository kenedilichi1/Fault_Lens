export const organizationKeys = {
  all: ["organizations"] as const,

  detail: (organizationId: string) =>
    [...organizationKeys.all, organizationId] as const,

  members: (organizationId: string) =>
    [
      ...organizationKeys.detail(organizationId),
      "members",
    ] as const,
};