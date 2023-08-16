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

def add_invoice_to_database(invoice_status, date_created, is_taxable, date_paid,
                            tech_notes, ticket, payment_method, purchase_order_number):
    sql = '''
    INSERT INTO public.invoices (invoice_status, date_created, is_taxable, date_paid,
                                tech_notes, ticket, payment_method, purchase_order_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (invoice_status, date_created, is_taxable, date_paid,
            tech_notes, ticket, payment_method, purchase_order_number)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")  # Retrieve the last auto-generated ID
        invoice_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding invoice: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding invoice: Integrity constraint violation"
        else:
            error_message = f"Error adding invoice: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

    return invoice_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    invoice_status = body['invoice_status']
    date_created = body['date_created']
    is_taxable = body['is_taxable']
    date_paid = body['date_paid']
    tech_notes = body['tech_notes']
    ticket = body['ticket']
    payment_method = body['payment_method']
    purchase_order_number = body['purchase_order_number']

    try:
        invoice_id = add_invoice_to_database(invoice_status, date_created, is_taxable, date_paid,
                                             tech_notes, ticket, payment_method, purchase_order_number)
        return {
            'statusCode': 200,
            'body': f'Invoice added with ID: {invoice_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }