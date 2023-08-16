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

def create_asset(asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, tenant_tag, notes):
    sql = '''
    INSERT INTO public.assets_TENANT (asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''.replace("TENANT", tenant_tag)
    data = (asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")
        asset_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error creating asset: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error creating asset: Integrity constraint violation"
        else:
            error_message = f"Error creating asset: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

    return asset_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    asset_name = body['asset_name']
    asset_serial = body['asset_serial']
    asset_password = body['asset_password']
    warranty_expiration = body['warranty_expiration']
    date_of_manufacture = body['date_of_manufacture']
    notes = body['notes']

    tenant_tag = event['request']['userAttributes']['custom:tenant_tag']

    try:
        asset_id = create_asset(asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, tenant_tag, notes)
        return {
            'statusCode': 200,
            'body': f'Asset created with ID: {asset_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }