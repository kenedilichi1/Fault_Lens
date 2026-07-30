import {
  Box,
  Container,
  Divider,
  Stack,
  Typography,
  Button,
  Card,
  Chip,
  Paper,
  TextField,
  CardContent
} from "@mui/material";

export default function UIPage() {
  return (
    <Container maxWidth="lg">
      <Stack spacing={6} sx={{ py: 6 }}>
        <Typography variant="h3">FaultLens Design System</Typography>

        <Divider />

        {/* Typography */}
        <Stack spacing={2}>
          <Typography variant="h4">Typography</Typography>

          <Typography variant="h1">Heading 1</Typography>

          <Typography variant="h2">Heading 2</Typography>

          <Typography variant="h3">Heading 3</Typography>

          <Typography variant="body1">Body 1</Typography>

          <Typography variant="body2">Body 2</Typography>
        </Stack>

        {/* Buttons */}
        <Stack direction="row" spacing={2} sx={{ flexWrap: "wrap" }}>
          <Button>Primary</Button>

          <Button color="secondary">AI</Button>

          <Button color="success">Success</Button>

          <Button color="warning">Warning</Button>

          <Button color="error">Error</Button>

          <Button loading>Loading</Button>

          <Button variant="outlined">Outlined</Button>

          <Button variant="text">Text</Button>
        </Stack>

        {/* Inputs */}
        <Stack spacing={2}>
          <TextField label="Email" />

          <TextField label="Password" type="password" />

          <TextField error helperText="Invalid password" />
        </Stack>

        {/* Alerts */}
        <Stack direction="row" spacing={2}>
          <Chip color="success" label="Healthy" />

          <Chip color="warning" label="Warning" />

          <Chip color="error" label="Critical" />

          <Chip color="info" label="Investigating" />
        </Stack>

        {/* Chips */}
        <Paper sx={{ p: 3 }}>This is a Paper component.</Paper>

        {/* Cards */}
        <Card>
          <CardContent>Card Content</CardContent>
        </Card>
      </Stack>
    </Container>
  );
}
