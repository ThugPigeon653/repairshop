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

database = get_parameter_value(os.environ['DB'])
user = get_parameter_value(os.environ['USER'])
password = get_parameter_value(os.environ['PASSWORD'])
host = get_parameter_value(os.environ['HOST'])
port = get_parameter_value(os.environ['PORT'])

# Fist level functions
def create_customer(first_name, last_name, business, email, phone, address_line_1,
                    address_line_2, city, state_territory, zip_code, country,
                    referred_by, tax_rate, is_sms, is_billing_emails, is_marketing_emails,
                    is_report_emails, is_portal_user, additional_notification_email,
                    invoice_cc_email):
    # Add your connection setup here
    
    sql = '''
    INSERT INTO public.customers (first_name, last_name, business, email, phone, address_line_1,
                                  address_line_2, city, state_territory, zip_code, country, referred_by,
                                  tax_rate, is_sms, is_billing_emails, is_marketing_emails,
                                  is_report_emails, is_portal_user, additional_notification_email,
                                  invoice_cc_email)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (first_name, last_name, business, email, phone, address_line_1, address_line_2, city,
            state_territory, zip_code, country, referred_by, tax_rate, is_sms, is_billing_emails,
            is_marketing_emails, is_report_emails, is_portal_user, additional_notification_email,
            invoice_cc_email)
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()  
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor() 
    cursor.execute(sql, data)
    customer_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    cursor.close()
    
    return customer_id

def lambda_handler(event, context):
    body = json.loads(event['body'])
    first_name = body['first_name']
    last_name = body['last_name']
    business = body['business']
    email = body['email']
    phone = body['phone']
    address_line_1 = body['address_line_1']
    address_line_2 = body['address_line_2']
    city = body['city']
    state_territory = body['state_territory']
    zip_code = body['zip_code']
    country = body['country']
    referred_by = body['referred_by']
    tax_rate = body['tax_rate']
    is_sms = body['is_sms']
    is_billing_emails = body['is_billing_emails']
    is_marketing_emails = body['is_marketing_emails']
    is_report_emails = body['is_report_emails']
    is_portal_user = body['is_portal_user']
    additional_notification_email = body['additional_notification_email']
    invoice_cc_email = body['invoice_cc_email']
    
    customer_id = create_customer(first_name, last_name, business, email, phone, address_line_1,
                                  address_line_2, city, state_territory, zip_code, country,
                                  referred_by, tax_rate, is_sms, is_billing_emails,
                                  is_marketing_emails, is_report_emails, is_portal_user,
                                  additional_notification_email, invoice_cc_email)
    
    return {
        'statusCode': 200,
        'body': f'Customer created with ID: {customer_id}'
    }
