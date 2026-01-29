import streamlit as st
import database  # Optimized for unique usernames and passwords
import cart_logic 
import complaints 

def main():
    # Set professional page configuration
    st.set_page_config(page_title="SIC Marketplace | Secure Portal", layout="centered")
    
    # Initialize database tables with unique constraints
    database.create_tables()

    # --- SESSION STATE INITIALIZATION ---
    # track login status and whether we are showing Login or Signup screen
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "signup"  # Amazon-style: Signup is the default landing
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # --- PART A: THE GATEKEEPER (SIGNUP/LOGIN) ---
    if not st.session_state.logged_in:
        
        # --- 1. CREATE ACCOUNT INTERFACE (PRIMARY) ---
        if st.session_state.auth_mode == "signup":
            st.header("Create Account")
            
            # Professional Toggle for Role selection
            is_seller = st.toggle("Register as a Seller", help="Switch on if you want to sell products")
            role_label = "Seller" if is_seller else "Buyer"
            st.info(f"Registering as a new **{role_label}**")

            with st.form("signup_form"):
                full_name = st.text_input("Full Name" if not is_seller else "Store Name")
                # New: Unique username and password requirements
                username = st.text_input("Choose Unique Username")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Create Account"):
                    if is_seller:
                        # Sellers use store name as unique identifier
                        success = database.add_seller(full_name, password)
                    else:
                        # Buyers use unique username and email
                        success = database.add_user(full_name, username, email, password)
                    
                    if success:
                        st.success("Account created successfully! Please sign in below.")
                    else:
                        st.error("Error: Username or Email already exists. Please try another.")

            # Link to switch to Login view
            st.write("---")
            if st.button("Already have an account? Sign in"):
                st.session_state.auth_mode = "login"
                st.rerun()

        # --- 2. LOGIN INTERFACE (SECONDARY) ---
        else:
            st.header("Sign In")
            login_role = st.radio("Account Type:", ["Buyer", "Seller"], horizontal=True)
            user_input = st.text_input("Username" if login_role == "Buyer" else "Store Name")
            pass_input = st.text_input("Password", type="password")

            if st.button("Sign In"):
                # Authenticate using the new secure login functions
                if login_role == "Buyer":
                    user = database.login_user(user_input, pass_input)
                else:
                    user = database.login_seller(user_input, pass_input)
                
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_role = login_role
                    st.session_state.user_id = user[0]
                    st.rerun()
                else:
                    st.error("Invalid Username or Password. Please try again.")

            # Link to switch back to Signup view
            st.write("---")
            if st.button("New to SIC? Create an account"):
                st.session_state.auth_mode = "signup"
                st.rerun()

    # --- PART B: THE DASHBOARD (AFTER LOGIN) ---
    else:
        st.sidebar.title(f"👤 {st.session_state.user_role} Mode")
        st.sidebar.info(f"Logged in as: ID {st.session_state.user_id}")
        
        if st.sidebar.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.auth_mode = "login"
            st.session_state.cart = []
            st.rerun()

        st.sidebar.divider()

        # Dynamic Sidebar Menu based on Authenticated Role
        if st.session_state.user_role == "Buyer":
            menu = ["Shop Products", "My Cart", "File a Complaint"]
        else:
            menu = ["My Inventory", "Add New Product", "Sales Data"]

        choice = st.sidebar.radio("Navigation", menu)

        # Buyer View: Fetch and Display Products
        if choice == "Shop Products":
            st.header("Browse Marketplace")
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            conn.close()

            if not products:
                st.info("The marketplace is currently empty.")
            else:
                for p in products:
                    p_id, p_name, p_price = p[0], p[1], p[2]
                    col1, col2 = st.columns([4, 1])
                    col1.write(f"**{p_name}** — ${p_price:.2f}")
                    if col2.button("Add", key=f"btn_{p_id}"):
                        st.session_state.cart.append({"id": p_id, "name": p_name, "price": p_price})
                        st.toast(f"Added {p_name}")

        # Seller View: Form to add new research products
        elif choice == "Add New Product":
            st.header("List New Product")
            with st.form("product_form"):
                name = st.text_input("Name")
                price = st.number_input("Price", min_value=0.01)
                cat = st.selectbox("Category", ["Electronics", "Research Tools", "Books"])
                if st.form_submit_button("List Product"):
                    database.add_product(name, price, cat, st.session_state.user_id)
                    st.success("Product listed!")

if __name__ == "__main__":
    main()