from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..auth import issue_admin_token, validate_admin_credentials
from ..schemas import AdminLoginResponseSchema, AdminLoginSchema

blp = Blueprint(
    "Admin",
    "admin",
    url_prefix="/api/admin",
    description="Admin authentication endpoints",
)


@blp.route("/login")
class AdminLogin(MethodView):
    """Admin login endpoint.

    Validates username/password against environment variables and returns a bearer token.
    """

    @blp.arguments(AdminLoginSchema)
    @blp.response(200, AdminLoginResponseSchema)
    def post(self, payload):
        username = payload["username"]
        password = payload["password"]

        if not validate_admin_credentials(username, password):
            abort(401, message="Invalid admin credentials.")

        token = issue_admin_token(username)
        return {"token": token, "token_type": "Bearer"}
