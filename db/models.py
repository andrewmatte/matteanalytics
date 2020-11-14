import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import execute_batch
import os
import hashlib


DB_USER = os.environ.get('db_user')
DB_PASSWD = os.environ.get('db_pass')
DB_SCHEMA = os.environ.get('db_schema')


def execute(query, params = []):
    conn = psycopg2.connect(user = DB_USER,
                            password = DB_PASSWD,
                            host = "localhost",
                            database = DB_SCHEMA)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    h = hashlib.new('md5')
    h.update(bytes(query, 'utf8'))
    hashed_stmt = h.hexdigest()
    execute_string = ' ('
    for _ in range(len(params)):
        execute_string += '%s,'
    if len(params) > 0:
        execute_string = execute_string[:-1] + ')'
    prepared_statement = "PREPARE stmt_" + hashed_stmt + " AS " + query
    cursor.execute(prepared_statement)
    cursor.execute("EXECUTE stmt_" + hashed_stmt + execute_string, params)
    cursor.execute("DEALLOCATE stmt_" + hashed_stmt)
    try:
        return cursor.fetchall()
    except:
        return []