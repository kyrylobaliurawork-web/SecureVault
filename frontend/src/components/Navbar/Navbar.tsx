import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/useAuth";
import "./Navbar.css";

function Navbar() {
  const { user, loading, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <span>SecureVault</span>
        </Link>
      </div>

      <div className="navbar-actions">
        {!loading && (
          user ? (
            <>
              <Link
                to="/profile"
                className="navbar-button navbar-button-login"
              >
                Profile
              </Link>

              <button
                type="button"
                className="navbar-button navbar-button-register"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="navbar-button navbar-button-login"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="navbar-button navbar-button-register"
              >
                Register
              </Link>
            </>
          )
        )}
      </div>
    </nav>
  );
}

export default Navbar;