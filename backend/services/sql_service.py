import sqlite3

def read_sql_query(sql: str, db: str = "db/cars.db"):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        conn.close()
        return rows, col_names
    except Exception as e:
        return [[f"Error: {str(e)}"]], ["error"]
