import { useNavigate } from "react-router-dom";
import AuthForm from "../../../components/AuthForm/AuthForm";

function Register() {
  const navigate = useNavigate();

  const handleRegister = () => {
    // Поки просто імітуємо успішну реєстрацію
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