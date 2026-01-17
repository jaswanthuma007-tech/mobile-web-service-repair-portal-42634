import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.repairs import blp as repairs_blp
from .routes.admin import blp as admin_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS setup:
# Allow the React dev server (port 3000) to call the Flask backend (port 3001).
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
CORS(
    app,
    resources={r"/api/*": {"origins": [frontend_origin]}},
    supports_credentials=False,
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
