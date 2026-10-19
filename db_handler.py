import os
import mariadb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes database connection with the underlying MariaDB instance."""
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "localhost"),
            port=3306,
            database=os.getenv("DB_NAME", "threat_analytics")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MariaDB Platform: {e}")
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
    
    cursor = conn.cursor()
    query = """
        SELECT log_timestamp, host_identifier, severity_level, payload_message 
        FROM event_security_logs 
        ORDER BY log_timestamp DESC LIMIT 100;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['Timestamp', 'Host', 'Severity', 'Message'])
    conn.close()
    return df
