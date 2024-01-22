set -o errexit
pip install -r requirements.txt
sudo apt-get install libpq-dev
pip install psycopg2==2.9.9
python manage.py collectstatic --noinput
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser --no-input