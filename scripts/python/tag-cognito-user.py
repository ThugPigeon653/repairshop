import os
import boto3
import json
import uuid

ssm = boto3.client('ssm')
cognito_client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    try:
        unique_tag = str(uuid.uuid4())  # Generate a UUID as the unique tag
        for user in event['request']['userAttributes']:
            if user == 'email':  # Use any user attribute that's available
                email = event['request']['userAttributes'][user]
                update_user_attributes(event['userName'], email, unique_tag)
    except Exception as e:
        print(f"Error: {e}")

    response = {
        'response': event['response']
    }

    return response

def update_user_attributes(username, email, unique_tag):
    try:
        pool = get_parameter_value(os.environ['POOL'])

        response = cognito_client.admin_update_user_attributes(
            UserPoolId=pool,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'custom:tenant_tag',
                    'Value': unique_tag
                }
            ]
        )

        ddl_event = {
            'tenant': unique_tag  # Pass the relevant tenant ID or value
        }

        # Invoke the DDL Lambda function
        response = boto3.client('lambda').invoke(
            FunctionName=os.environ['DEFINETABLES'],
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps(ddl_event)
        )

        print(f"User attributes updated for {username}")
    except Exception as e:
        print(f"Error updating user attributes: {e}")

def get_parameter_value(parameter_name):
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving parameter value: {e}")
        return None