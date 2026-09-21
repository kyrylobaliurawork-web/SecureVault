import { useState } from "react";
import AuthForm from "../../components/AuthForm/AuthForm";

function Auth() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <main className="auth-page">
      <AuthForm
        isLogin={isLogin}
        onSwitch={() => setIsLogin(!isLogin)}
      />
    </main>
  );
}

export default Auth;