import sys
import pymysql
import datetime

INTERVAL = '5 hour'

def load_pw():
    x = "3219ahn7fg53esartnoC$"
    return "".join(reversed(x[:7] + x[12:]))

def dbConnection(dbConfig, query):
    try:
        conn = pymysql.connect(dbConfig["host"], user=dbConfig["user"], passwd=dbConfig["password"],
                               db=dbConfig["db_name"])
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    print("SUCCESS: Connection to RDS mysql instance succeeded")
    cur = conn.cursor()
    cur.execute(query)


    conn.close()

    return cur

def get_queries():
    dbConfig = {"host": "deduca.cos61ph0fzqs.us-east-1.rds.amazonaws.com",
                "user": "admin",
                "password": load_pw(),
                "db_name": "employees"
                }

    query = "select start_time, user_host, rows_examined, sql_text from mysql.slow_log where user_host NOT LIKE '%rdsadmin%' and start_time >date_sub(UTC_TIMESTAMP(), interval "
    query += INTERVAL
    query += ") and (lower(sql_text) LIKE 'select%' or lower(sql_text) LIKE 'update%' or lower(sql_text) LIKE 'insert%' or lower(sql_text) LIKE 'delete%')"
    cur = dbConnection(dbConfig, query)
    rows = []
    for row in cur:
        #role = ''
        #datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S')
        timestamp = row[0].strftime('%m-%d-%y %H:%M:%S')
        user = row[1].split('[')[0]
        rows_examined = row[2]
        text = row[3].decode()
        rows.append({'role': user, 'user': user, 'rows_examined': rows_examined, 'timestamp': timestamp, 'text': text})
    return rows


if __name__ == "__main__":
    for q in get_queries():
        print(q)
    #print(load_pw())