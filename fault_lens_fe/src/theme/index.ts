import { createTheme } from "@mui/material/styles";

import { components } from "./components";

export const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#2563EB",
      light: "#3B82F6",
      dark: "#1D4ED8",
      contrastText: "#FFFFFF",
    },

    secondary: {
      main: "#7C3AED",
    },

    success: {
      main: "#16A34A",
    },

    warning: {
      main: "#F59E0B",
    },

    error: {
      main: "#DC2626",
    },

    info: {
      main: "#0284C7",
    },

    background: {
      default: "#F8FAFC",
      paper: "#FFFFFF",
    },

    text: {
      primary: "#0F172A",
      secondary: "#475569",
    },

    divider: "#E2E8F0",
  },

  shape: {
    borderRadius: 8,
  },

  typography: {
    fontFamily: [
      "Inter",
      "system-ui",
      "sans-serif",
    ].join(","),
  },

  components,
});