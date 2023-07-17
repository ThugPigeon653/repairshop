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

def add_store_to_database(address_line_1, city, zip_code, phone):
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = '''
    INSERT INTO public.stores (address_line_1, city, zip_code, phone)
    VALUES (%s, %s, %s, %s)
    '''
    data = (address_line_1, city, zip_code, phone)

    try:
        cursor.execute(sql, data)
        store_id = cursor.fetchone()[0]
        conn.commit()
        return store_id
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding store: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding store: Integrity constraint violation"
        else:
            error_message = f"Error adding store: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    address_line_1 = event['address_line_1']
    city = event['city']
    zip_code = event['zip_code']
    phone = event['phone']

    try:
        store_id = add_store_to_database(address_line_1, city, zip_code, phone)
        return {
            'statusCode': 200,
            'body': f'Store added with ID: {store_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }