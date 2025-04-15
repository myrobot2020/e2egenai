conn = psycopg2.connect(
    dbname="db5",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

#conn.rollback()  # ❗ Clear the broken transaction state
