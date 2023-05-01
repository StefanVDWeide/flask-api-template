from typing import Any
from flask import request, jsonify, Response

from app import db
from app.comments import bp
from app.models import Comments, Posts
from app.schemas import CommentsSchema, CommentsDeserializingSchema
from app.errors.handlers import bad_request

from flask_jwt_extended import jwt_required, current_user

from marshmallow import ValidationError

import asyncio
from aiohttp import ClientSession

comment_schema = CommentsSchema()
comments_schema = CommentsSchema(many=True)
comment_deserializing_schema = CommentsDeserializingSchema()


@bp.get("/get/user/comments/post/<int:id>")
@jwt_required()
def get_comments_by_post_id(id: int) -> Response:
    """
    Endpoint for retrieving the user comments associated with a particular post

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing the comments
    """
    comments = Comments.query.filter_by(post_id=id).all()
    return comments_schema.jsonify(comments)


@bp.post("/post/user/submit/comment")
@jwt_required()
def submit_comment() -> tuple[Response, int] | Response:
    """
    Lets users submit a comment regarding a post

    Returns
    -------
    str
        A JSON object containing a success message
    """
    try:
        result = comment_deserializing_schema.load(request.get_json())
    except ValidationError as e:
        return bad_request(e.messages)

    post = Posts.query.get(result["post_id"])

    if not post:
        return bad_request("Post not found")

    if post.user_id != current_user.id:
        return bad_request("Unauthorized")

    comment = Comments(body=result["body"], post=post, user=current_user)

    db.session.add(comment)
    db.session.commit()

    return jsonify({"msg": "Comment succesfully submitted"}), 201


@bp.delete("/delete/user/comment/<int:id>")
@jwt_required()
def delete_comment(id: int) -> tuple[Response, int] | Response:
    """
    Lets users delete one of their own comments

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing a success message
    """
    comment = Comments.query.get(id)

    if not comment:
        return bad_request("Comment not found")

    if comment.user_id != current_user.id:
        return bad_request("Unauthorized")

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"msg": "Comment succesfully deleted"}), 201


@bp.get("/get/user/comments/async")
@jwt_required()
async def async_comments_api_call() -> dict[str, list[Any]]:
    """
    Calls two endpoints from an external API as async demo

    Returns
    -------
    str
        A JSON object containing the comment
    """
    urls = [
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/comments",
    ]

    async with ClientSession() as session:
        tasks = (session.get(url) for url in urls)
        user_posts_res = await asyncio.gather(*tasks)
        json_res = [await r.json() for r in user_posts_res]

    response_data = {"comments": json_res}

    return response_data
