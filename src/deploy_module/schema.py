""""INPUT SCHEMAS"""

from marshmallow import Schema, fields


class DeploySchema(Schema):
    """Deploy Schema"""
    app_type = fields.Str(
        required=True, validate=lambda x: x in ['flask', 'node'])
    git = fields.Str(required=True)
    env = fields.Dict()
    port = fields.Number(required=True)
    project_name = fields.Str(required=True)
