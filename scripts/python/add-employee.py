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

def add_employee_to_database(first_name, last_name, email, store):
    # Add your connection setup here
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = '''
    INSERT INTO public.employees (first_name, last_name, email, store)
    VALUES (%s, %s, %s, %s)
    '''
    data = (first_name, last_name, email, store)

    try:
        cursor.execute(sql, data)
        employee_id = cursor.fetchone()[0]
        conn.commit()
        return employee_id
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding employee: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding employee: Integrity constraint violation"
        else:
            error_message = f"Error adding employee: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    first_name = event['first_name']
    last_name = event['last_name']
    email = event['email']
    store = event['store']

    try:
        employee_id = add_employee_to_database(first_name, last_name, email, store)
        return {
            'statusCode': 200,
            'body': f'Employee added with ID: {employee_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }