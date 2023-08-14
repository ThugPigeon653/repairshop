import json
import boto3

barred_values=["/repair/DBParameter", "/repair/UserParameter", "/repair/PasswordParameter", "/repair/HostParameter", "/repair/PortParameter"]

def lambda_handler(event, context):
        try:
                print(event)
                request_body = json.loads(event['body'])
                parameter_name = request_body.get('parameterName')
                is_allow=True
                for param in barred_values:
                        if param==parameter_name:
                                is_allow=False
                if is_allow:
                        ssm_client = boto3.client('ssm')
                        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
                        parameter_value = response['Parameter']['Value']
                                
                        response = {
                                "statusCode": 200,
                                "headers": {
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*"
                                },
                                "body": json.dumps({"value": parameter_value})
                        }
                        return response
                else:
                        # This error response is not distinct from an actual error. This prevents the api acknowledging to an attacker that they 
                        # correctly guessed a parameter name.
                        error_response = {
                        "statusCode": 500,
                        "headers": {
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*"
                                },
                        "body": "error"
                        }
                        return error_response
        except Exception as e:
                error_response = {
                        "statusCode": 500,
                        "headers": {
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*"
                                },
                        "body": json.dumps({"error": str(e)})
                }
                return error_response
                                                            
