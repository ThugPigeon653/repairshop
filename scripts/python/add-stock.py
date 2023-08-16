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

def add_stock_item(barcode, net_paid, tax_paid, net_sale_price, tax_charged, item):
    sql = '''
    INSERT INTO public.stock (barcode, net_paid, tax_paid, net_sale_price, tax_charged, item)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    data = (barcode, net_paid, tax_paid, net_sale_price, tax_charged, item)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")  # Retrieve the last auto-generated ID
        stock_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error adding stock item: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error adding stock item: Integrity constraint violation"
        else:
            error_message = f"Error adding stock item: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

    return stock_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    barcode = body['barcode']
    net_paid = body['net_paid']
    tax_paid = body['tax_paid']
    net_sale_price = body['net_sale_price']
    tax_charged = body['tax_charged']
    item = body['item']

    try:
        stock_id = add_stock_item(barcode, net_paid, tax_paid, net_sale_price, tax_charged, item)
        return {
            'statusCode': 200,
            'body': f'Stock item added with ID: {stock_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }