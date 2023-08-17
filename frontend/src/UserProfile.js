import React from 'react';

function UserProfile({ user, onLogout }) {
  return (
    <div className="user-profile">
      <p>Welcome, {user.username}!</p>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default UserProfile;