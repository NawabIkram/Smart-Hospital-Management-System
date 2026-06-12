"""
Generic CRUD functions for all EERD tables.

The SQL identifiers are not taken directly from user input. They come only from
entity_config.py, which works as a whitelist.
"""

from mysql.connector import Error
from db_connection import execute_select, execute_write


def quote_identifier(name):
    """
    Quote a MySQL table/column name using backticks.
    """
    return f"`{name}`"


def get_columns(config):
    return [field["name"] for field in config["fields"]]


def get_visible_columns(config):
    return [field["name"] for field in config["fields"]]


def get_list(config, search_text=None):
    table = quote_identifier(config["table"])
    columns = ", ".join(quote_identifier(col) for col in get_visible_columns(config))

    query = f"SELECT {columns} FROM {table}"
    params = []

    if search_text and config.get("search_fields"):
        conditions = []
        for field in config["search_fields"]:
            conditions.append(f"{quote_identifier(field)} LIKE %s")
            params.append(f"%{search_text}%")
        query += " WHERE " + " OR ".join(conditions)

    order_cols = ", ".join(quote_identifier(col) for col in config["pk"])
    query += f" ORDER BY {order_cols} DESC"
    return execute_select(query, tuple(params))


def get_one(config, pk_values):
    table = quote_identifier(config["table"])
    columns = ", ".join(quote_identifier(col) for col in get_visible_columns(config))
    where_clause = " AND ".join(f"{quote_identifier(pk)}=%s" for pk in config["pk"])
    params = tuple(pk_values[pk] for pk in config["pk"])
    query = f"SELECT {columns} FROM {table} WHERE {where_clause}"
    rows = execute_select(query, params)
    return rows[0] if rows else None


def clean_form_value(value):
    """
    Convert empty strings to None so nullable fields work correctly.
    """
    if value == "":
        return None
    return value


def collect_form_data(config, form, mode="add"):
    """
    Collect form data based on entity fields.

    For auto-increment IDs:
    - In add mode, auto field is skipped.
    - In edit mode, primary key is not updated.
    """
    data = {}

    for field in config["fields"]:
        name = field["name"]
        if mode == "add" and field.get("auto"):
            continue
        if mode == "edit" and name in config["pk"]:
            continue

        value = clean_form_value(form.get(name))
        data[name] = value

    return data


def validate_data(config, data):
    """
    Basic validation before sending data to MySQL.
    MySQL constraints still remain the final validation layer.
    """
    errors = []

    field_map = {field["name"]: field for field in config["fields"]}
    for name, value in data.items():
        field = field_map.get(name, {})
        label = field.get("label", name)

        if field.get("required") and (value is None or str(value).strip() == ""):
            errors.append(f"{label} is required.")

        if value not in (None, "") and field.get("type") == "number":
            try:
                number = float(value)
                if "min" in field and number < float(field["min"]):
                    errors.append(f"{label} must be at least {field['min']}.")
            except ValueError:
                errors.append(f"{label} must be a valid number.")

    return errors


def insert_record(config, data):
    errors = validate_data(config, data)
    if errors:
        return False, " ".join(errors)

    table = quote_identifier(config["table"])
    columns = list(data.keys())
    placeholders = ", ".join(["%s"] * len(columns))
    column_sql = ", ".join(quote_identifier(col) for col in columns)
    values = tuple(data[col] for col in columns)

    query = f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})"
    try:
        execute_write(query, values)
        return True, "Record added successfully."
    except Error as err:
        return False, friendly_db_error(err)
    except Exception as err:
        return False, str(err)


def update_record(config, pk_values, data):
    errors = validate_data(config, data)
    if errors:
        return False, " ".join(errors)

    table = quote_identifier(config["table"])
    set_clause = ", ".join(f"{quote_identifier(col)}=%s" for col in data.keys())
    where_clause = " AND ".join(f"{quote_identifier(pk)}=%s" for pk in config["pk"])
    values = tuple(data[col] for col in data.keys()) + tuple(pk_values[pk] for pk in config["pk"])

    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    try:
        execute_write(query, values)
        return True, "Record updated successfully."
    except Error as err:
        return False, friendly_db_error(err)
    except Exception as err:
        return False, str(err)


def delete_record(config, pk_values):
    table = quote_identifier(config["table"])
    where_clause = " AND ".join(f"{quote_identifier(pk)}=%s" for pk in config["pk"])
    values = tuple(pk_values[pk] for pk in config["pk"])

    query = f"DELETE FROM {table} WHERE {where_clause}"
    try:
        execute_write(query, values)
        return True, "Record deleted successfully."
    except Error as err:
        return False, friendly_db_error(err)
    except Exception as err:
        return False, str(err)


def friendly_db_error(err):
    """
    Convert common MySQL errors into beginner-friendly messages.
    """
    message = str(err)

    if getattr(err, "errno", None) == 1062:
        return "Duplicate value error. A record with this unique/primary key value already exists."
    if getattr(err, "errno", None) == 1451:
        return "Cannot delete this record because it is used by another table. Delete related records first."
    if getattr(err, "errno", None) == 1452:
        return "Invalid foreign key. Please select an existing related record."
    if getattr(err, "errno", None) == 1048:
        return "A required field was left empty."
    if getattr(err, "errno", None) == 1265:
        return "Invalid value for one of the selected fields."

    return f"Database error: {message}"
