"""Application factory for MG ERP.

This module defines the :func:`create_app` function used to configure
and create the Flask application.  It configures the secret key and
database location from environment variables, integrates CSRF
protection, registers teardown handlers, and registers the
application's blueprints.  Running this file directly will start a
development server.
"""

import os

from flask import Flask
try:
    # Prefer Flask-WTF for CSRF protection if available.  It injects a CSRF
    # token into WTForms and verifies it on submission.  If the package
    # is unavailable (for example in offline environments), fall back to
    # a no-op implementation that logs a warning.
    from flask_wtf.csrf import CSRFProtect  # type: ignore
except ImportError:  # pragma: no cover
    class CSRFProtect:  # type: ignore
        """Fallback no-op CSRF protection.

        When Flask-WTF is not installed, this class provides an
        interface-compatible object that simply logs a warning when
        initialised.  This avoids breaking the application in
        restricted environments while signalling that CSRF protection
        is disabled.
        """

        def init_app(self, app):
            # Delay import to avoid creating a circular import for app.logger
            import logging

            logger = getattr(app, "logger", logging.getLogger(__name__))
            logger.warning(
                "Flask-WTF not installed; CSRF protection is disabled."
            )
            return self

from .db import close_db


def create_app() -> Flask:
    """Create and configure an instance of the MG ERP Flask application.

    :returns: The configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=False)
    # Configure secret key and database path from environment variables
    # Provide sensible defaults for development when variables are absent
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        # Use DB_PATH env var if provided, else default to erp.db in this directory
        DATABASE=os.environ.get(
            "DB_PATH",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "erp.db"),
        ),
    )

    # Initialize CSRF protection; it protects WTForms by injecting a
    # hidden token into rendered forms and verifying it on POST
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Register database teardown so connections are cleaned up
    app.teardown_appcontext(close_db)

    # Register application blueprints
    from .blueprints.main import bp as main_bp  # imported here to avoid circular imports
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    # Only run a development server if this module is executed directly.
    # Use 127.0.0.1 rather than 0.0.0.0 for local-only access; enable debug for auto reload.
    _app = create_app()
    _app.run(host="127.0.0.1", port=5000, debug=True)