import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("employees.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    position TEXT,
    salary INTEGER
)
""")
conn.commit()

# Insert demo data only if database is empty
cursor.execute("SELECT COUNT(*) FROM employees")
count = cursor.fetchone()[0]

if count == 0:
    sample_data = [
        ("John Smith","IT","Software Engineer",5500),
        ("Mary Johnson","HR","HR Manager",4800),
        ("David Brown","Finance","Accountant",5200),
        ("Aisha Bello","Sales","Sales Executive",4500),
        ("Peter James","IT","Backend Developer",6000),
        ("Fatima Musa","Marketing","Marketing Officer",4700),
        ("Grace Williams","Operations","Operations Manager",6200),
        ("Michael Lee","Support","Application Support",5000)
    ]

    cursor.executemany(
        "INSERT INTO employees(name,department,position,salary) VALUES(?,?,?,?)",
        sample_data
    )
    conn.commit()

# ---------------- LOAD DATA ----------------
df = pd.read_sql_query("SELECT * FROM employees", conn)

# ---------------- HEADER ----------------
st.title("👨‍💼 Employee Management Dashboard")
st.caption("Professional Employee Management System built with Python, SQLite and Streamlit")

st.divider()

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Employees", len(df))

with col2:
    st.metric("Departments", df["department"].nunique())

with col3:
    st.metric("Average Salary", f"${int(df['salary'].mean())}")

with col4:
    st.metric("Highest Salary", f"${df['salary'].max()}")

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Search Employees")

search = st.sidebar.text_input("Search by Name")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["department"].unique().tolist())
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search, case=False)
    ]

if department != "All":
    filtered_df = filtered_df[
        filtered_df["department"] == department
    ]

# ---------------- CHARTS ----------------
left, right = st.columns(2)

with left:
    st.subheader("Employees by Department")

    dept = (
        filtered_df.groupby("department")
        .size()
        .reset_index(name="Employees")
    )

    st.bar_chart(
        dept.set_index("department")
    )

with right:
    st.subheader("Salary Distribution")

    st.line_chart(
        filtered_df.set_index("name")["salary"]
    )

st.divider()

# ---------------- EMPLOYEE TABLE ----------------
st.subheader("Employee Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.download_button(
    "⬇ Download Employee Data",
    filtered_df.to_csv(index=False),
    file_name="employees.csv",
    mime="text/csv"
)

st.divider()

# ---------------- ADD EMPLOYEE ----------------
st.subheader("Add New Employee")

with st.form("employee_form"):

    name = st.text_input("Employee Name")

    department = st.selectbox(
        "Department",
        ["IT","HR","Finance","Sales","Marketing","Support","Operations"]
    )

    position = st.text_input("Position")

    salary = st.number_input(
        "Salary",
        min_value=1000,
        step=100
    )

    submit = st.form_submit_button("Add Employee")

    if submit:

        cursor.execute(
            """
            INSERT INTO employees(name,department,position,salary)
            VALUES(?,?,?,?)
            """,
            (name, department, position, salary)
        )

        conn.commit()

        st.success("Employee Added Successfully!")

        st.rerun()
