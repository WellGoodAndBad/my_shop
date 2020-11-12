import zipfile, io, requests, traceback
from .models import ItemShop, UserCart
from users.models import User
from django.conf import settings
from django.db import transaction
import pandas as pd
import pdfkit, os


class DataDowloader:

    user_agent = settings.USER_AGENT
    url = settings.BASE_URL

    def __init__(self):
        self.headers = {
            'user-agent': self.user_agent
        }

    def parse(self):
        try:
            content = self.get_data(self.url)
            zf = zipfile.ZipFile(io.BytesIO(content))
            df = pd.read_csv(zf.open('1f3af500435bef872af2b6f3cc8e79fc-9b6862442f3fc516bd78a6adc6b550a01f970462/goods.csv'), delimiter=';')
            with transaction.atomic():
                rows_for_ins = []
                for v in df.values:
                    article = v[0]
                    name = v[1]
                    price = v[2]
                    purchase_price = price * 0.9
                    if price < 1000:
                        shop_price = price * 1.2
                    else:
                        shop_price = price * 1.1

                    ItemShop.objects.filter(article=article).delete()
                    i_s = ItemShop(article=article, name_item=name, purchase_price=purchase_price, shop_price=shop_price)
                    rows_for_ins.append(i_s)

                ItemShop.objects.bulk_create(rows_for_ins)

        except:
            print(traceback.format_exc())

    def get_data(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 404:
                return
            if response.status_code != 200:
                raise ValueError('Request to {} responded with status {}'.format(url, response.status_code))
            else:
                return response.content
        except Exception:
            raise Exception('Error in getting html\n'+str(traceback.format_exc()))


def create_pdf(user_id, item_shop):

    user = User.objects.get(pk=user_id)
    user_cart = UserCart.objects.get(owner=user)

    body = f"""
        <html>
          <head>
            <meta charset="utf-8">
            <meta name="pdfkit-page-size" content="Legal"/>
            <meta name="pdfkit-orientation" content="Landscape"/>
          </head>
          %s
          </html>
        """

    # счет номер заказа в задаче ничего нет особенно, ормирую его из id
    str_for_pdf = f'''<p>Клиент: {user_cart.owner.full_name}</p>
                      <p>Номер заказа: {user_cart.id}{user_cart.owner.id}</p>
                      <p>Адрес доставки: {user_cart.owner.delivery_address}</p>'''

    if not os.path.exists('pdf_docs'):
        os.makedirs('pdf_docs')
    pdfkit.from_string(body % str_for_pdf, f'pdf_docs/{user_cart.id}.pdf')