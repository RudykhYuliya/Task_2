import allure
import pytest

import helpers


class TestLoginUser:
    @allure.title('Можно авторизоваться под существующим пользователем')
    def test_login_existing_user(self, user):
        response = helpers.login_user(user['email'], user['password'])
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert body['user']['email'] == user['email']
        assert body['user']['name'] == user['name']
        assert body['accessToken'].startswith('Bearer ')
        assert body['refreshToken']

    @allure.title('Нельзя авторизоваться с неверным логином и паролем')
    @pytest.mark.parametrize('wrong_email, wrong_password', [
        (True, False),
        (False, True),
    ])
    def test_login_with_wrong_credentials(self, user, wrong_email, wrong_password):
        email = 'nobody@yandex.ru' if wrong_email else user['email']
        password = 'wrong-password' if wrong_password else user['password']
        response = helpers.login_user(email, password)
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}
