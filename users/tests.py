from django.test import TestCase, Client
from users.models import User


class UsersTests(TestCase):
    username = 'Test_user@mail.com'
    password = 'Test_user_password'

    def test_login(self):
        client = Client()
        User.objects.create(email=self.username, password=self.password)
        resp = client.post('/users/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(resp.status_code, 200)

    def test_add_del(self):
        client = Client()
        resp = client.post('/users/registration/', {'email': self.username,
                                                    'password1': self.password,
                                                    'password2': self.password,
                                                    'full_name': 'New User Test',
                                                    'delivery_address': 'somewhere',
                                                    'role': 'customer'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)
