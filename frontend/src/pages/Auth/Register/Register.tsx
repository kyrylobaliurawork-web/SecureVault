import { useNavigate } from "react-router-dom";
import AuthForm from "../../../components/AuthForm/AuthForm";
import { registerUser } from "../../../services/auth";

function Register() {
  const navigate = useNavigate();

  const handleRegister = async (data: {
    login?: string;
    email: string;
    password: string;
  }) => {
    if (!data.login) {
      throw new Error("Login is required");
    }

    await registerUser({
      login: data.login,
      email: data.email,
      password: data.password,
    });

    navigate("/login");
  };

  return (
    <AuthForm
      mode="register"
      onSubmit={handleRegister}
      onSwitch={() => navigate("/login")}
    />
  );
}

export default Register;