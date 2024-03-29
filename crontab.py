from database_postgres.config import get_db
import time

con, cur = get_db()
print(f"Start: {con, cur}")
def crontab():
    print("Start")
    while True:
        update_status_query = """UPDATE token_managers SET token_status = 1 WHERE created_date < NOW() - INTERVAL '5 minutes' and token_status = 0"""
        cur.execute(update_status_query)
        update_update_date_query="""UPDATE token_managers SET updated_date = NOW() WHERE token_status = 0"""
        cur.execute(update_update_date_query)
        con.commit()
        time.sleep(10)
        print("Update status success")

if __name__ == '__main__':
    crontab()