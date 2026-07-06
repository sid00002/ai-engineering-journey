import sqlite3

DATABASE_NAME = "customer_support.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        order_id TEXT PRIMARY KEY,
        customer_name TEXT,
        product_id TEXT,
        status TEXT,
        estimated_delivery TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_email TEXT,
        issue_description TEXT,
        priority TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def seed_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")

    count = cursor.fetchone()[0]
    if count == 0:
        orders = [
            (
                "ORD1001",
                "Alice",
                "P101",
                "Shipped",
                "2026-07-08"
            ),
            (
                "ORD1002",
                "Bob",
                "P102",
                "Processing",
                "2026-07-10"
            ),
            (
                "ORD1003",
                "Charlie",
                "P103",
                "Delivered",
                "2026-07-02"
            )
        ]
        cursor.executemany("""
        INSERT INTO orders
        VALUES(?,?,?,?,?)
        """, orders)
    conn.commit()
    conn.close()


def setup_database():
    initialize_database()
    seed_orders()