"use client";

import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Button,
  Card,
  Divider,
  Stack,
  TextField,
  Typography,
  CardContent,
  Link,
  Paper,
  Alert,
} from "@mui/material";
import { toast } from "sonner";
import axios from "axios";

import { useRegister } from "../hooks/useRegister";
import { type RegisterRequest } from "../types/auth.types";
import { registerSchema } from "../schemas/auth.schema";
import { OAuthProviders } from "./OAuthProviders";

export function RegisterForm() {
  const router = useRouter();

  const registerMutation = useRegister();

  const errorMessage = (() => {
    if (!axios.isAxiosError(registerMutation.error)) {
      return "Something went wrong";
    }

    const detail = registerMutation.error.response?.data?.detail;

    return typeof detail === "string" ? detail : "Something went wrong";
  })();

  type RegisterFormValues = RegisterRequest & {
    confirm_password: string;
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = (values: RegisterFormValues) => {
    const { confirm_password, ...requestPayload } = values;

    registerMutation.mutate(requestPayload, {
      onSuccess: () => {
        toast.success("Account created successfully.");

        router.push("/login");
      },

      onError: () => {
        toast.error(errorMessage);
      },
    });
  };

  return (
    <Paper elevation={3} sx={{ width: "100%", p: 4, borderRadius: 3 }}>
      <Stack spacing={3}>
        <Typography variant="h4">Create Account</Typography>

        <OAuthProviders idPrefix="register" />

        <Divider>
          <Typography variant="caption" color="text.secondary">
            or sign up with email
          </Typography>
        </Divider>

        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={2}>
            <TextField
              label="Full Name"
              {...register("full_name")}
              error={!!errors.full_name}
              helperText={errors.full_name?.message}
            />

            <TextField
              label="Email"
              {...register("email")}
              error={!!errors.email}
              helperText={errors.email?.message}
            />

            <TextField
              label="Password"
              type="password"
              {...register("password")}
              error={!!errors.password}
              helperText={errors.password?.message}
            />

            <TextField
              label="Confirm Password"
              type="password"
              {...register("confirm_password")}
              error={!!errors.confirm_password}
              helperText={errors.confirm_password?.message}
            />

            
            <Button
              type="submit"
              variant="contained"
              disabled={registerMutation.isPending}
              fullWidth
            >
              Create Account
            </Button>
          </Stack>
        </form>

        <Typography align="center">
          Already have an account? <Link href="/login">Sign In</Link>
        </Typography>
      </Stack>
    </Paper>
  );
}
