"""
Smart Hospital Management System 

Run:
    python main.py

Then open:
    http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from mysql.connector import Error

from db_connection import execute_select, test_connection
from models.entity_config import ENTITIES, get_entity, get_navigation_entities
from models.crud import (
    get_list,
    get_one,
    collect_form_data,
    insert_record,
    update_record,
    delete_record,
)
from models.reports import REPORTS, dashboard_counts
from models.db_views import load_database_views


app = Flask(__name__)
app.secret_key = "smart-hospital-phase2-secret-key"


@app.context_processor
def inject_navigation():
    return {"entities": get_navigation_entities()}


def get_pk_values(config):
    """
    Read primary key values from URL query parameters or submitted form.
    Supports both single-column and composite primary keys.
    """
    values = {}
    for pk in config["pk"]:
        value = request.values.get(pk)
        if value is None:
            abort(400, description=f"Missing primary key field: {pk}")
        values[pk] = value
    return values


def build_pk_query(row, config):
    """
    Build dictionary used by url_for(..., **pk_query).
    """
    return {pk: row[pk] for pk in config["pk"]}


def load_dynamic_options(field):
    """
    Load dropdown options from a query when a field has options_query.
    Static options are also supported.
    """
    if "options" in field:
        return [{"value": option, "label": option} for option in field["options"]]

    if "options_query" in field:
        try:
            return execute_select(field["options_query"])
        except Exception:
            return []

    return []


@app.route("/")
def dashboard():
    db_status = False
    counts = []
    error_message = None

    try:
        db_status = test_connection()
        counts = dashboard_counts()
    except Exception as err:
        error_message = str(err)

    return render_template(
        "dashboard.html",
        db_status=db_status,
        counts=counts,
        error_message=error_message,
    )


@app.route("/entity/<entity_key>")
def entity_list(entity_key):
    config = get_entity(entity_key)
    if not config:
        abort(404)

    search_text = request.args.get("q", "").strip()
    rows = get_list(config, search_text)

    return render_template(
        "list.html",
        entity_key=entity_key,
        config=config,
        rows=rows,
        search_text=search_text,
        build_pk_query=build_pk_query,
    )


@app.route("/entity/<entity_key>/add", methods=["GET", "POST"])
def entity_add(entity_key):
    config = get_entity(entity_key)
    if not config:
        abort(404)

    if request.method == "POST":
        data = collect_form_data(config, request.form, mode="add")
        success, message = insert_record(config, data)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("entity_list", entity_key=entity_key))

    options = {field["name"]: load_dynamic_options(field) for field in config["fields"]}
    return render_template(
        "form.html",
        entity_key=entity_key,
        config=config,
        row={},
        options=options,
        mode="add",
    )


@app.route("/entity/<entity_key>/edit", methods=["GET", "POST"])
def entity_edit(entity_key):
    config = get_entity(entity_key)
    if not config:
        abort(404)

    pk_values = get_pk_values(config)
    row = get_one(config, pk_values)
    if not row:
        flash("Record not found.", "danger")
        return redirect(url_for("entity_list", entity_key=entity_key))

    if request.method == "POST":
        data = collect_form_data(config, request.form, mode="edit")
        success, message = update_record(config, pk_values, data)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("entity_list", entity_key=entity_key))
        row.update(data)

    options = {field["name"]: load_dynamic_options(field) for field in config["fields"]}
    return render_template(
        "form.html",
        entity_key=entity_key,
        config=config,
        row=row,
        options=options,
        mode="edit",
    )


@app.route("/entity/<entity_key>/delete", methods=["POST"])
def entity_delete(entity_key):
    config = get_entity(entity_key)
    if not config:
        abort(404)

    pk_values = get_pk_values(config)
    success, message = delete_record(config, pk_values)
    flash(message, "success" if success else "danger")
    return redirect(url_for("entity_list", entity_key=entity_key))


@app.route("/reports")
def reports():
    report_data = []
    for report_key, report_info in REPORTS.items():
        try:
            rows = report_info["function"]()
            columns = list(rows[0].keys()) if rows else []
            report_data.append({
                "key": report_key,
                "title": report_info["title"],
                "description": report_info["description"],
                "columns": columns,
                "rows": rows,
                "error": None,
            })
        except Error as err:
            report_data.append({
                "key": report_key,
                "title": report_info["title"],
                "description": report_info["description"],
                "columns": [],
                "rows": [],
                "error": str(err),
            })

    return render_template("reports.html", report_data=report_data)


@app.route("/views")
def database_views():
    view_data = []
    error_message = None

    try:
        view_data = load_database_views()
    except Error as err:
        error_message = str(err)

    return render_template("views.html", view_data=view_data, error_message=error_message)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", title="404 Not Found", message="The requested page was not found."), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", title="400 Bad Request", message=str(error)), 400


if __name__ == "__main__":
    app.run(debug=True)
