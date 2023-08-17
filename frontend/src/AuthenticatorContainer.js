import { withAuthenticator } from '@aws-amplify/ui-react';
import { Auth } from 'aws-amplify'; // Import the Auth module

function AuthenticatorContainer({ authOpen, onClose, user, onLogout }) {
  const handleFormClick = (e) => {
    e.stopPropagation();
  };

  return authOpen ? (
    <div className="auth-form-container" onClick={onClose}>
      <div className="auth-form" onClick={handleFormClick}>
        ferofiheowrhfoiwehjrfioj
      </div>
      
      <button onClick={() => Auth.signOut()}>Logout</button>
    </div>
  ) : null;
}

export default withAuthenticator(AuthenticatorContainer);