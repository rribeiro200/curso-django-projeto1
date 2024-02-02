import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        # Criando um novo usuário fictício para este teste
        string_password = 'pass'
        user = User.objects.create_user(username='username', password=string_password)

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Obtendo formulário e campos
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Logando o usuário
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        
        # Submetendo o form
        form.submit()

        # Pegando texto de login feito com sucesso na página
        body = self.browser.find_element(By.TAG_NAME, 'body').text

        # Fim do teste
        self.assertIn('Login successfully!', body)

    def test_login_create_raises_404_if_not_POST_method(self):
        url = self.browser.get(self.live_server_url + reverse('authors:login_create'))

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Not found', body)