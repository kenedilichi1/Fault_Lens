import { Components, Theme } from "@mui/material/styles";

export const components: Components<Theme> = {
  MuiCssBaseline: {
    styleOverrides: {
      html: {
        backgroundColor: "#14121A",
      },

      body: {
        backgroundColor: "#14121A",
        color: "#F1EDF7",
      },

      "*": {
        scrollbarWidth: "thin",
        scrollbarColor: "#34303D transparent",
      },

      "*::-webkit-scrollbar": {
        width: 8,
        height: 8,
      },

      "*::-webkit-scrollbar-track": {
        background: "transparent",
      },

      "*::-webkit-scrollbar-thumb": {
        backgroundColor: "#34303D",
        borderRadius: 8,
      },

      "::selection": {
        backgroundColor: "rgba(124, 58, 237, 0.35)",
        color: "#FFFFFF",
      },
    },
  },

  MuiPaper: {
    styleOverrides: {
      root: {
        backgroundImage: "none",
        backgroundColor: "#211E27",
        border: "1px solid #34303D",
        boxShadow: "none",
      },
    },
  },

  MuiCard: {
    styleOverrides: {
      root: {
        backgroundImage: "none",
        backgroundColor: "#211E27",
        border: "1px solid #34303D",
        borderRadius: 12,
        boxShadow: "none",

        transition:
          "border-color 150ms ease, background-color 150ms ease",

        "&:hover": {
          borderColor: "#4B4358",
        },
      },
    },
  },

  MuiButton: {
    defaultProps: {
      disableElevation: true,
    },

    styleOverrides: {
      root: {
        borderRadius: 8,
        minHeight: 40,
        padding: "8px 16px",
        fontWeight: 600,
      },

      contained: {
        "&.MuiButton-containedPrimary": {
          backgroundColor: "#7C3AED",

          "&:hover": {
            backgroundColor: "#6D28D9",
          },

          "&:active": {
            backgroundColor: "#5B21B6",
          },
        },
      },

      outlined: {
        borderColor: "#4A4453",
        color: "#D8D2E0",

        "&:hover": {
          borderColor: "#7C3AED",
          backgroundColor: "rgba(124, 58, 237, 0.08)",
        },
      },

      text: {
        "&:hover": {
          backgroundColor: "rgba(124, 58, 237, 0.08)",
        },
      },
    },
  },

  MuiIconButton: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        color: "#A8A2B1",

        "&:hover": {
          color: "#F1EDF7",
          backgroundColor: "rgba(124, 58, 237, 0.10)",
        },
      },
    },
  },

  MuiTextField: {
    defaultProps: {
      size: "small",
    },
  },

  MuiOutlinedInput: {
    styleOverrides: {
      root: {
        backgroundColor: "#1A1820",
        borderRadius: 8,

        "& .MuiOutlinedInput-notchedOutline": {
          borderColor: "#403B49",
        },

        "&:hover .MuiOutlinedInput-notchedOutline": {
          borderColor: "#625A6D",
        },

        "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
          borderColor: "#7C3AED",
          borderWidth: 1,
        },
      },

      input: {
        color: "#F1EDF7",

        "&::placeholder": {
          color: "#6F6978",
          opacity: 1,
        },
      },
    },
  },

  MuiInputLabel: {
    styleOverrides: {
      root: {
        color: "#A8A2B1",

        "&.Mui-focused": {
          color: "#A78BFA",
        },
      },
    },
  },

  MuiSelect: {
    styleOverrides: {
      select: {
        backgroundColor: "#1A1820",
      },

      icon: {
        color: "#8B96A8",
      },
    },
  },

  MuiMenu: {
    styleOverrides: {
      paper: {
        backgroundColor: "#211E27",
        border: "1px solid #34303D",
        boxShadow: "0 12px 40px rgba(0, 0, 0, 0.4)",
      },
    },
  },

  MuiMenuItem: {
    styleOverrides: {
      root: {
        borderRadius: 6,
        margin: "2px 4px",

        "&:hover": {
          backgroundColor: "rgba(124, 58, 237, 0.10)",
        },

        "&.Mui-selected": {
          backgroundColor: "rgba(124, 58, 237, 0.18)",
        },

        "&.Mui-selected:hover": {
          backgroundColor: "rgba(124, 58, 237, 0.24)",
        },
      },
    },
  },

  MuiChip: {
    styleOverrides: {
      root: {
        borderRadius: 6,
        fontWeight: 600,
      },
    },
  },

  MuiDialog: {
    styleOverrides: {
      paper: {
        backgroundColor: "#211E27",
        backgroundImage: "none",
        border: "1px solid #34303D",
        borderRadius: 14,
        boxShadow: "0 24px 80px rgba(0, 0, 0, 0.55)",
      },
    },
  },

  MuiDrawer: {
    styleOverrides: {
      paper: {
        backgroundColor: "#14121A",
        backgroundImage: "none",
        borderColor: "#34303D",
      },
    },
  },

  MuiTooltip: {
    styleOverrides: {
      tooltip: {
        backgroundColor: "#2A2632",
        border: "1px solid #403B49",
        color: "#F1EDF7",
        fontSize: "0.75rem",
      },

      arrow: {
        color: "#2A2632",
      },
    },
  },

  MuiDivider: {
    styleOverrides: {
      root: {
        borderColor: "#34303D",
      },
    },
  },

  MuiTableCell: {
    styleOverrides: {
      root: {
        borderColor: "#34303D",
      },

      head: {
        color: "#8B96A8",
        fontFamily: '"JetBrains Mono", monospace',
        fontSize: "0.72rem",
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: "0.06em",
      },

      body: {
        color: "#D8D2E0",
      },
    },
  },

  MuiTabs: {
    styleOverrides: {
      indicator: {
        height: 2,
        borderRadius: 2,
        backgroundColor: "#7C3AED",
      },
    },
  },

  MuiTab: {
    styleOverrides: {
      root: {
        minHeight: 44,
        textTransform: "none",
        fontWeight: 600,
        color: "#8B96A8",

        "&.Mui-selected": {
          color: "#C4B5FD",
        },
      },
    },
  },

  MuiLinearProgress: {
    styleOverrides: {
      root: {
        height: 6,
        borderRadius: 6,
        backgroundColor: "#2A2632",
      },

      bar: {
        borderRadius: 6,
      },
    },
  },

  MuiBadge: {
    styleOverrides: {
      badge: {
        fontFamily: '"JetBrains Mono", monospace',
        fontSize: "0.65rem",
      },
    },
  },
};