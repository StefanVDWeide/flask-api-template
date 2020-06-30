import unittest
from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class TestMain(unittest.TestCase):
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
            c.post("/api/auth/register", json={"username": "test",
                                               "password": "secret",
                                               "first_name": "tim",
                                               "last_name": "apple",
                                               "email": "tim@test.com",
                                               "birthday": "1990-01-01"})

            setup_resp = c.post("/api/auth/login", json={"username": "test",
                                                         "password": "secret"})
            setup_resp_json = setup_resp.get_json()
            setup_access_token = setup_resp_json["access_token"]

            resp = c.get("/api/", headers={"Authorization": "Bearer {}".format(setup_access_token)})

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)

    def test_get_user(self):
        with self.app.test_client() as c:
            c.post("/api/auth/register", json={"username": "test",
                                               "password": "secret",
                                               "first_name": "tim",
                                               "last_name": "apple",
                                               "email": "tim@test.com",
                                               "birthday": "1990-01-01"})

            setup_resp = c.post("/api/auth/login", json={"username": "test",
                                                         "password": "secret"})
            setup_resp_json = setup_resp.get_json()
            setup_access_token = setup_resp_json["access_token"]

            resp = c.get("/api/user/test", headers={"Authorization": "Bearer {}".format(setup_access_token)})

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)


if __name__ == '__main__':
    unittest.main()
