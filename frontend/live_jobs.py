import time

import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from mysql.connector import Error
import os

load_dotenv()

st.set_page_config(page_title="Live Jobs Table", layout="wide")

REFRESH_INTERVAL = 2  # seconds

st.title("📋 Live Jobs Table Viewer")

placeholder = st.empty()


def get_jobs_data():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=os.environ.get("DB_PORT", 3306)
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
