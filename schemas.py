from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)

class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
