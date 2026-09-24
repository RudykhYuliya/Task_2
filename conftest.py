import pytest

import helpers


@pytest.fixture
def user_payload():
    payload = helpers.generate_user()
    yield payload
    token = payload.get('accessToken')
    deleted = token and helpers.delete_user(token).status_code == 202
    if not deleted:
        response = helpers.login_user(payload['email'], payload['password'])
        if response.status_code == 200:
            helpers.delete_user(response.json()['accessToken'])


@pytest.fixture
def user(user_payload):
    response = helpers.register_user(user_payload)
    user_payload['accessToken'] = response.json()['accessToken']
    return user_payload


@pytest.fixture
def ingredients():
    return helpers.ingredient_ids()
