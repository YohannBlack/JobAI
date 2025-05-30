import time

import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

st.set_page_config(page_title="Live Jobs Table", layout="wide")

# --- DB connection config ---
DB_USER = st.secrets.get("DB_USER")
DB_PASS = st.secrets.get("DB_PASS")
DB_HOST = st.secrets.get("DB_HOST")
DB_PORT = st.secrets.get("DB_PORT")
DB_NAME = st.secrets.get("DB_NAME")

REFRESH_INTERVAL = 2  # seconds

st.title("📋 Live Jobs Table Viewer")

placeholder = st.empty()


def get_jobs_data():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
        )
        if connection.is_connected():
            query = "SELECT * FROM jobs"
            df = pd.read_sql(query, connection)
            connection.close()
            return df
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


while True:
    with placeholder.container():
        df = get_jobs_data()
        if df is not None:
            st.dataframe(df, use_container_width=True)
    time.sleep(REFRESH_INTERVAL)
