import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <span>SecureVault</span>
      </div>

      <div className="navbar-actions">
        <button className="navbar-button navbar-button-login">
          Login
        </button>

        <button className="navbar-button navbar-button-register">
          Register
        </button>
      </div>
    </nav>
  );
}

export default Navbar;