import streamlit as st
import sqlite3
from database import create_tables

create_tables()

st.set_page_config(
    page_title="Pharmacy Management System",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Pharmacy Management System")

st.sidebar.title("MENU")

option = st.sidebar.selectbox(
    "Select",
    [
        "Dashboard",
        "Medicines",
        "Customers",
        "Suppliers",
        "Sales",
        "Purchases",
        "Reports"
    ]
)

if option == "Dashboard":
    st.header("🏠 Pharmacy Dashboard")

    conn = sqlite3.connect("pharmacy.db")

    medicine_count = conn.execute(
        "SELECT COUNT(*) FROM medicines"
    ).fetchone()[0]

    customer_count = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    supplier_count = conn.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    sales_count = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    purchase_count = conn.execute(
        "SELECT COUNT(*) FROM purchases"
    ).fetchone()[0]

    conn.close()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💊 Medicines", medicine_count)

    with col2:
        st.metric("👥 Customers", customer_count)

    with col3:
        st.metric("🚚 Suppliers", supplier_count)

    col4, col5 = st.columns(2)

    with col4:
        st.metric("🛒 Sales", sales_count)

    with col5:
        st.metric("📦 Purchases", purchase_count)
elif option == "Medicines":
    st.header("💊 Medicine Management")

    name = st.text_input("Medicine Name")
    category = st.text_input("Category")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.01)
    expiry_date = st.date_input("Expiry Date")
    supplier = st.text_input("Supplier")

    if st.button("Add Medicine"):

        if name == "":
            st.error("Please enter the medicine name.")

        else:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO medicines
                (name, category, quantity, price, expiry_date, supplier)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                category,
                quantity,
                price,
                str(expiry_date),
                supplier
            ))

            conn.commit()
            conn.close()

            st.success("Medicine added successfully!")
            st.subheader("📋 Medicine List")

    conn = sqlite3.connect("pharmacy.db")

    medicines = conn.execute("""
        SELECT id, name, category, quantity, price, expiry_date, supplier
        FROM medicines
    """).fetchall()

    conn.close()

    if medicines:
        st.dataframe(
            medicines,
            column_config={
                "id": "ID",
                "name": "Medicine Name",
                "category": "Category",
                "quantity": "Quantity",
                "price": "Price",
                "expiry_date": "Expiry Date",
                "supplier": "Supplier"
            },
            use_container_width=True
        )
    else:
        st.info("No medicines added yet.")
        st.subheader("🗑️ Delete Medicine")

    delete_id = st.number_input(
        "Enter Medicine ID to Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Medicine"):
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM medicines WHERE id = ?",
            (delete_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            st.success("Medicine deleted successfully!")
        else:
            st.warning("Medicine ID not found.")

        conn.close()
        st.subheader("✏️ Update Medicine")

    update_id = st.number_input(
        "Enter Medicine ID to Update",
        min_value=1,
        step=1,
        key="update_id"
    )

    new_quantity = st.number_input(
        "New Quantity",
        min_value=0,
        step=1,
        key="new_quantity"
    )

    new_price = st.number_input(
        "New Price",
        min_value=0.0,
        step=0.01,
        key="new_price"
    )

    if st.button("Update Medicine"):

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE medicines
            SET quantity = ?, price = ?
            WHERE id = ?
        """, (
            new_quantity,
            new_price,
            update_id
        ))

        conn.commit()

        if cursor.rowcount > 0:
            st.success("Medicine updated successfully!")
        else:
            st.warning("Medicine ID not found.")

        conn.close()

elif option == "Customers":
    st.header("👥 Customer Management")

    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")

    if st.button("Add Customer"):

        if name == "":
            st.error("Please enter the customer name.")

        else:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO customers
                (name, phone, address)
                VALUES (?, ?, ?)
            """, (
                name,
                phone,
                address
            ))

            conn.commit()
            conn.close()

            st.success("Customer added successfully!")
            st.subheader("📋 Customer List")

    conn = sqlite3.connect("pharmacy.db")

    customers = conn.execute("""
        SELECT id, name, phone, address
        FROM customers
    """).fetchall()

    conn.close()

    if customers:
        st.dataframe(
            customers,
            column_config={
                "id": "ID",
                "name": "Customer Name",
                "phone": "Phone Number",
                "address": "Address"
            },
            use_container_width=True
        )
    else:
        st.info("No customers added yet.")

elif option == "Suppliers":
    st.header("🚚 Supplier Management")

    name = st.text_input("Supplier Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")

    if st.button("Add Supplier"):

        if name == "":
            st.error("Please enter the supplier name.")

        else:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO suppliers
                (name, phone, address)
                VALUES (?, ?, ?)
            """, (
                name,
                phone,
                address
            ))

            conn.commit()
            conn.close()

            st.success("Supplier added successfully!")
            st.subheader("📋 Supplier List")

    conn = sqlite3.connect("pharmacy.db")

    suppliers = conn.execute("""
        SELECT id, name, phone, address
        FROM suppliers
    """).fetchall()

    conn.close()

    if suppliers:
        st.dataframe(
            suppliers,
            column_config={
                "id": "ID",
                "name": "Supplier Name",
                "phone": "Phone Number",
                "address": "Address"
            },
            use_container_width=True
        )
    else:
        st.info("No suppliers added yet.")
elif option == "Sales":
    st.header("🛒 Sales Management")

    medicine_name = st.text_input("Medicine Name")
    quantity = st.number_input("Quantity Sold", min_value=1, step=1)
    total_price = st.number_input("Total Price", min_value=0.0, step=0.01)
    sale_date = st.date_input("Sale Date")

    if st.button("Record Sale"):

        if medicine_name == "":
            st.error("Please enter the medicine name.")

        else:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO sales
                (medicine_name, quantity, total_price, sale_date)
                VALUES (?, ?, ?, ?)
            """, (
                medicine_name,
                quantity,
                total_price,
                str(sale_date)
            ))

            conn.commit()
            conn.close()

            st.success("Sale recorded successfully!")
            st.subheader("📋 Sales List")

    conn = sqlite3.connect("pharmacy.db")

    sales = conn.execute("""
        SELECT id, medicine_name, quantity, total_price, sale_date
        FROM sales
    """).fetchall()

    conn.close()

    if sales:
        st.dataframe(
            sales,
            column_config={
                "id": "ID",
                "medicine_name": "Medicine Name",
                "quantity": "Quantity Sold",
                "total_price": "Total Price",
                "sale_date": "Sale Date"
            },
            use_container_width=True
        )
    else:
        st.info("No sales recorded yet.")
       
elif option == "Purchases":
    st.header("📦 Purchase Management")

    medicine_name = st.text_input("Medicine Name")
    quantity = st.number_input("Quantity Purchased", min_value=1, step=1)
    total_price = st.number_input("Total Price", min_value=0.0, step=0.01)
    purchase_date = st.date_input("Purchase Date")

    if st.button("Record Purchase"):

        if medicine_name == "":
            st.error("Please enter the medicine name.")

        else:
            conn = sqlite3.connect("pharmacy.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO purchases
                (medicine_name, quantity, total_price, purchase_date)
                VALUES (?, ?, ?, ?)
            """, (
                medicine_name,
                quantity,
                total_price,
                str(purchase_date)
            ))

            conn.commit()
            conn.close()

            st.success("Purchase recorded successfully!")
            st.subheader("📋 Purchase List")

    conn = sqlite3.connect("pharmacy.db")

    purchases = conn.execute("""
        SELECT id, medicine_name, quantity, total_price, purchase_date
        FROM purchases
    """).fetchall()

    conn.close()

    if purchases:
        st.dataframe(
            purchases,
            column_config={
                "id": "ID",
                "medicine_name": "Medicine Name",
                "quantity": "Quantity Purchased",
                "total_price": "Total Price",
                "purchase_date": "Purchase Date"
            },
            use_container_width=True
        )
    else:
        st.info("No purchases recorded yet.")

elif option == "Reports":
    st.header("📊 Pharmacy Reports")

    conn = sqlite3.connect("pharmacy.db")

    total_medicines = conn.execute(
        "SELECT COUNT(*) FROM medicines"
    ).fetchone()[0]

    total_customers = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    total_suppliers = conn.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    total_sales = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM sales"
    ).fetchone()[0]

    total_purchases = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM purchases"
    ).fetchone()[0]

    conn.close()

    st.subheader("📋 Summary Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💊 Total Medicines", total_medicines)

    with col2:
        st.metric("👥 Total Customers", total_customers)

    with col3:
        st.metric("🚚 Total Suppliers", total_suppliers)

    col4, col5 = st.columns(2)

    with col4:
        st.metric("🛒 Total Sales", f"₹{total_sales:.2f}")

    with col5:
        st.metric("📦 Total Purchases", f"₹{total_purchases:.2f}")