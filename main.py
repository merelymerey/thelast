import psycopg2
from config import DB_CONFIG

def create_table():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("True")
    except Exception as e:
        print("-1 ", e)

def add_entry():
    name = input("name ")
    phone = input("number ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s);", (name, phone))
        conn.commit()
        cur.close()
        conn.close()
        print("True")
    except Exception as e:
        print("-1:", e)

def view_all():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM phonebook;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("-1:", e)

def find_by_phone():
    phone = input("number ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM phonebook WHERE phone = %s;", (phone,))
        result = cur.fetchone()
        print(result)
        cur.close()
        conn.close()
    except Exception as e:
        print("-1:", e)

def update_phone():
    name = input("new name ")
    new_phone = input("new number ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s;", (new_phone, name))
        conn.commit()
        print("+1 ")
        cur.close()
        conn.close()
    except Exception as e:
        print("-1 ", e)

def delete_by_name():
    name = input("delate ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM phonebook WHERE first_name = %s;", (name,))
        conn.commit()
        print("True")
        cur.close()
        conn.close()
    except Exception as e:
        print("ERROR:", e)

def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Create a table")
        print("2. Add elements")
        print("3. Show all elements")
        print("4. search an element")
        print("5. update")
        print("6. delete")
        print("0. exit")

        choice = input("please select the command:")

        if choice == '1':
            create_table()
        elif choice == '2':
            add_entry()
        elif choice == '3':
            view_all()
        elif choice == '4':
            find_by_phone()
        elif choice == '5':
            update_phone()
        elif choice == '6':
            delete_by_name()
        elif choice == '0':
            print("duai ")
            break
        else:
            print("kaita ")

if __name__ == "__main__":
    main()