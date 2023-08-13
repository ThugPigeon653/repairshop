import React, { useState } from 'react';
import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports';
import AuthenticatorContainer from './AuthenticatorContainer'; // Update the import path
import NavBar from './Navbar';
import SearchFields from './SearchFields';
import '@aws-amplify/ui-react/styles.css';
import './styles.css';
import {apiEndpoint} from './custom-exports'


const api = apiEndpoint + "/getvalue";

const poolIdResponse = await fetch(api, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    parameterName: '/repair/userPoolIdParameter'
  })
});
const poolIdData = await poolIdResponse.json();

const clientIdResponse = await fetch(api, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    parameterName: 'repair/appClientIdParameter'
  })
});
const clientIdData = await clientIdResponse.json();

const dynamicConfig = {
  ...awsconfig,
  Auth: {
    ...awsconfig.Auth,
    userPoolId: poolIdData.parameterValue,  
    userPoolWebClientId: clientIdData.parameterValue
  }
};

Amplify.configure(dynamicConfig);
function App() {
  const [showAuthForm, setShowAuthForm] = useState(false);
  const [selectedAssetType, setSelectedAssetType] = useState(null);

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
        <AuthenticatorContainer authOpen={showAuthForm} onClose={closeAuthForm} />
        {selectedAssetType && <SearchFields assetType={selectedAssetType} />}
      </header>
    </div>
  );
}

export default App;