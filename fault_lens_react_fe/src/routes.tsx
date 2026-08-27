import { createBrowserRouter, Navigate } from "react-router-dom";

import { RootRedirect } from "@/modules/auth/guards/RootRedirect";

import AuthLayout from "@/components/layout/AuthLayout";
import ProtectedLayout from "@/components/layout/ProtectedLayout";
import { GlobalErrorBoundary } from "@/components/common/GlobalErrorBoundary";

import LoginPage from "@/modules/auth/pages/Login";
import RegisterPage from "@/modules/auth/pages/Register";
import OrganizationsPage from "./modules/organization/pages/OrganizationPage";
import OrganizationDetailsPage from "./modules/organization/pages/OrganizationDetailsPage";
import OrganizationOverviewPage from "./modules/organization/pages/OrganizationOverviewPage";
import CreateOrganizationPage from "./modules/organization/pages/CreateOrganizationPage";
import OrganizationList from "./modules/organization/components/OrganizationList";
import OrganizationMembersPage from "./modules/organization/pages/OrganizationMemberPage";
import OverviewPage from "@/modules/overview/pages/OverviewPage";

export const router = createBrowserRouter([
  {
    errorElement: <GlobalErrorBoundary />,
    children: [
      {
        path: "/",
        element: <RootRedirect />,
      },
      {
        element: <AuthLayout />,
        children: [
          {
            path: "login",
            element: <LoginPage />,
          },
          {
            path: "register",
            element: <RegisterPage />,
          },
        ],
      },
      {
        element: <ProtectedLayout />,
        children: [
          {
            path: "overview",
            element: <OverviewPage />,
          },
          {
            path: "organizations",
            element: <OrganizationsPage />,
            children: [
              {
                index: true,
                element: <OrganizationList />
              },
              {
                path: "new",
                element: <CreateOrganizationPage />,
              },
            ],
          },
          {
            path: "organizations/:organizationId",
            element: <OrganizationDetailsPage />,
            children: [
              {
                index: true,
                element: (
                  <Navigate
                    to="overview"
                    replace
                  />
                ),
              },

              {
                path: "overview",
                element: <OrganizationOverviewPage />,
              },

              {
                path: "members",
                element: <OrganizationMembersPage />,
              },
            ]
          }
        ],
      },
    ],
  },
]);
