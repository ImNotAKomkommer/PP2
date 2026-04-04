import csv
from connect import connect


def execute_sql_file(filename):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            sql = file.read()
            cur.execute(sql)
        conn.commit()
        print(f"{filename} executed successfully.")
    except Exception as e:
        print(f"Error executing {filename}:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def create_table():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                phone VARCHAR(20) NOT NULL UNIQUE
            )
        """)
        conn.commit()
        print("Table 'phonebook' is ready.")
    except Exception as e:
        print("Error creating table:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def load_functions():
    execute_sql_file("functions.sql")


def load_procedures():
    execute_sql_file("procedures.sql")


def insert_from_csv(filename):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute(
                    "CALL insert_or_update_user(%s, %s, %s)",
                    (row["first_name"], row["last_name"], row["phone"])
                )
        conn.commit()
        print("CSV data inserted/updated successfully.")
    except Exception as e:
        print("Error inserting from CSV:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_from_console():
    conn = connect()
    if conn is None:
        return

    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    phone = input("Enter phone: ").strip()

    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_or_update_user(%s, %s, %s)",
            (first_name, last_name, phone)
        )
        conn.commit()
        print("User inserted or updated successfully.")
    except Exception as e:
        print("Error inserting/updating user:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_many_from_console():
    conn = connect()
    if conn is None:
        return

    try:
        count = int(input("How many users do you want to insert? ").strip())
    except ValueError:
        print("Invalid number.")
        return

    first_names = []
    last_names = []
    phones = []

    for i in range(count):
        print(f"\nUser {i + 1}:")
        first_names.append(input("First name: ").strip())
        last_names.append(input("Last name: ").strip())
        phones.append(input("Phone: ").strip())

    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_users(%s, %s, %s)",
            (first_names, last_names, phones)
        )

        cur.execute("SELECT * FROM temp_incorrect_data")
        incorrect_rows = cur.fetchall()

        conn.commit()

        print("Bulk insert completed.")
        if incorrect_rows:
            print("\nIncorrect data:")
            for row in incorrect_rows:
                print(f"First name: {row[0]}, Last name: {row[1]}, Phone: {row[2]}")
        else:
            print("No incorrect data found.")

    except Exception as e:
        print("Error inserting many users:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def search_by_pattern():
    conn = connect()
    if conn is None:
        return

    pattern = input("Enter pattern to search: ").strip()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()

        if rows:
            print("\nSearch results:")
            for row in rows:
                print(f"ID: {row[0]}, First name: {row[1]}, Last name: {row[2]}, Phone: {row[3]}")
        else:
            print("No matching records found.")

    except Exception as e:
        print("Error searching records:", e)

    finally:
        cur.close()
        conn.close()


def show_paginated():
    conn = connect()
    if conn is None:
        return

    try:
        limit = int(input("Enter LIMIT: ").strip())
        offset = int(input("Enter OFFSET: ").strip())
    except ValueError:
        print("Limit and offset must be integers.")
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        if rows:
            print("\nPaginated results:")
            for row in rows:
                print(f"ID: {row[0]}, First name: {row[1]}, Last name: {row[2]}, Phone: {row[3]}")
        else:
            print("No data found.")

    except Exception as e:
        print("Error getting paginated data:", e)

    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, first_name, last_name, phone
            FROM phonebook
            ORDER BY id
        """)
        rows = cur.fetchall()

        if rows:
            print("\nAll contacts:")
            for row in rows:
                print(f"ID: {row[0]}, First name: {row[1]}, Last name: {row[2]}, Phone: {row[3]}")
        else:
            print("PhoneBook is empty.")
    except Exception as e:
        print("Error showing contacts:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    conn = connect()
    if conn is None:
        return

    value = input("Enter first name or phone to delete: ").strip()
    cur = conn.cursor()

    try:
        cur.execute("CALL delete_user(%s)", (value,))
        conn.commit()
        print("Delete procedure executed.")
    except Exception as e:
        print("Error deleting contact:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Load functions.sql")
        print("3. Load procedures.sql")
        print("4. Insert one user from console")
        print("5. Insert many users from console")
        print("6. Search records by pattern")
        print("7. Show data with pagination")
        print("8. Show all contacts")
        print("9. Delete by username or phone")
        print("10. Insert data from CSV")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            load_functions()
        elif choice == "3":
            load_procedures()
        elif choice == "4":
            insert_from_console()
        elif choice == "5":
            insert_many_from_console()
        elif choice == "6":
            search_by_pattern()
        elif choice == "7":
            show_paginated()
        elif choice == "8":
            show_all_contacts()
        elif choice == "9":
            delete_contact()
        elif choice == "10":
            insert_from_csv("contacts.csv")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()