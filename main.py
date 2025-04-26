import psycopg2
import csv
from config import DB_CONFIG

with open("data.csv", mode = "w", newline = '') as file:
    pass
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
        print("Table created.")
    except Exception as e:
        print("Error:", e)

def add_entry_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s);", (name, phone))
        conn.commit()
        cur.close()
        conn.close()
        print("Entry added.")
    except Exception as e:
        print("Error:", e)

import csv

def add_entries_from_csv():
    filename = input("Enter CSV filename (example: data.csv): ")

    try:
        # Проверяем существует ли файл
        try:
            open(filename, 'r').close()
        except FileNotFoundError:
            print(f"{filename} doesnt exist, creating the new onw")
            with open(filename, 'w', newline='') as file:
                pass  # Просто создаем пустой файл
            print(f"{filename} was created.")

        while True:
            action = input("choose the command: (1) add into the file, (2) insert data to database, (0) exit: ")
            if action == '1':
                name = input("name: ")
                phone = input("phone number: ")
                with open(filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, phone])
                print("success.")
            elif action == '2':
                conn = psycopg2.connect(**DB_CONFIG)
                cur = conn.cursor()
                with open(filename, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) == 2:
                            name, phone = row
                            cur.execute(
                                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
                                (name, phone)
                            )
                conn.commit()
                cur.close()
                conn.close()
                print("success.")
            elif action == '0':
                print("exit CSV.")
                break
            else:
                print("error, try again.")

    except Exception as e:
        print("ERROR:", e)


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
        print("Error:", e)

def search_entries():
    filter_choice = input("Search by (1) name or (2) phone: ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if filter_choice == '1':
            name = input("Enter name: ")
            cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s;", ('%' + name + '%',))
        elif filter_choice == '2':
            phone = input("Enter phone: ")
            cur.execute("SELECT * FROM phonebook WHERE phone = %s;", (phone,))
        else:
            print("Invalid choice.")
            return
        result = cur.fetchall()
        for row in result:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

def update_entry():
    id = input("Enter ID to update: ")
    new_name = input("Enter new name (or leave empty): ")
    new_phone = input("Enter new phone (or leave empty): ")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if new_name:
            cur.execute("UPDATE phonebook SET first_name = %s WHERE id = %s;", (new_name, id))
        if new_phone:
            cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s;", (new_phone, id))
        conn.commit()
        cur.close()
        conn.close()
        print("Entry updated.")
    except Exception as e:
        print("Error:", e)

def delete_entry():
    delete_choice = input("Delete by (1) name or (2) phone: ")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if delete_choice == '1':
            name = input("Enter name: ")
            cur.execute("DELETE FROM phonebook WHERE first_name = %s;", (name,))
        elif delete_choice == '2':
            phone = input("Enter phone: ")
            cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
        else:
            print("Invalid choice.")
            return
        conn.commit()
        cur.close()
        conn.close()
        print("Entry deleted.")
    except Exception as e:
        print("Error:", e)

def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Create table")
        print("2. Add entry (console)")
        print("3. Add entries (CSV)")
        print("4. View all entries")
        print("5. Search entry")
        print("6. Update entry")
        print("7. Delete entry")
        print("0. Exit")

        choice = input("Select command: ")

        if choice == '1':
            create_table()
        elif choice == '2':
            add_entry_from_console()
        elif choice == '3':
            add_entries_from_csv()
        elif choice == '4':
            view_all()
        elif choice == '5':
            search_entries()
        elif choice == '6':
            update_entry()
        elif choice == '7':
            delete_entry()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
