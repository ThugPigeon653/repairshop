import React, { useState, useEffect } from 'react';
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from './aws-exports';
import AuthenticatorContainer from './AuthenticatorContainer'; // Update the import path
import NavBar from './Navbar';
import SearchFields from './SearchFields';
import '@aws-amplify/ui-react/styles.css';
import './styles.css';
import { apiEndpoint } from './custom-exports';
import UserProfile from './UserProfile';

Amplify.configure(awsconfig);

function App() {
  const [user, setUser] = useState(null);
  const [showAuthForm, setShowAuthForm] = useState(false);
  const [selectedAssetType, setSelectedAssetType] = useState(null);

  useEffect(() => {
    const fetchUserPoolAndClientId = async () => {
      const api = apiEndpoint + "/getvalue";
      const poolIdResponse = await fetch(api, {
        method: 'POST',
        body: JSON.stringify({
          parameterName: '/repair/UserPoolIdParameter'
        })
      });
      const poolIdData = await poolIdResponse.json();

      const clientIdResponse = await fetch(api, {
        method: 'POST',
        body: JSON.stringify({
          parameterName: '/repair/AppClientIdParameter'
        })
      });
      const clientIdData = await clientIdResponse.json();

      const dynamicConfig = {
        ...awsconfig,
        Auth: {
          ...awsconfig.Auth,
          userPoolId: poolIdData.value,  
          userPoolWebClientId: clientIdData.value
        }
      };

      Amplify.configure(dynamicConfig);
      checkUserAuth();
    };

    fetchUserPoolAndClientId();
  }, []);

  const checkUserAuth = async () => {
    try {
      const userData = await Auth.currentAuthenticatedUser();
      setUser(userData);
    } catch (error) {
      setUser(null);
    }
  };

  const toggleAuthForm = () => {
    setShowAuthForm(!showAuthForm);
  };

  const closeAuthForm = () => {
    setShowAuthForm(false);
  };

  const generateSearchFields = (assetType) => {
    setSelectedAssetType(assetType);
  };

  return (
    <div className="App">
      <header className="App-header">
        <NavBar
          generateSearchFields={generateSearchFields}
          toggleAuthForm={toggleAuthForm}
        />
        <br />
        {user ? (
          <UserProfile user={user} />
        ) : (
          <AuthenticatorContainer authOpen={showAuthForm} onClose={closeAuthForm} />
        )}
        {selectedAssetType && <SearchFields assetType={selectedAssetType} />}
      </header>
    </div>
  );
}

export default App;