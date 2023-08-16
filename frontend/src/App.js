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

console.log("getting pool...")

const frontendOrigin = window.location.origin;
const frontendProtocol = window.location.protocol;

console.log(frontendProtocol)

const poolIdResponse = await fetch(api, {
  method: 'POST',
  body: JSON.stringify({
    parameterName: '/repair/UserPoolIdParameter'
  })
});
const poolIdData = await poolIdResponse.json();
console.log("getting client...")

const clientIdResponse = await fetch(api, {
  method: 'POST',
  body: JSON.stringify({
    parameterName: '/repair/AppClientIdParameter'
  })
});
const clientIdData = await clientIdResponse.json();

console.log(clientIdData.value)

const dynamicConfig = {
  ...awsconfig,
  Auth: {
    ...awsconfig.Auth,
    userPoolId: poolIdData.value,  
    userPoolWebClientId: clientIdData.value
  }
};
console.log(dynamicConfig)

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