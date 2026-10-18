import { useNavigate } from "react-router-dom";
import AuthForm from "../../../components/AuthForm/AuthForm";
import { loginUser } from "../../../services/auth";
import { useAuth } from "../../../context/useAuth";

function Login() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();

  const handleLogin = async (data: {
    login?: string;
    email: string;
    password: string;
  }) => {
    const result = await loginUser({
      email: data.email,
      password: data.password,
    });

    sessionStorage.setItem("access_token", result.access_token);

    await refreshUser();
    navigate("/");
  };

  return (
    <AuthForm
      mode="login"
      onSubmit={handleLogin}
      onSwitch={() => navigate("/register")}
    />
  );
}

export default Login;