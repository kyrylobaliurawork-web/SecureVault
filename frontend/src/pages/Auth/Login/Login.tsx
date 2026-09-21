import { useNavigate } from "react-router-dom";
import AuthForm from "../../../components/AuthForm/AuthForm";

function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Поки просто імітуємо успішний login
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