
import { useAuth } from "../../context/AuthContext";
import "./ProfileCard.css";

function ProfileCard() {
  const { user, loading } = useAuth();

  if (loading) {
    return <section className="profile-card">Loading profile...</section>;
  }

  if (!user) {
    return <section className="profile-card">Please log in to view your profile.</section>;
  }

  return (
    <section className="profile-card">
      <div className="profile-header">
        <div className="profile-avatar">
          {user.login.charAt(0).toUpperCase()}
        </div>

        <div>
          <h1>{user.login}</h1>
          <p>{user.email}</p>
        </div>
      </div>

      <div className="profile-divider" />

      <div className="profile-section">
        <h2>Account information</h2>

        <div className="profile-info">
          <div className="info-item">
            <span className="info-label">Name</span>
            <span className="info-value">{user.login}</span>
          </div>

          <div className="info-item">
            <span className="info-label">Email</span>
            <span className="info-value">{user.email}</span>
          </div>

          <div className="info-item">
            <span className="info-label">User ID</span>
            <span className="info-value">{user.id}</span>
          </div>
        </div>
      </div>

      <div className="profile-divider" />

      <div className="profile-section">
        <h2>Security</h2>
        <p>Password changes are not implemented yet.</p>
      </div>
    </section>
  );
}

export default ProfileCard;