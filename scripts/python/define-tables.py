import psycopg2
import json
import boto3

# Initialize the database connection outside the lambda_handler function
ssm = boto3.client('ssm')
db_name = ssm.get_parameter(Name='/repair/DBParameter', WithDecryption=False)['Parameter']['Value']
db_user = ssm.get_parameter(Name='/repair/UserParameter', WithDecryption=False)['Parameter']['Value']
db_password = ssm.get_parameter(Name='/repair/PasswordParameter', WithDecryption=False)['Parameter']['Value']
db_host = ssm.get_parameter(Name='/repair/HostParameter', WithDecryption=False)['Parameter']['Value']
db_port = ssm.get_parameter(Name='/repair/PortParameter', WithDecryption=False)['Parameter']['Value']

conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

def fetch_sql_statements_from_s3():
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket='repair-lneil', Key='ddl.sql')
        sql_statements = response['Body'].read().decode('utf-8')
        return sql_statements
    except Exception as e:
        raise e

def lambda_handler(event, context):
    user_attributes = event['request']['userAttributes']
    
    if 'custom:tenant_tag' not in user_attributes:
        return {
            'statusCode': 400,
            'body': json.dumps('Tenant tag not found in user attributes')
        }
    
    tenant = user_attributes['custom:tenant_tag']
    
    try:
        sql_statements = fetch_sql_statements_from_s3()
        sql_statements = sql_statements.replace('TENANT', tenant)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching or replacing SQL statements: ' + str(e))
        }
    
    try:
        print("connecting...")
        cursor = conn.cursor()
        cursor.execute(sql_statements)
        conn.commit()
        cursor.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Tables created successfully for tenant: ' + tenant)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating tables: ' + str(e))
        }
    finally:
        conn.close()  # Close the database connection in the finally block