from app import ma
from app.models import Users, Posts, Comments, Tasks

from marshmallow import Schema, fields


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class UsersDeserializingSchema(Schema):
    username = fields.String()
    password = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    birthday = fields.Date()


class PostsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Posts


class PostsDeserializingSchema(Schema):
    body = fields.String()


class CommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments


class CommentsDeserializingSchema(Schema):
    body = fields.String()
    post_id = fields.Integer()


class TasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks
