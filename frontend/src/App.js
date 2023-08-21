import React, { useState, useEffect } from 'react';
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from './aws-exports';
import NavBar from './Navbar';
import SearchFields from './SearchFields';
import '@aws-amplify/ui-react/styles.css';
import './styles.css';
import { apiEndpoint } from './custom-exports';
import { withAuthenticator } from '@aws-amplify/ui-react';

Amplify.configure(awsconfig);

function App() {
  const [selectedAssetType, setSelectedAssetType] = useState(null);

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
  };

  const generateSearchFields = (assetType) => {
    setSelectedAssetType(assetType);
  };

  useEffect(() => {
    fetchUserPoolAndClientId();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <NavBar generateSearchFields={generateSearchFields} />
        <br/>
        <button onClick={() => Auth.signOut()}>Sign Out</button>
        {selectedAssetType && <SearchFields assetType={selectedAssetType} />}
      </header>
    </div>
  );
}

export default withAuthenticator(App);