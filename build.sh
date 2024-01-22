set -o errexit
sudo apt-get install libpq-dev python-dev
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser --no-input