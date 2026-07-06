import streamlit as st
from database import add_employee, get_employees

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide"
)

st.title("👨‍💼 Employee Management System")

st.header("Add Employee")

name = st.text_input("Full Name")
email = st.text_input("Email")
department = st.text_input("Department")
position = st.text_input("Position")
salary = st.number_input("Salary", min_value=0.0)

if st.button("Add Employee"):
    add_employee(name, email, department, position, salary)
    st.success("Employee added successfully!")

st.divider()

st.header("Employee List")

employees = get_employees()

st.dataframe(
    employees,
    use_container_width=True
)
