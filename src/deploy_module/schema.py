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
    account_id = fields.Number(required=True)


class CleanUpSchema(Schema):
    """Clean Up Schema"""
    project_name = fields.Str(required=True)
    account_id = fields.Number(required=True)



class TaskStatusSchema(Schema):
    """Task Status Schema"""
    task_id= fields.Str(required=True)
