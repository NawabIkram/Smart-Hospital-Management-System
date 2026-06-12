"""
Database connection helper.

Install dependency:
    pip install mysql-connector-python
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """
    Create and return a new MySQL connection.

    A new connection is opened per request/action because this is simpler and safer
    for a beginner Flask project.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as err:
        raise RuntimeError(f"Database connection failed: {err}") from err


def test_connection():
    """
    Check whether Flask can connect to MySQL.
    """
    conn = get_connection()
    try:
        return conn.is_connected()
    finally:
        conn.close()


def execute_select(query, params=None):
    """
    Execute SELECT query and return rows as dictionaries.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def execute_write(query, params=None):
    """
    Execute INSERT/UPDATE/DELETE query and commit changes.
    Returns the last inserted ID if available.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
