import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <span>SecureVault</span>
        </Link>
      </div>

      <div className="navbar-actions">
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
      </div>
    </nav>
  );
}

export default Navbar;