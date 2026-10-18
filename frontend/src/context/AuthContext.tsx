import {
  useCallback,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { getCurrentUser, type User } from "../services/auth";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    const token = sessionStorage.getItem("access_token");

    if (!token) {
      setUser(null);
      return;
    }

    try {
      const currentUser = await getCurrentUser(token);
      setUser(currentUser);
    } catch {
      sessionStorage.removeItem("access_token");
      setUser(null);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function initializeAuth() {
      try {
        await refreshUser();
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void initializeAuth();

    return () => {
      cancelled = true;
    };
  }, [refreshUser]);

  const logout = useCallback(() => {
    sessionStorage.removeItem("access_token");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, refreshUser, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}