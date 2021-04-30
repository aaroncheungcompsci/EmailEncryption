# database.py
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


def initialize_table(cur, conn):
    # execute function for SQL queries
    cur.execute("""CREATE TABLE messages (
                ID int not null PRIMARY KEY,
                SENDER text not null,
                RECIPIENT text not null,
                SUBJECT text,
                MESSAGE blob
                )""")
    conn.commit()


def insert_element(sender, recipient, subject, message, cur, conn):
    """Insert element to table."""
    cur.execute("SELECT COUNT(*) from messages")
    key_to_assign = cur.fetchall()
    key_to_assign = key_to_assign[0][0] + 1

    cur.execute(f"""INSERT INTO messages (ID, SENDER, RECIPIENT, SUBJECT, MESSAGE)
                    VALUES ({key_to_assign}, '{sender}', '{recipient}', '{subject}', ?)""", [sqlite3.Binary(message)])
    conn.commit()


def drop_table(cur):
    """Drops the table."""
    cur.execute("DROP TABLE messages")


def delete_elements(condition, cur, conn):
    """Deletes rows from table depending on the provided condition"""
    cur.execute(f"DELETE FROM messages WHERE {condition}")
    conn.commit()


def display_elements(cur, conn):
    """Display row contents to console."""
    cur.execute("SELECT * FROM messages")
    list = cur.fetchall()
    for i in range(len(list)):
        print(list[i])
    conn.commit()


def get_row_from_id(id, cur):
    """Get the row number."""
    cur.execute(f"SELECT * from messages WHERE ID={id}")
    return cur.fetchone()


def get_number_of_rows(cur):
    """Get total number of rows."""
    cur.execute("SELECT COUNT(*) from messages")
    extract = cur.fetchone()
    return extract[0]

# ------------- debugging function calls -----------------
# initialize_table()
# drop_table()
# insert_element("test@gmail.com", "secondtest@gmail.com", "test subject", b"test message")
# display_elements(c, conn)
# c.execute("SELECT COUNT() from messages")
# extract = c.fetchall()
# number = [row[0] for row in extract]
# number = extract[0][0]
# delete_elements("ID>1", c, conn)

# row_data = get_row_from_id(3, c)
# private_key = import_key("private_key.pem")
# decrypted_message = decrypt(private_key, row_data[4])
# print(decrypted_message.decode('ascii'))


