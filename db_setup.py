import sqlite3

conn = sqlite3.connect("logger.db",check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE sensor_data(id Integer Primary Key, created_at timestamp, humidity real, temperature real, dew_point real)")
cur.close()
conn.commit()
