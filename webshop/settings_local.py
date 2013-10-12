# File for storing custom settings
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'webshop',
		'TEST_NAME': 'webshop_unit_test_db',
		'USER': 'dbuser',
		'PASSWORD': '12345678',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}
