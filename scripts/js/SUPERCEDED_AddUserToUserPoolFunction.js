const AWS = require('aws-sdk');
const ssm = new AWS.SSM();
const cognito = new AWS.CognitoIdentityServiceProvider();

exports.handler = async (event) => {
  const { tenant, username, email, password } = event;

  try {
    // Fetch the User Pool ID from SSM Parameter Store
    const ssmParamName = '/repair/UserPoolId';
    const ssmParams = {
      Name: ssmParamName,
      WithDecryption: false,
    };
    const ssmResponse = await ssm.getParameter(ssmParams).promise();
    const userPoolId = ssmResponse.Parameter.Value;

    const params = {
      UserPoolId: userPoolId,
      Username: username,
      UserAttributes: [
        { Name: 'email', Value: email },
        // Add other user attributes as needed
      ],
      TemporaryPassword: password,
    };

    // Add the user to the User Pool
    await cognito.adminCreateUser(params).promise();

    // Tag the user with the tenant identifier
    await cognito.tagResource({
      ResourceArn: `arn:aws:cognito-idp:${process.env.AWS_REGION}:${process.env.AWS_ACCOUNT_ID}:userpool/${userPoolId}`,
      Tags: [{ Key: 'Tenant', Value: tenant }],
    }).promise();

    return {
      statusCode: 200,
      body: JSON.stringify('User added successfully!'),
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify('An error occurred while adding the user.'),
    };
  }
};