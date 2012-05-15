cd ..
echo "WARNING!!! All sql create data will be overwriten"
python manage.py sqlall catalog > webshop/create_db.sql
python manage.py sqlall accounts >> webshop/create_db.sql
python manage.py sqlall cart >> webshop/create_db.sql
python manage.py sqlall checkout >> webshop/create_db.sql
python manage.py sqlall news >> webshop/create_db.sql
python manage.py sqlall search >> webshop/create_db.sql
PAUSE