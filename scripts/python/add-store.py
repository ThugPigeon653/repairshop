import psycopg2
import boto3
import os
import json

## DB & VPC Connection
ssm = boto3.client('ssm')

def get_parameter_value(parameter_name):
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving parameter value: {e}")
        return None

# Add your connection setup here
database = get_parameter_value(os.environ['DB'])
user = get_parameter_value(os.environ['USER'])
password = get_parameter_value(os.environ['PASSWORD'])
host = get_parameter_value(os.environ['HOST'])
port = get_parameter_value(os.environ['PORT'])

# Create a global connection and cursor
conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

def create_store(address_line_1, city, zip_code, phone, tenant_tag):
    sql = '''
    INSERT INTO public.stores_TENANT (address_line_1, city, zip_code, phone)
    VALUES (%s, %s, %s, %s)
    '''.replace("TENANT", tenant_tag)
    data = (address_line_1, city, zip_code, phone)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")
        store_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error creating store: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error creating store: Integrity constraint violation"
        else:
            error_message = f"Error creating store: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

    return store_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    address_line_1 = body['address_line_1']
    city = body['city']
    zip_code = body['zip_code']
    phone = body['phone']

    tenant_tag = event['request']['userAttributes']['custom:tenant_tag']

    try:
        store_id = create_store(address_line_1, city, zip_code, phone, tenant_tag)
        return {
            'statusCode': 200,
            'body': f'Store created with ID: {store_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }