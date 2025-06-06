import psycopg2

def write_to_postgres(data, table_name):
    conn = psycopg2.connect(
        dbname="postgresDB",
        user="admin",
        password="admin",
        host="postgres",
        port=5432
    )
    cur = conn.cursor()
    for row in data:
        cur.execute(f"INSERT INTO {table_name} VALUES (%s, %s, %s)", row)
    conn.commit()
    cur.close()
    conn.close()
