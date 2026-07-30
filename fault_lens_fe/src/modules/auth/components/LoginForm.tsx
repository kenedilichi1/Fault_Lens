"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import {
  Alert,
  Box,
  Button,
  Divider,
  Paper,
  Stack,
  TextField,
  Typography,
  Link,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import NextLink from "next/link";
import axios from "axios";

import { useLogin } from "../hooks/useLogin";
import { loginSchema, type LoginFormData } from "../schemas/auth.schema";
import { OAuthProviders } from "./OAuthProviders";

export function LoginForm() {
  const loginMutation = useLogin();
  const router = useRouter();

  const errorMessage = (() => {
    if (!axios.isAxiosError(loginMutation.error)) {
      return "Something went wrong";
    }

    const detail = loginMutation.error.response?.data?.detail;

    return typeof detail === "string" ? detail : "Something went wrong";
  })();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (values: LoginFormData) => {
    loginMutation.mutate(values, {
      onSuccess: () => {
        router.replace("/dashboard");
      },
    });
  };

  return (
    <Paper
      elevation={3}
      sx={{
        width: "100%",
        p: 4,
        borderRadius: 3,
      }}
    >
      <Stack spacing={3}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Welcome back
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Sign in to FaultLens
          </Typography>
        </Box>

        {loginMutation.isError && (
          <Alert severity="error">{errorMessage}</Alert>
        )}

        <OAuthProviders idPrefix="login" />

        <Divider>
          <Typography variant="caption" color="text.secondary">
            or sign in with email
          </Typography>
        </Divider>

        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={2}>
            <TextField
              id="login-email"
              label="Email"
              fullWidth
              {...register("email")}
              error={!!errors.email}
              helperText={errors.email?.message}
            />

            <TextField
              id="login-password"
              label="Password"
              type="password"
              fullWidth
              {...register("password")}
              error={!!errors.password}
              helperText={errors.password?.message}
            />

            <Button
              id="login-submit"
              type="submit"
              variant="contained"
              loading={loginMutation.isPending}
              fullWidth
            >
              Login
            </Button>
          </Stack>
        </form>

        <Typography align="center" variant="body2">
          Don&apos;t have an account?{" "}
          <Link component={NextLink} href="/register" underline="hover">
            Create one
          </Link>
        </Typography>
      </Stack>
    </Paper>
  );
}
