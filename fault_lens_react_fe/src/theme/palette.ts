import { PaletteOptions } from "@mui/material/styles";

export const palette: PaletteOptions = {
  mode: "dark",

  primary: {
    main: "#7C3AED",
    light: "#A78BFA",
    dark: "#6D28D9",
    contrastText: "#FFFFFF",
  },

  secondary: {
    main: "#8B96A8",
    light: "#B8C2D3",
    dark: "#647084",
    contrastText: "#0F1117",
  },

  error: {
    main: "#EF4444",
    light: "#F87171",
    dark: "#B91C1C",
  },

  warning: {
    main: "#A15100",
    light: "#D97706",
    dark: "#78350F",
    contrastText: "#FFFFFF",
  },

  success: {
    main: "#22C55E",
    light: "#4ADE80",
    dark: "#16A34A",
  },

  info: {
    main: "#3B82F6",
    light: "#60A5FA",
    dark: "#2563EB",
  },

  background: {
    default: "#14121A",
    paper: "#211E27",
  },

  text: {
    primary: "#F1EDF7",
    secondary: "#A8A2B1",
    disabled: "#625D6A",
  },

  divider: "#34303D",

  action: {
    active: "#C4B5FD",
    hover: "rgba(124, 58, 237, 0.10)",
    selected: "rgba(124, 58, 237, 0.18)",
    focus: "rgba(124, 58, 237, 0.22)",
    disabled: "rgba(255, 255, 255, 0.25)",
    disabledBackground: "rgba(255, 255, 255, 0.06)",
  },
};