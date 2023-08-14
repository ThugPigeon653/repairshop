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

def add_item_to_database(item_display_name, item_make, item_model, item_description,
                         operating_system, website, custom_fields):
    # Add your connection setup here
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])
    
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    
    sql = '''
    INSERT INTO public.items (item_display_name, item_make, item_model, item_description,
                              operating_system, website, custom_fields)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    data = (item_display_name, item_make, item_model, item_description,
            operating_system, website, custom_fields)

    try:
        cursor.execute(sql, data)
        item_id = cursor.fetchone()[0]
        conn.commit()
        return item_id
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding item: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding item: Integrity constraint violation"
        else:
            error_message = f"Error adding item: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    body = json.loads(event['body'])
    item_display_name = body['item_display_name']
    item_make = body['item_make']
    item_model = body['item_model']
    item_description = body['item_description']
    operating_system = body['operating_system']
    website = body['website']
    custom_fields = body['custom_fields']
    
    try:
        item_id = add_item_to_database(item_display_name, item_make, item_model, item_description,
                                       operating_system, website, custom_fields)
        return {
            'statusCode': 200,
            'body': f'Item added with ID: {item_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }