import os
import pymysql
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes database connection with Aiven Cloud MySQL / Local Database."""
    try:
        conn = pymysql.connect(
            host=st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost")),
            user=st.secrets.get("DB_USER", os.getenv("DB_USER", "admin")),
            password=st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", "password")),
            database=st.secrets.get("DB_NAME", os.getenv("DB_NAME", "defaultdb")), # Aiven defaultdb map kiya
            port=int(st.secrets.get("DB_PORT", os.getenv("DB_PORT", 16852))),
            ssl_verify_identity=False,
            ssl_ca=None
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Database Platform: {e}")
        return None

def initialize_table_if_not_exists():
    """Automatically creates the required event logs table if it is missing in Aiven."""
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Agar table nahi bani hai, toh system ise khud generate kar lega
            create_table_query = """
                CREATE TABLE IF NOT EXISTS event_security_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    host_identifier VARCHAR(100),
                    severity_level VARCHAR(50),
                    payload_message TEXT
                );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print("Database table checked/created successfully!")
        except Exception as e:
            print(f"Auto-initialization error: {e}")
        finally:
            conn.close()

# App load hote hi sabse pehle table setup triggers confirm karna
initialize_table_if_not_exists()

def fetch_historical_threat_metrics():
    """Executes relational queries to fetch latest logs from the auto-created table."""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame({
            'Timestamp': pd.date_range(end=pd.Timestamp.now(), periods=5, freq='H'),
            'Host': ['Server-01A', 'DB-Main', 'Auth-Gateway', 'Server-01A', 'Edge-Node'],
            'Severity': ['Low', 'High', 'Critical', 'Medium', 'Low'],
            'Message': ['Routine port scan blocked', 'Failed login threshold breached', 'SQL Injection attempt detected', 'High memory usage alert', 'SSL connection reset']
        })
    
    try:
        cursor = conn.cursor()
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
        df = pd.DataFrame(columns=['Timestamp', 'Host', 'Severity', 'Message'])
    finally:
        conn.close()
        
    return df
    
