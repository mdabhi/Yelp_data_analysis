import time
import pymysql.cursors

def run_queries(MYSQL_QUERIES):
    MYSQL_HOST = "marmoset04.shoshin.uwaterloo.ca"
    MYSQL_USER = "username"
    MYSQL_PASS = "user_password"
    MYSQL_DB = "db656_username"

    # connect to DB
    timestamp = time.time()
    comm = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
        password=MYSQL_PASS, db=MYSQL_DB)
    print("\nConnected to {} on: {}@{} ({:.0f}ms).\n\nRunning queries..."
        .format(MYSQL_DB, MYSQL_USER, MYSQL_HOST,
        1000 * (time.time() - timestamp)))

    # run queries
    with comm.cursor() as cursor:
        ret, result = [], []
        for i in MYSQL_QUERIES:
            timestamp = time.time()
            ret.append(cursor.execute(i))
            result.append(cursor.fetchall())
            print("Query complete ({:.0f}ms)."
                .format(1000 * (time.time() - timestamp)))
    comm.close()
    print()
    return ret, result

