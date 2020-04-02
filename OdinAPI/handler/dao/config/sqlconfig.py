import os
from dotenv import load_dotenv
load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
cloud_sql_connection_name = os.getenv('CLOUD_SQL_CONNECTION_NAME')

db_config = {
    'username': db_user,
    'password': db_pass,
    'database': db_name,
    'host': cloud_sql_connection_name,
    'port': 5432
}
