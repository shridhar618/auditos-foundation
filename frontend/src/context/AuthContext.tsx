import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";

import { apiClient, tokenStorage } from "@/lib/api-client";
import type { AuthenticatedUser, LoginPayload, RegisterOrganizationPayload, TokenResponse } from "@/types/auth";

interface AuthContextValue {
  user: AuthenticatedUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  registerOrganization: (payload: RegisterOrganizationPayload) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (code: string) => boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCurrentUser = useCallback(async () => {
    try {
      const { data } = await apiClient.get<AuthenticatedUser>("/auth/me");
      setUser(data);
    } catch {
      setUser(null);
      tokenStorage.clear();
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (tokenStorage.getAccessToken()) {
      fetchCurrentUser();
    } else {
      setIsLoading(false);
    }
  }, [fetchCurrentUser]);

  const login = useCallback(async (payload: LoginPayload) => {
    const { data } = await apiClient.post<TokenResponse>("/auth/login", payload);
    tokenStorage.setTokens(data.access_token, data.refresh_token);
    await fetchCurrentUser();
  }, [fetchCurrentUser]);

  const registerOrganization = useCallback(async (payload: RegisterOrganizationPayload) => {
    const { data } = await apiClient.post<TokenResponse>("/auth/register", payload);
    tokenStorage.setTokens(data.access_token, data.refresh_token);
    await fetchCurrentUser();
  }, [fetchCurrentUser]);

  const logout = useCallback(async () => {
    const refreshToken = tokenStorage.getRefreshToken();
    tokenStorage.clear();
    setUser(null);
    if (refreshToken) {
      try {
        await apiClient.post("/auth/logout", { refresh_token: refreshToken });
      } catch {
        // best-effort - token is already cleared client-side regardless
      }
    }
  }, []);

  const hasPermission = useCallback(
    (code: string) => user?.permissions.includes(code) ?? false,
    [user]
  );

  return (
    <AuthContext.Provider
      value={{ user, isLoading, isAuthenticated: !!user, login, registerOrganization, logout, hasPermission }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
