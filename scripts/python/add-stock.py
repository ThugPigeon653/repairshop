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

def add_stock_item(barcode, net_paid, tax_paid, net_sale_price, tax_charged, item):
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql = '''
    INSERT INTO public.stock (barcode, net_paid, tax_paid, net_sale_price, tax_charged, item)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    data = (barcode, net_paid, tax_paid, net_sale_price, tax_charged, item)

    try:
        cursor.execute(sql, data)
        stock_id = cursor.fetchone()[0]
        conn.commit()
        return stock_id
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
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    barcode = event['barcode']
    net_paid = event['net_paid']
    tax_paid = event['tax_paid']
    net_sale_price = event['net_sale_price']
    tax_charged = event['tax_charged']
    item = event['item']

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