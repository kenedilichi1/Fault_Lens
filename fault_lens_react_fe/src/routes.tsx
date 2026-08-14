import { createBrowserRouter } from "react-router-dom";

import { RootRedirect } from "@/modules/auth/guards/RootRedirect";

import AuthLayout from "@/components/layout/AuthLayout";
import ProtectedLayout from "@/components/layout/ProtectedLayout";
import { GlobalErrorBoundary } from "@/components/common/GlobalErrorBoundary";

import LoginPage from "@/pages/login";
import RegisterPage from "@/pages/register";
import DashboardPage from "@/pages/dashboard";

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
            path: "dashboard",
            element: <DashboardPage />,
          },
        ],
      },
    ],
  },
]);
