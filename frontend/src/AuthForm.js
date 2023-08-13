import { useState } from 'react';
import { withAuthenticator, Authenticator } from '@aws-amplify/ui-react';
import { customConfig } from './custom-exports';
import '@aws-amplify/ui-react/styles.css';

function AuthForm() {
  const [authOpen, setAuthOpen] = useState(false);

  const openAuth = () => {
    setAuthOpen(true);
  };

  const closeAuth = () => {
    setAuthOpen(false);
  };

  const handleFormClick = () => {
    console.log('Form clicked');
    closeAuth();
  };

  return (
    <div className="auth-form-container" onClick={closeAuth}>
      <button onClick={openAuth}>Open Authenticator</button>
      {authOpen && (
        <div className="auth-form" onClick={handleFormClick}>
          <Authenticator />
        </div>
      )}
    </div>
  );
}

export default withAuthenticator(AuthForm, false, [], null, customConfig);