import allure

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

    @allure.title('Нельзя авторизоваться с неверным логином')
    def test_login_with_wrong_email(self, user):
        response = helpers.login_user('nobody@yandex.ru', user['password'])
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}

    @allure.title('Нельзя авторизоваться с неверным паролем')
    def test_login_with_wrong_password(self, user):
        response = helpers.login_user(user['email'], 'wrong-password')
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}
