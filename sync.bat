cd webshop

del /S *.pyc
cd ..


python manage.py syncdb

PAUSE