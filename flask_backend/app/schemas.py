from marshmallow import Schema, fields, validate


class RepairCreateSchema(Schema):
    """Schema for creating a repair request."""

    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    phone = fields.Str(required=True, validate=validate.Length(min=5, max=40))
    email = fields.Email(required=False, allow_none=True)
    device_type = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    issue_description = fields.Str(required=True, validate=validate.Length(min=5, max=4000))
    preferred_contact_method = fields.Str(
        required=False, allow_none=True, validate=validate.OneOf(["phone", "email", "sms"])
    )


class RepairSchema(RepairCreateSchema):
    """Schema representing a repair request (as stored)."""

    id = fields.Raw(required=False)  # Supabase may return int/uuid depending on table
    created_at = fields.Str(required=False)


class AdminLoginSchema(Schema):
    """Schema for admin login payload."""

    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=200))


class AdminLoginResponseSchema(Schema):
    """Schema for admin login response."""

    token = fields.Str(required=True)
    token_type = fields.Str(required=True)
