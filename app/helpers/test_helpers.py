def register_and_login_test_user(c) -> str:
    """
    Helper function that makes an HTTP request to register a test user

    Parameters
    ----------
    c : object
        Test client object

    Returns
    -------
    str
        Access JWT in order to use in subsequent tests
    """
    c.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "secret",
            "first_name": "tim",
            "last_name": "apple",
            "email": "tim@test.com",
            "birthday": "1990-01-01",
        },
    )

    setup_resp = c.post(
        "/api/auth/login", json={"username": "test", "password": "secret"}
    )
    setup_resp_json = setup_resp.get_json()
    setup_access_token = setup_resp_json["access_token"]

    return setup_access_token
