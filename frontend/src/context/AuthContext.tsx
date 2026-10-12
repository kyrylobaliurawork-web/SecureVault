import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { getCurrentUser, type User } from "../services/auth";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  refreshUser: () => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  async function refreshUser() {
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
  }

  useEffect(() => {
    void refreshUser().finally(() => setLoading(false));
  }, []);

  function logout() {
    sessionStorage.removeItem("access_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, refreshUser, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
}