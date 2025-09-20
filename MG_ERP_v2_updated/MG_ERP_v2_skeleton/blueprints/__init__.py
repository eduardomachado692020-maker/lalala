"""Blueprint package for MG ERP routes.

This file marks the directory as a Python package.  Blueprints are
registered in :func:`~app.create_app` via :func:`~flask.Blueprint.register`.
Additional blueprints can be added by creating modules in this package
and registering them in ``create_app()``.
"""

__all__ = ["main"]