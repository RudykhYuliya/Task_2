import allure
import pytest

import helpers


class TestCreateUser:
    @allure.title('Можно создать уникального пользователя')
    def test_create_unique_user(self, user_payload):
        response = helpers.register_user(user_payload)
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert body['user']['email'] == user_payload['email']
        assert body['user']['name'] == user_payload['name']
        assert body['accessToken'].startswith('Bearer ')
        assert body['refreshToken']

    @allure.title('Нельзя создать пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, user):
        payload = {
            'email': user['email'],
            'password': user['password'],
            'name': user['name'],
        }
        response = helpers.register_user(payload)
        assert response.status_code == 403
        assert response.json() == {'success': False, 'message': 'User already exists'}

    @allure.title('Нельзя создать пользователя без обязательного поля')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_without_required_field(self, user_payload, field):
        payload = user_payload.copy()
        payload.pop(field)
        response = helpers.register_user(payload)
        assert response.status_code == 403
        assert response.json() == {
            'success': False,
            'message': 'Email, password and name are required fields',
        }
