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

def create_customer(first_name, last_name, business, email, phone, address_line_1,
                    address_line_2, city, state_territory, zip_code, country,
                    referred_by, tax_rate, is_sms, is_billing_emails, is_marketing_emails,
                    is_report_emails, is_portal_user, additional_notification_email,
                    invoice_cc_email):
    # Add your connection setup here
    database = get_parameter_value(os.environ['DB'])
    user = get_parameter_value(os.environ['USER'])
    password = get_parameter_value(os.environ['PASSWORD'])
    host = get_parameter_value(os.environ['HOST'])
    port = get_parameter_value(os.environ['PORT'])

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

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

    try:
        cursor.execute(sql, data)
        customer_id = cursor.fetchone()[0]
        conn.commit()
        return customer_id
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
    finally:
        cursor.close()
        conn.close()

def lambda_handler(event, context):
    first_name = event['first_name']
    last_name = event['last_name']
    business = event['business']
    email = event['email']
    phone = event['phone']
    address_line_1 = event['address_line_1']
    address_line_2 = event['address_line_2']
    city = event['city']
    state_territory = event['state_territory']
    zip_code = event['zip_code']
    country = event['country']
    referred_by = event['referred_by']
    tax_rate = event['tax_rate']
    is_sms = event['is_sms']
    is_billing_emails = event['is_billing_emails']
    is_marketing_emails = event['is_marketing_emails']
    is_report_emails = event['is_report_emails']
    is_portal_user = event['is_portal_user']
    additional_notification_email = event['additional_notification_email']
    invoice_cc_email = event['invoice_cc_email']

    try:
        customer_id = create_customer(first_name, last_name, business, email, phone, address_line_1,
                                      address_line_2, city, state_territory, zip_code, country,
                                      referred_by, tax_rate, is_sms, is_billing_emails,
                                      is_marketing_emails, is_report_emails, is_portal_user,
                                      additional_notification_email, invoice_cc_email)
        return {
            'statusCode': 200,
            'body': f'Customer created with ID: {customer_id}'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }