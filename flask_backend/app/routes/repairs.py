from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..auth import require_admin_token
from ..schemas import RepairCreateSchema, RepairSchema
from ..supabase_client import get_supabase_client

blp = Blueprint(
    "Repairs",
    "repairs",
    url_prefix="/api/repairs",
    description="Repair request submission and admin listing",
)


def _supabase_table():
    """Internal helper to return the Supabase table client."""
    client = get_supabase_client()
    return client.table("repairs")


@blp.route("")
class RepairsCollection(MethodView):
    """Repairs collection.

    POST: Create a new repair request (public).
    GET: List repair requests (admin only).
    """

    @blp.arguments(RepairCreateSchema)
    @blp.response(201, RepairSchema)
    def post(self, payload):
        # Insert into Supabase `repairs` table. The table should have columns:
        # name, phone, email, device_type, issue_description, preferred_contact_method, created_at (optional default).
        try:
            res = _supabase_table().insert(payload).execute()
        except Exception as e:
            abort(500, message=f"Failed to submit repair request: {str(e)}")

        data = getattr(res, "data", None) or []
        if not data:
            abort(500, message="Repair request was not saved.")
        return data[0]

    @blp.response(200, RepairSchema(many=True))
    def get(self):
        ok, _username = require_admin_token()
        if not ok:
            abort(401, message="Missing or invalid admin token.")

        try:
            # Order newest first if created_at exists.
            res = _supabase_table().select("*").order("created_at", desc=True).execute()
        except Exception as e:
            abort(500, message=f"Failed to load repairs: {str(e)}")

        return getattr(res, "data", None) or []
