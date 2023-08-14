import psycopg2
import json
import boto3


def lambda_handler(event, context):
    print(event)
    ssm = boto3.client('ssm')
    payload = json.loads(event['Payload'])
    tenant = payload['TENANT']
    if not tenant:
        return {
            'statusCode': 400,
            'body': json.dumps('TENANT parameter missing in the payload')
        }
    sql_statements = sql_statements.replace('TENANT', tenant)
    try:
        sql_statements = ssm.get_parameter(Name='/repair/ddl/s3', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get /repair/ddl/s3')
        }
    try:
        db_name = ssm.get_parameter(Name='/repair/DBParameter', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get /repair/DBParameter')
        }
    try:
        db_user = ssm.get_parameter(Name='/repair/UserParameter', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get /repair/UserParameter')
        }
    try:
        db_password = ssm.get_parameter(Name='/repair/PasswordParameter', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get PasswordParameter')
        }
    try:
        db_host = ssm.get_parameter(Name='/repair/HostParameter', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get /repair/HostParameter')
        }
    try:
        db_port = ssm.get_parameter(Name='/repair/PortParameter', WithDecryption=False)['Parameter']['Value']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('SSM: failed to get /repair/PortParameter')
        }

    try:
        print("connecting...")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("connected")
        cursor = conn.cursor()
        cursor.execute(sql_statements)
        conn.commit()
        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Tables created successfully for tenant: ' + tenant)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating tables: ' + str(e))
        }