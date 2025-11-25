import pyodbc
import sys



SERVER = r"ALVIN"


DATABASES = ["Store_UK", "Store_US", "Store_Japan"]


DRIVER = "{ODBC Driver 17 for SQL Server}"  
def connect(dbname):
    conn_str = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={dbname};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def menu_databases():
    print("\n=== Select a database ===")
    for i, db in enumerate(DATABASES, 1):
        print(f"{i}. {db}")
    print("0. Exit")

def menu_actions():
    print("\n--- Actions ---")
    print("1. Print data (show TOP 10 from each table)")
    print("2. Update product price (by product_id)")
    print("0. Back")

def print_data(conn):
    cur = conn.cursor()
    tables = ["Customers", "Products", "Orders", "OrderItems", "Payments"]
    for t in tables:
        print(f"\n--- {t} (TOP 10) ---")
        cur.execute(f"SELECT TOP 10 * FROM dbo.{t}")
        cols = [d[0] for d in cur.description]
        print(" | ".join(cols))
        for row in cur.fetchall():
            print(" | ".join(str(x) for x in row))

def update_product_price(conn):
    cur = conn.cursor()
    try:
        pid = int(input("Enter product_id to update: ").strip())
        new_price = float(input("Enter new price: ").strip())
        cur.execute("UPDATE dbo.Products SET price=? WHERE product_id=?", (new_price, pid))
        conn.commit()
        print("✅ Updated. New row:")
        cur.execute("SELECT product_id, sku, name, price FROM dbo.Products WHERE product_id=?", (pid,))
        row = cur.fetchone()
        if row:
            print(row)
        else:
            print("No product with that product_id.")
    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)

def main():
    while True:
        menu_databases()
        choice = input("Choice: ").strip()
        if choice == "0":
            sys.exit(0)
        if choice in {"1", "2", "3"}:
            dbname = DATABASES[int(choice) - 1]
            print(f"\nConnecting to {dbname} ...")
            try:
                conn = connect(dbname)
            except Exception as e:
                print("❌ Connection error:", e)
                continue

            while True:
                menu_actions()
                act = input("Action: ").strip()
                if act == "0":
                    conn.close()
                    break
                elif act == "1":
                    print_data(conn)
                elif act == "2":
                    update_product_price(conn)
                else:
                    print("Invalid action.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
