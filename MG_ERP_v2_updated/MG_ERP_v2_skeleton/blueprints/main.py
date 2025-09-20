"""Main application routes for MG ERP.

This blueprint contains the core pages for the ERP, such as the
landing page and the dashboard.  By registering this blueprint in
``create_app``, the routes become part of the application without
cluttering the application factory itself.  Routes here use the
database helper from ``db.py`` to retrieve data.
"""

from flask import Blueprint, render_template
import sqlite3

from db import get_db


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Render the homepage.

    The base template provides a simple landing page.  As the
    application grows, this can be extended or populated with
    additional data.
    """
    return render_template("base.html")


@bp.route("/dashboard")
def dashboard():
    """Render the dashboard view.

    This example executes a placeholder query against the database.  If
    the underlying tables are missing, it safely returns an empty
    result list so the template can handle it gracefully.  Once
    additional tables and data are added to the ERP, this query can
    be updated to show real information (e.g. top products by
    profitability).
    """
    db = get_db()
    # Use a try/except in case the expected table is missing during early development
    try:
        rows = db.execute(
            """
            SELECT 'Example Product' as nome, 0 as lucro_liquido
            """
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    return render_template("dashboard.html", rows=rows)