import allure

import helpers


class TestUpdateUser:
    @allure.title('Можно изменить email авторизованного пользователя')
    def test_update_authorized_user_email(self, user):
        new_email = helpers.generate_user()['email']
        response = helpers.update_user({'email': new_email}, user['accessToken'])
        user['email'] = new_email
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert body['user']['email'] == new_email

    @allure.title('Можно изменить имя авторизованного пользователя')
    def test_update_authorized_user_name(self, user):
        response = helpers.update_user({'name': 'Julia New'}, user['accessToken'])
        user['name'] = 'Julia New'
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert body['user']['name'] == 'Julia New'

    @allure.title('Можно изменить пароль авторизованного пользователя')
    def test_update_authorized_user_password(self, user):
        response = helpers.update_user({'password': 'newpassword'}, user['accessToken'])
        user['password'] = 'newpassword'
        login = helpers.login_user(user['email'], user['password'])
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert login.status_code == 200

    @allure.title('Нельзя изменить данные пользователя без авторизации')
    def test_update_user_without_authorization():
        response = helpers.update_user({'name': 'Julia New'})
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'You should be authorised'}
