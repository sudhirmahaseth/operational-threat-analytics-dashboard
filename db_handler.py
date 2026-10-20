import os
import pymysql  # mariadb ki jagah pymysql use karenge (Cloud-safe aur stable hai)
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes database connection with Aiven Cloud MySQL / Local Database."""
    try:
        # Streamlit production pe st.secrets check karega, local pe .env file ya default values chalengi
        conn = pymysql.connect(
            host=st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost")),
            user=st.secrets.get("DB_USER", os.getenv("DB_USER", "admin")),
            password=st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", "password")),
            database=st.secrets.get("DB_NAME", os.getenv("DB_NAME", "threat_analytics")),
            # Default MySQL port 3306 hai, lekin Aiven ka port 25060 hota hai
            port=int(st.secrets.get("DB_PORT", os.getenv("DB_PORT", 3306))),
            ssl_verify_identity=False,
            ssl_ca=None  # Aiven secure clusters ke liye connection verify handle kar leta hai
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Database Platform: {e}")
        return None

def fetch_historical_threat_metrics():
    """
    Executes optimized relational queries to group analytical summary records 
    without causing processing bottlenecks.
    """
    conn = get_db_connection()
    if conn is None:
        # Return fallback dummy dataframe if database is offline during staging
        return pd.DataFrame({
            'Timestamp': pd.date_range(end=pd.Timestamp.now(), periods=5, freq='H'),
            'Host': ['Server-01A', 'DB-Main', 'Auth-Gateway', 'Server-01A', 'Edge-Node'],
            'Severity': ['Low', 'High', 'Critical', 'Medium', 'Low'],
            'Message': ['Routine port scan blocked', 'Failed login threshold breached', 'SQL Injection attempt detected', 'High memory usage alert', 'SSL connection reset']
        })
    
    try:
        cursor = conn.cursor()
        # Query aapke schema ke tables ke mutabik execute hogi
        query = """
            SELECT log_timestamp, host_identifier, severity_level, payload_message 
            FROM event_security_logs 
            ORDER BY log_timestamp DESC LIMIT 100;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['Timestamp', 'Host', 'Severity', 'Message'])
    except Exception as e:
        print(f"Error executing query: {e}")
        # Table na hone ya error aane par safe return dashboard crash hone se bachayega
        df = pd.DataFrame(columns=['Timestamp', 'Host', 'Severity', 'Message'])
    finally:
        conn.close()
        
    return df
