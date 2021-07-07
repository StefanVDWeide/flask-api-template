import unittest

from flask import json
from app import create_app, db
from app.helpers.test_helpers import register_and_login_test_user
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "SQL-SECRET"
    JWT_SECRET_KEY = "JWT-SECRET"


class TestComments(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_comment(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            post_payload = {"body": "This is a test post"}

            resp = c.post(
                "/api/posts/post/user/submit/post",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=post_payload,
            )

            comment_payload = {"body": "This is a test comment", "post_id": 1}

            c.post(
                "/api/comments/post/user/submit/comment",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=comment_payload,
            )

            resp = c.get(
                "/api/comments/get/user/comments/post/1",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
            )

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)

    def test_submit_user_comment(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            post_payload = {"body": "This is a test post"}

            resp = c.post(
                "/api/posts/post/user/submit/post",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=post_payload,
            )

            payload = {"body": "This is a test comment", "post_id": 1}

            resp = c.post(
                "/api/comments/post/user/submit/comment",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            json_data = resp.get_json()

            self.assertEqual(201, resp.status_code, msg=json_data)

    def test_delete_user_comment(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            post_payload = {"body": "This is a test comment"}

            resp = c.post(
                "/api/posts/post/user/submit/post",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=post_payload,
            )

            payload = {"body": "This is a test comment", "post_id": 1}

            resp = c.post(
                "/api/comments/post/user/submit/comment",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
                json=payload,
            )

            resp = c.delete(
                "/api/comments/delete/user/comment/1",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
            )

            json_data = resp.get_json()

            self.assertEqual(201, resp.status_code, msg=json_data)

    def test_get_user_comments_async(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            resp = c.get(
                "/api/comments/get/user/comments/async",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
            )

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)


if __name__ == "__main__":
    unittest.main()
