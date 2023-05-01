from flask import request, jsonify, Response

from app import db
from app.posts import bp
from app.models import Posts
from app.schemas import PostsSchema
from app.errors.handlers import bad_request

from flask_jwt_extended import jwt_required, current_user

from marshmallow import ValidationError

import asyncio
from aiohttp import ClientSession

# Declare database schemas so they can be returned as JSON objects
post_schema = PostsSchema()
posts_schema = PostsSchema(many=True)


@bp.get("get/user/posts")
@jwt_required()
def get_posts() -> tuple[Response, int]:
    """
    Returns all posts submitted by the user making the request

    Returns
    -------
    JSON
        A JSON object containing all post data
    """
    posts = current_user.posts.all()

    return posts_schema.jsonify(posts), 200


@bp.get("/get/user/post/<int:id>")
@jwt_required()
def get_post_by_id(id: int) -> tuple[Response, int] | Response:
    """
    Returns a specific post based on the ID in the URL

    Parameters
    ----------
    id : int
        The ID of the post

    Returns
    -------
    JSON
        A JSON object containing all post data
    """
    post = Posts.query.get(id)

    if not post:
        return bad_request("No post found")

    return post_schema.jsonify(post), 200


@bp.post("/post/user/submit/post")
@jwt_required()
def submit_post() -> tuple[Response, int] | Response:
    """
    Lets users retrieve a user profile when logged in

    Returns
    -------
    str
        A JSON object containing a success message
    """
    try:
        result = post_schema.load(request.json)
    except ValidationError as e:
        return bad_request(e.messages[0])

    post = Posts(body=result["body"], user=current_user)

    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "Post succesfully submitted"}), 201


@bp.delete("/delete/user/post/<int:id>")
@jwt_required()
def delete_post(id: int) -> tuple[Response, int] | Response:
    """
    Lets users retrieve a user profile when logged in

    Parameters
    ----------
    id : int
        The ID of the post to be deleted

    Returns
    -------
    str
        A JSON object containing the success message
    """
    post = Posts.query.get(id)

    if not post:
        return bad_request("Post not found")

    if post.user_id != current_user.id:
        return bad_request("Unauthorized")

    db.session.delete(post)
    db.session.commit()

    return jsonify({"msg": "Post succesfully deleted"}), 201


@bp.get("/get/user/posts/async")
@jwt_required()
async def async_posts_api_call() -> tuple[dict, int]:
    """
    Calls two endpoints from an external API as async demo

    Returns
    -------
    str
        A JSON object containing the posts
    """
    urls = [
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
    ]

    async with ClientSession() as session:
        tasks = (session.get(url) for url in urls)
        user_posts_res = await asyncio.gather(*tasks)
        json_res = [await r.json() for r in user_posts_res]

    response_data = {"posts": json_res}

    return response_data, 200
