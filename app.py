import sqlite3
import pandas as pd
import streamlit as st
import os

# --- 1. AUTO-SETUP DATABASE ---
DB_NAME = "company_data.db"

def init_db():
    if os.path.exists(DB_NAME):
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, join_date TEXT)''')
    data = [
        (1, 'Anvesh Rao', 'Engineering', 120000, '2023-01-15'),
        (2, 'Sarah Jenkins', 'Marketing', 85000, '2023-03-10'),
        (3, 'Raj Patel', 'Engineering', 115000, '2023-02-01'),
        (4, 'Emily Chen', 'Sales', 92000, '2023-04-20'),
        (5, 'Michael Scott', 'Management', 150000, '2019-05-01')
    ]
    c.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?)', data)
    conn.commit()
    conn.close()

init_db()

# --- 2. SIMULATION LOGIC ---
def natural_language_to_sql(query):
    query = query.lower()
    if "salary" in query and "average" in query:
        return "SELECT AVG(salary) as average_salary FROM employees;"
    elif "engineering" in query:
        return "SELECT * FROM employees WHERE department = 'Engineering';"
    elif "marketing" in query:
        return "SELECT * FROM employees WHERE department = 'Marketing';"
    elif "highest" in query:
        return "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1;"
    elif "count" in query:
        return "SELECT COUNT(*) as employee_count FROM employees;"
    else:
        return "SELECT * FROM employees LIMIT 5;"

# --- 3. UI ---
st.set_page_config(page_title="QueryMate", layout="wide")
st.title("🤖 QueryMate: AI SQL Agent")

with st.sidebar:
    st.header("Schema")
    st.code("Table: employees\n- id, name, department, salary")

user_query = st.text_input("Ask a question:", "Show me all employees in Engineering")

if st.button("Generate SQL & Run"):
    sql = natural_language_to_sql(user_query)
    st.subheader("Generated SQL:")
    st.code(sql, language="sql")
    
    conn = sqlite3.connect(DB_NAME)
    results = pd.read_sql_query(sql, conn)
    conn.close()
    
    st.subheader("Results:")
    st.dataframe(results)