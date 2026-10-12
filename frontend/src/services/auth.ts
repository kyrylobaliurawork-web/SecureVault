import { apiRequest } from "./api";

export interface RegisterPayload {
  login: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface User {
  id: number;
  login: string;
  email: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export async function registerUser(
  payload: RegisterPayload,
): Promise<User> {
  return apiRequest<User>("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function loginUser(
  payload: LoginPayload,
): Promise<AuthToken> {
  return apiRequest<AuthToken>("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function getCurrentUser(
  token: string,
): Promise<User> {
  return apiRequest<User>("/auth/me", { token });
}