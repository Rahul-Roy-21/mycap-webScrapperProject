import sqlite3

def connect(dbname):

    conn = sqlite3.connect(dbname)
    # Create Table oyo_rooms if it doesn't Exist
    conn.execute("CREATE TABLE IF NOT EXISTS oyo_rooms (NAME TEXT, STREET TEXT, DIST TEXT, RATING TEXT, REVIEWS TEXT, SUMMARY TEXT, FINALPRICE TEXT, SLASHEDPRICE TEXT, PCTAGEOFF TEXT)")

    conn.close()

def insert_row(dbname, values):
    conn = sqlite3.connect(dbname)

    sql = "INSERT INTO oyo_rooms (NAME, STREET, DIST, RATING, REVIEWS, SUMMARY, FINALPRICE, SLASHEDPRICE, PCTAGEOFF) VALUES (?,?,?,?,?,?,?,?,?)"
    conn.execute(sql, values)
    conn.commit()

    conn.close()

def show_db(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM oyo_rooms")

    for index, row in enumerate(c.fetchall()):
        print('{} => {}'.format(index, row))