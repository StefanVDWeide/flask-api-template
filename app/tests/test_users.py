import unittest
from app import create_app, db
from app.helpers.test_helpers import register_and_login_test_user
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "SQL-SECRET"
    JWT_SECRET_KEY = "JWT-SECRET"


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_page(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            resp = c.get(
                "/api/users/get/user/profile",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
            )

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)

    def test_get_user(self):
        with self.app.test_client() as c:
            setup_access_token = register_and_login_test_user(c)

            resp = c.get(
                "/api/users/get/user/profile/test",
                headers={"Authorization": "Bearer {}".format(setup_access_token)},
            )

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)


if __name__ == "__main__":
    unittest.main()
