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

def create_customer(first_name, last_name, business, email, phone, address_line_1,
                    address_line_2, city, state_territory, zip_code, country,
                    referred_by, tax_rate, is_sms, is_billing_emails, is_marketing_emails,
                    is_report_emails, is_portal_user, additional_notification_email,
                    invoice_cc_email, tenant_tag):
    sql = '''
    INSERT INTO public.customers_TENANT (first_name, last_name, business, email, phone, address_line_1,
                                  address_line_2, city, state_territory, zip_code, country, referred_by,
                                  tax_rate, is_sms, is_billing_emails, is_marketing_emails,
                                  is_report_emails, is_portal_user, additional_notification_email,
                                  invoice_cc_email)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''.replace("TENANT", tenant_tag)
    data = (first_name, last_name, business, email, phone, address_line_1, address_line_2, city,
            state_territory, zip_code, country, referred_by, tax_rate, is_sms, is_billing_emails,
            is_marketing_emails, is_report_emails, is_portal_user, additional_notification_email,
            invoice_cc_email)

    try:
        cursor.execute(sql, data)
        conn.commit()
        cursor.execute("SELECT lastval()")
        customer_id = cursor.fetchone()[0]
    except psycopg2.Error as e:
        # Check the specific exception raised by psycopg2
        if isinstance(e, psycopg2.DataError):
            error_message = f"Error creating customer: Invalid value for one or more parameters"
        elif isinstance(e, psycopg2.IntegrityError):
            error_message = f"Error creating customer: Integrity constraint violation"
        else:
            error_message = f"Error creating customer: Unknown error occurred"
        print(error_message)
        raise Exception(error_message)

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

    tenant_tag = event['request']['userAttributes']['custom:tenant_tag']

    try:
        customer_id = create_customer(first_name, last_name, business, email, phone, address_line_1,
                                      address_line_2, city, state_territory, zip_code, country,
                                      referred_by, tax_rate, is_sms, is_billing_emails,
                                      is_marketing_emails, is_report_emails, is_portal_user,
                                      additional_notification_email, invoice_cc_email, tenant_tag)
        return {
            'statusCode': 200,
            'body': f'Customer created with ID: {customer_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }