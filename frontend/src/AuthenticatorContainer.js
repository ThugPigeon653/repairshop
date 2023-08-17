import React from 'react';
import { Authenticator } from '@aws-amplify/ui-react';
import UserProfile from './UserProfile';

function AuthenticatorContainer({ authOpen, onClose }) {
  const handleFormClick = (e) => {
    e.stopPropagation(); // Prevent clicks inside the form from closing the window
    onClose(); // Close the overlay when clicking outside the form
  };

  return authOpen ? (
    <div className="auth-form-container" onClick={onClose}>
      <div className="auth-form" onClick={handleFormClick}>
        <Authenticator signUpAttributes={["email"]} />
      </div>
    </div>
  ) : null;
}

export default AuthenticatorContainer;