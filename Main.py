import streamlit as st
import storage
import complaints
import cart_logic

def main():
    st.set_page_config(page_title="SIC E-Commerce", layout="wide")
    
    # 1. Initialize Session State (This keeps the cart active)
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Products", "My Cart", "File a Complaint", "Admin"])

    # --- OPTION 1: PRODUCTS ---
    if choice == "Products":
        st.header("Available Products")
        # Dhruv (Research) can add more products here
        products = [
            {"id": 101, "name": "Laptop", "price": 800},
            {"id": 102, "name": "Headphones", "price": 50},
        ]
        for p in products:
            col1, col2 = st.columns([3, 1])
            col1.write(f"*{p['name']}* - ${p['price']}")
            if col2.button(f"Add to Cart", key=p['id']):
                st.session_state.cart.append(p)
                st.toast(f"{p['name']} added!")

    # --- OPTION 4: COMPLAINTS ---
    elif choice == "File a Complaint":
        st.header("Help & Support")
        with st.form("complaint_form"):
            u_name = st.text_input("Name")
            msg = st.text_area("What is your issue?")
            pri = st.select_slider("Priority", options=["Low", "Medium", "High"])
            submit = st.form_submit_button("Submit Ticket")
            
            if submit:
                # Structured data logic
                new_ticket = {"user": u_name, "issue": msg, "priority": pri, "status": "Open"}
                existing_data = storage.load_data("complaints_db.json")
                existing_data.append(new_ticket)
                storage.save_data("complaints_db.json", existing_data)
                st.success("Complaint Filed Successfully!")

if __name__ == "__main__":
    main()