import { authApi } from "@/modules/auth/api/auth.api";
import { useAuthStore } from "@/modules/auth/store/auth.store";
import axios, { AxiosError, AxiosRequestConfig } from "axios";

type RetryRequestConfig = AxiosRequestConfig & {
  _retry?: boolean;
};

let isRefreshing = false;

let failedQueue: {
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}[] = [];

function processQueue(error: unknown, token?: string) {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token!);
    }
  });

  failedQueue = [];
}

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  console.log("REQUEST:", config.url);
  console.log("TOKEN:", token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,

  async (error: AxiosError) => {
    const originalRequest = error.config as RetryRequestConfig;

    if (!originalRequest) {
      return Promise.reject(error);
    }

    if (
      error.response?.status !== 401 ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        failedQueue.push({
          resolve,
          reject,
        });
      })
        .then((token) => {
          originalRequest.headers = {
            ...originalRequest.headers,
            Authorization: `Bearer ${token}`,
          };

          return api(originalRequest);
        })
        .catch((err) => Promise.reject(err));
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const {
        refreshToken,
        setTokens,
        logout,
      } = useAuthStore.getState();

      if (!refreshToken) {
        logout();
        return Promise.reject(error);
      }

      const tokens = await authApi.refresh(refreshToken);

      setTokens(tokens);
      console.log("NEW TOKEN:", tokens.access_token);
      console.log(
        "STORE TOKEN:",
        useAuthStore.getState().accessToken
      );

      processQueue(null, tokens.access_token);

      originalRequest.headers = {
        ...originalRequest.headers,
        Authorization: `Bearer ${tokens.access_token}`,
      };

      return api(originalRequest);
    } catch (err) {
      processQueue(err);

      useAuthStore.getState().logout();

      return Promise.reject(err);
    } finally {
      isRefreshing = false;
    }
  }
);