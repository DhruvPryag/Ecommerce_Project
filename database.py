import sqlite3

def connect_db():
    """
    Connects to the SQLite database. 
    'check_same_thread=False' is used to support Streamlit's multi-threaded environment.
    """
    conn = sqlite3.connect('ecommerce.db', check_same_thread=False)
    return conn

def create_tables():
    """
    Initializes the database schema.
    Added UNIQUE constraints for usernames and emails to prevent duplicates.
    Added password columns for security.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # 1. Users Table: Added username and password with UNIQUE constraints
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         name TEXT, 
         username TEXT UNIQUE, 
         email TEXT UNIQUE, 
         password TEXT)''')

    # 2. Sellers Table: Added password and UNIQUE constraint for store name
    cursor.execute('''CREATE TABLE IF NOT EXISTS sellers 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         store_name TEXT UNIQUE, 
         password TEXT)''')

    # 3. Products Table: Unchanged
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, 
         category TEXT, seller_id INTEGER, 
         FOREIGN KEY(seller_id) REFERENCES sellers(id))''')

    # 4. Orders Table: Unchanged
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
         total_price REAL, status TEXT,
         FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

# --- AUTHENTICATION FUNCTIONS (LOGIN) ---

def login_user(username, password):
    """
    Authenticates a Buyer using their unique username and password.
    Returns (id, name) if credentials match.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def login_seller(store_name, password):
    """
    Authenticates a Seller using their store name and password.
    Returns (id, store_name) if credentials match.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, store_name FROM sellers WHERE store_name = ? AND password = ?", (store_name, password))
    seller = cursor.fetchone()
    conn.close()
    return seller

# --- DATA ENTRY FUNCTIONS (SIGN UP) ---

def add_user(name, username, email, password):
    """
    Registers a new Buyer. 
    Returns True if successful, False if username/email is already taken.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)", 
                       (name, username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This occurs if a UNIQUE constraint is violated (e.g., duplicate username)
        return False
    finally:
        conn.close()

def add_seller(store_name, password):
    """
    Registers a new Seller.
    Returns True if successful, False if store name is already taken.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sellers (store_name, password) VALUES (?, ?)", (store_name, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- BUSINESS LOGIC FUNCTIONS ---

def add_product(name, price, category, seller_id):
    """Saves a product linked to a specific seller ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, category, seller_id) VALUES (?, ?, ?, ?)", 
                   (name, price, category, seller_id))
    conn.commit()
    conn.close()

def create_order(user_id, total_price):
    """Records a purchase linked to a specific user ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, total_price, status) VALUES (?, ?, ?)", 
                   (user_id, total_price, 'Paid'))
    conn.commit()
    conn.close()