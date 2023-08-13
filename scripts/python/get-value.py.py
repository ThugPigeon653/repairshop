import json
import boto3

def lambda_handler(event, context):
        try:
                print(event)
                request_body = json.loads(event['body'])
                parameter_name = request_body.get('parameterName')
                
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
                                                            
