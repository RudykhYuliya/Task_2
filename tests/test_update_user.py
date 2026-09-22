import allure
import pytest

import helpers


class TestUpdateUser:
    @allure.title('Можно изменить данные авторизованного пользователя')
    @pytest.mark.parametrize('field', ['email', 'name', 'password'])
    def test_update_authorized_user(self, user, field):
        if field == 'email':
            value = helpers.generate_user()['email']
        elif field == 'name':
            value = 'Julia New'
        else:
            value = 'newpassword'
        response = helpers.update_user({field: value}, user['accessToken'])
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        if field == 'password':
            login = helpers.login_user(user['email'], value)
            assert login.status_code == 200
            user['password'] = value
        else:
            assert body['user'][field] == value
            user[field] = value

    @allure.title('Нельзя изменить данные пользователя без авторизации')
    def test_update_user_without_authorization(self):
        response = helpers.update_user({'name': 'Julia New'})
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'You should be authorised'}
