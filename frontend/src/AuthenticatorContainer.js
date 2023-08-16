import React from 'react';
import { Authenticator } from '@aws-amplify/ui-react';

function AuthenticatorContainer({ authOpen, onClose }) {
  const handleFormClick = (e) => {
    e.stopPropagation(); // Prevent clicks inside the form from closing the window
  };

  return authOpen ? (
    <div className="auth-form-container" onClick={onClose}>
      <div className="auth-form" onClick={handleFormClick}>
        <Authenticator signUpAttributes={["email"]}/>
      </div>
    </div>
  ) : null;
}

export default AuthenticatorContainer;