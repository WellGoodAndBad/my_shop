from my_shop.celery import app
from .utils import DataDowloader, create_pdf


@app.task
def parse_task():
    parser = DataDowloader()
    parser.parse()
    return 'done'


@app.task
def crt_pdf(user_id, item_shop_id):
    create_pdf(user_id, item_shop_id)
    return 'pdf created'
