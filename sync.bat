cd webshop
del /S *.pyc
python manage.py syncdb
cd ..
PAUSE