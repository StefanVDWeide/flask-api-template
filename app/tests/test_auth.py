import unittest
from app import create_app, db
from app.models import Users
from config import Config

import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        u = Users(username="stefan")
        u.set_password("dog")
        self.assertFalse(u.check_password("cat"))
        self.assertTrue(u.check_password("dog"))

    def test_register(self):
        with self.app.test_client() as c:
            resp = c.post("/api/auth/register", json={"username": "test",
                                                      "password": "secret",
                                                      "first_name": "tim",
                                                      "last_name": "apple",
                                                      "email": "tim@test.com",
                                                      "birthday": "1990-01-01"})

            json_data = resp.get_json()
            self.assertEqual(201, resp.status_code, msg=json_data)
            self.assertEqual("Successfully registered", json_data["msg"])

    def test_login(self):
        with self.app.test_client() as c:
            c.post("/api/auth/register", json={"username": "test",
                                               "password": "secret",
                                               "first_name": "tim",
                                               "last_name": "apple",
                                               "email": "tim@test.com",
                                               "birthday": "1990-01-01"})

            resp = c.post("/api/auth/login", json={"username": "test",
                                                   "password": "secret"})
            json_data = resp.get_json()
            self.assertEqual(200, resp.status_code, msg=json_data)
            self.assertTrue(json_data["access_token"])
            self.assertTrue(json_data["refresh_token"])

    # def test_refresh(self):
    #     self.assertEqual(True, False)
    #
    # def test_fresh_login(self):
    #     self.assertEqual(True, False)
    #
    # def test_logout_access_token(self):
    #     self.assertEqual(True, False)
    #
    # def test_logout_refresh_token(self):
    #     self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
