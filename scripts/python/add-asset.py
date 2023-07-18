import psycopg2
import boto3
import os

## DB & VPC Connection
ssm = boto3.client('ssm')

def get_parameter_value(parameter_name):
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving parameter value: {e}")
        return None

def create_asset(asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes):
    # Add your connection setup here
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = '''
    INSERT INTO public.assets (asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    data = (asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes)

    try:
        cursor.execute(sql, data)
        asset_id = cursor.fetchone()[0]
        conn.commit()
        return asset_id
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error creating asset: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error creating asset: Integrity constraint violation"
        else:
            error_message = f"Error creating asset: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    asset_name = event['asset_name']
    asset_serial = event['asset_serial']
    asset_password = event['asset_password']
    warranty_expiration = event['warranty_expiration']
    date_of_manufacture = event['date_of_manufacture']
    notes = event['notes']

    try:
        asset_id = create_asset(asset_name, asset_serial, asset_password, warranty_expiration, date_of_manufacture, notes)
        return {
            'statusCode': 200,
            'body': f'Asset created with ID: {asset_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }