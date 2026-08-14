export type User = {
  id: string;
  email: string;
  full_name: string;
  avatar: string | null;
  is_active: boolean;
  email_verified: boolean;
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type RegisterRequest = {
  full_name: string;
  email: string;
  password: string;
};

export type AuthTokens = {
  access_token: string;
  refresh_token: string;
};

export type AuthResponse = {
  
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
};

export type RefreshResponse = {
  access_token: string;
};

export type ApiError = {
  detail: string;
};

