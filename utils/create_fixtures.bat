cd ..
python manage.py dumpdata catalog --indent=2 > webshop/catalog/fixtures/initial_data.json
python manage.py dumpdata accounts --indent=2 > webshop/accounts/fixtures/initial_data.json
python manage.py dumpdata cart --indent=2 > webshop/cart/fixtures/initial_data.json
python manage.py dumpdata checkout --indent=2 > webshop/checkout/fixtures/initial_data.json
python manage.py dumpdata news --indent=2 > webshop/news/fixtures/initial_data.json
python manage.py dumpdata search --indent=2 > webshop/search/fixtures/initial_data.json
PAUSE