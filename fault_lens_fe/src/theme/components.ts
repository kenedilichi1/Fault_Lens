import { Components } from "@mui/material/styles";

export const components: Components = {
  MuiButton: {
    defaultProps: {
      variant: "contained",
      disableElevation: true,
    },

    styleOverrides: {
      root: {
        borderRadius: 8,
        textTransform: "none",
        fontWeight: 600,
        minHeight: 44,
      },
    },
  },

  MuiPaper: {
    defaultProps: {
      elevation: 0,
    },

    styleOverrides: {
      root: {
        border: "1px solid #E2E8F0",
      },
    },
  },

  MuiTextField: {
    defaultProps: {
      fullWidth: true,
      size: "medium",
    },
  },

  MuiOutlinedInput: {
    styleOverrides: {
      root: {
        borderRadius: 8,
      },
    },
  },

  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 8,
      },
    },
  },
};