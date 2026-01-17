import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.admin import blp as admin_blp
from .routes.health import blp as health_blp
from .routes.repairs import blp as repairs_blp

app = Flask(__name__)
app.url_map.strict_slashes = False


def _split_origins(value: str):
    """Split comma-separated origins into a clean list."""
    return [o.strip() for o in (value or "").split(",") if o.strip()]


def _build_allowed_origins() -> list[str]:
    """Build allowed origins list/patterns from env and safe dev defaults.

    Env vars supported:
      - CORS_ALLOWED_ORIGINS: comma-separated list of allowed origins/patterns.
        Examples:
          http://localhost:3000,https://localhost:3000
          https://*.beta01.cloud.kavia.ai:3000
      - FRONTEND_ORIGIN: legacy single origin value (still supported)

    Notes:
      - For local/dev we allow both http/https localhost:3000.
      - For preview environments, set CORS_ALLOWED_ORIGINS to the exact preview origin(s).
        If your preview host changes frequently and you understand the security tradeoff,
        you may use a wildcard subdomain pattern like: https://*.beta01.cloud.kavia.ai:3000
    """
    origins: list[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
    ]

    # Backward compatible single origin
    legacy = os.getenv("FRONTEND_ORIGIN", "").strip()
    if legacy:
        origins.append(legacy)

    # Preferred multi-origin env
    multi = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
    origins.extend(_split_origins(multi))

    # Also consider common platform-provided URLs if present (optional).
    # These are not guaranteed but harmless if unset.
    for name in ("SITE_URL", "REACT_APP_SITE_URL", "FRONTEND_URL"):
        v = os.getenv(name, "").strip()
        if v:
            origins.append(v)

    # de-duplicate while preserving order
    seen = set()
    deduped: list[str] = []
    for o in origins:
        if o not in seen:
            seen.add(o)
            deduped.append(o)
    return deduped


# CORS setup:
# Allow the React dev server (port 3000) / preview hosts to call the Flask backend (port 3001).
# We enable credentials so cookies/authorization can be used if needed.
allowed_origins = _build_allowed_origins()
CORS(
    app,
    resources={r"/api/*": {"origins": allowed_origins}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
)

# OpenAPI / Swagger settings
app.config["API_TITLE"] = "Mobile Web Service Repair Portal API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Register routes
api.register_blueprint(health_blp)
api.register_blueprint(repairs_blp)
api.register_blueprint(admin_blp)
