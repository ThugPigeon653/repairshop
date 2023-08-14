import boto3
import uuid
import psycopg2
import os

def add_user_to_database(username, tenant_id):
    # Add your RDS connection setup here
    database = os.environ['DB']
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    host = os.environ['HOST']
    port = os.environ['PORT']

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = '''
    INSERT INTO public.users (username, tenant_id)
    VALUES (%s, %s)
    '''
    data = (username, tenant_id)

    try:
        cursor.execute(sql, data)
        conn.commit()
    except psycopg2.Error as e:
        # Handle exceptions
        raise Exception("Error adding user to the database")
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    user_attributes = event['request']['userAttributes']
    username = user_attributes['sub']  

    tenant_id = str(uuid.uuid4())

    cognito_client = boto3.client('cognito-idp')
    response = cognito_client.admin_tag_user(
        UserPoolId=event['userPoolId'],
        Username=username,
        UserAttributes=[
            {
                'Name': 'custom:tenant_id',
                'Value': tenant_id
            }
        ]
    )

    # Add user to RDS database
    try:
        add_user_to_database(username, tenant_id)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': 'Error adding user to database'
        }

    return event