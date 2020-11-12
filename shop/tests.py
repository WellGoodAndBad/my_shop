from django.test import TestCase, Client
from users.models import User
from shop.models import UserCart, ItemShop


class ShopTests(TestCase):
    username = 'Test_user@mail.com'
    password = 'Test_user_password'

    def test_main_page(self):
        client = Client()
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_my_cart(self):
        client = Client()
        usr = User.objects.create(email=self.username, password=self.password)
        client.force_login(user=usr)
        resp = client.get(f'/mycart/{usr.id}/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_add_del(self):
        client = Client()
        usr = User.objects.create(email=self.username, password=self.password)
        item = ItemShop.objects.create(article=12,
                                       name_item='DjangoPython',
                                       purchase_price=1100,
                                       shop_price=1001)
        client.force_login(user=usr)
        client.get(f'/add-to-cart/{usr.id}/{item.id}/', follow=True)
        cart = UserCart.objects.get(owner=usr)
        self.assertEqual(len(cart.items.all()), 1)
        client.get(f'/delete-from-cart/{usr.id}/{item.id}/', follow=True)
        self.assertEqual(len(cart.items.all()), 0)

    def test_all_carts(self):
        client = Client()
        usr = User.objects.create(email=self.username, password=self.password)
        client.force_login(user=usr)
        resp = client.get('/all-carts/', follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_all_carts_manager(self):
        client = Client()
        usr = User.objects.create(email=self.username,
                                  password=self.password,
                                  role='manager')
        client.force_login(user=usr)
        resp = client.get('/all-carts/', follow=True)
        self.assertEqual(resp.status_code, 200)