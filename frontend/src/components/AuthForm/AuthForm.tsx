import "./AuthForm.css";

interface AuthFormProps {
  isLogin: boolean;
  onSwitch: () => void;
}

function AuthForm({ isLogin, onSwitch }: AuthFormProps) {
  return (
    <div className="auth-card">
      <div className="auth-header">
        <div className="auth-logo">🔐</div>

        <h1>{isLogin ? "Welcome back" : "Create account"}</h1>

        <p>
          {isLogin
            ? "Sign in to access your files"
            : "Create your SecureVault account"}
        </p>
      </div>

      <form className="auth-form">
        {!isLogin && (
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              placeholder="Your name"
            />
          </div>
        )}

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="••••••••"
          />
        </div>

        {!isLogin && (
          <div className="form-group">
            <label htmlFor="confirmPassword">
              Confirm password
            </label>

            <input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
            />
          </div>
        )}

        <button className="auth-submit" type="submit">
          {isLogin ? "Login" : "Register"}
        </button>
      </form>

      <div className="auth-switch">
        <span>
          {isLogin
            ? "Don't have an account?"
            : "Already have an account?"}
        </span>

        <button type="button" onClick={onSwitch}>
          {isLogin ? "Register" : "Login"}
        </button>
      </div>
    </div>
  );
}

export default AuthForm;