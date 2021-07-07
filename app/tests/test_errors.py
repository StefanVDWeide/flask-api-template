import unittest
from app import create_app, db
from app.models import Users
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SECRET_KEY = "SQL-SECRET"
    JWT_SECRET_KEY = "JWT-SECRET"


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_400_error(self):
        with self.app.test_client() as c:
            # Make a post request to the register route without JSON data to trigger 400 error
            resp = c.post("/api/auth/register")

            json_data = resp.get_json()

            self.assertEqual(400, resp.status_code, msg=json_data)
            self.assertEqual({"_schema": ["Invalid input type."]}, json_data["msg"])

    def test_other_errors(self):
        with self.app.test_client() as c:
            # Make a post request to a nonexistent route to trigger 404 error
            resp = c.post("/api/auth/xxx")

            json_data = resp.get_json()

            self.assertEqual(404, resp.status_code, msg=json_data)


if __name__ == "__main__":
    unittest.main()
