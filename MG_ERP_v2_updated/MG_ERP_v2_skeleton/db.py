"""Database helpers for MG ERP.

This module centralizes database access for the Flask application.  It
provides a ``get_db`` function that opens a connection to the database
configured on the current application and stores it on the application
context (``g``).  It also provides a ``close_db`` function which closes
the connection at the end of the request.

By keeping database logic here the rest of the application (including
blueprints) can import ``get_db`` without creating circular imports.
"""

from flask import current_app, g
import sqlite3


def get_db():
    """Return a database connection for the current request.

    A new connection is opened when first called in a request and
    reused for the remainder of that request.  The connection is
    configured to return rows as dictionaries (sqlite3.Row).
    """
    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        conn = sqlite3.connect(db_path)
        # return rows as dict-like objects
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(e=None):
    """Close the database connection if it was created for this request.

    This function is registered on the application teardown so it is
    automatically invoked at the end of each request, freeing
    resources.  The optional ``e`` parameter is ignored but included to
    satisfy Flask's teardown signature.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()