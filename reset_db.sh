mysql -u root -p -e "DROP DATABASE socmovdb; CREATE DATABASE IF NOT EXISTS socmovdb;"
python manage.py syncdb
