"""
Configuration for Smart Hospital Management System.

Default values are for XAMPP on a local machine:
- host: localhost
- user: root
- password: empty
- database: smart_hospital_db

You can override these using environment variables:
DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
"""

import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "smart_hospital_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}
