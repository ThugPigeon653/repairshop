import json
import os
import psycopg2
from psycopg2 import sql
import boto3

ssm = boto3.client('ssm')

def get_parameter_value(parameter_name):
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error retrieving parameter value: {e}")
        return None

def lambda_handler(event, context):
    try:
        # Retrieve search parameters and table name from the event payload
        search_params = event.get('search_params', {})
        table_name = event.get('table_name')
        select_value = event.get('select_value')
        select_columns = event.get('select_columns', [])

        # Validate input payload
        if not isinstance(search_params, dict):
            raise ValueError('Invalid search parameters')
        if not isinstance(table_name, str) or not table_name:
            raise ValueError('Invalid table name')

        # Construct the SQL query dynamically based on the search parameters, table name, and select value
        if select_columns:
            select_clause = sql.SQL(', ').join(sql.Identifier(column) for column in select_columns)
        else:
            select_clause = sql.SQL('*')

        query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
            select_clause,
            sql.Identifier(table_name),
            sql.SQL(' AND ').join(
                sql.SQL("{column} ILIKE {search_term}").format(
                    column=sql.Identifier(column),
                    search_term=sql.Literal(search_term)
                )
                for column, search_term in search_params.items()
            )
        )

        # Retrieve database connection information from SSM Parameter Store
        db = get_parameter_value(os.environ['DB'])
        user = get_parameter_value(os.environ['USER'])
        password = get_parameter_value(os.environ['PASSWORD'])
        host = get_parameter_value(os.environ['HOST'])
        port = get_parameter_value(os.environ['PORT'])

        # Connect to the database and execute the query
        conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Convert the result into a list of dictionaries
        results = []
        for row in rows:
            result = {column_names[i]: value for i, value in enumerate(row)}
            results.append(result)

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the search results
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    except Exception as e:
        # Handle any exceptions and return an error response
        error_message = str(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }