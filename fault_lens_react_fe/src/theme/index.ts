import { createTheme } from "@mui/material/styles";

import { palette } from "./palette";
import { typography } from "./typography";
import { shape } from "./shape";
import { components } from "./components";

const theme = createTheme({
  palette,
  typography,
  shape,
  components,
});

export default theme;