## test_shop

pip install -r install requirements.txt

Debian/Ubuntu:
    sudo apt-get install wkhtmltopdf
    
Так же используются postgresql(for db), redis(for celery).

## сбор данных
поднять воркер для задач: "celery -A my_shop worker -l info"

кнопка "GET DATA" запускает сбо данных из удаленного источника.

## pdf 
на странице mycart/id_user/, кнопка "print docs" запускает формирование пдф документ и складывает в папку "pdf_docs".
(так как в задаче насчет номера заказа ничего не указанно, формирую его просто из ид-шников).