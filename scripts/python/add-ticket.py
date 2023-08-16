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

def add_ticket(customer_id, ticket_title, ticket_priority_level,
               ticket_description, creation_date, due_date,
               tech, net_price, gross_price):
    sql = '''
    INSERT INTO public.tickets (customer_id, ticket_title, ticket_priority_level,
                                ticket_description, creation_date, due_date,
                                tech, net_price, gross_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (customer_id, ticket_title, ticket_priority_level,
            ticket_description, creation_date, due_date,
            tech, net_price, gross_price)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")
        ticket_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding ticket: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding ticket: Integrity constraint violation"
        else:
            error_message = f"Error adding ticket: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

    return ticket_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    customer_id = body['customer_id']
    ticket_title = body['ticket_title']
    ticket_priority_level = body['ticket_priority_level']
    ticket_description = body['ticket_description']
    creation_date = body['creation_date']
    due_date = body['due_date']
    tech = body['tech']
    net_price = body['net_price']
    gross_price = body['gross_price']

    try:
        ticket_id = add_ticket(customer_id, ticket_title, ticket_priority_level,
                                ticket_description, creation_date, due_date,
                                tech, net_price, gross_price)
        return {
            'statusCode': 200,
            'body': f'Ticket added with ID: {ticket_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }