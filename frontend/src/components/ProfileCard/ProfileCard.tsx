import "./ProfileCard.css";

function ProfileCard() {
  return (
    <section className="profile-card">
      <div className="profile-header">
        <div className="profile-avatar">
          K
        </div>

        <div>
          <h1>Kyrylo</h1>
          <p>kyrylo@example.com</p>
        </div>
      </div>

      <div className="profile-divider" />

      <div className="profile-section">
        <h2>Account information</h2>

        <div className="profile-info">
          <div className="info-item">
            <span className="info-label">Name</span>
            <span className="info-value">Kyrylo</span>
          </div>

          <div className="info-item">
            <span className="info-label">Email</span>
            <span className="info-value">
              kyrylo@example.com
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">Member since</span>
            <span className="info-value">
              September 2026
            </span>
          </div>
        </div>
      </div>

      <div className="profile-divider" />

      <div className="profile-section">
        <h2>Security</h2>

        <button className="password-button">
          Change password
        </button>
      </div>
    </section>
  );
}

export default ProfileCard;