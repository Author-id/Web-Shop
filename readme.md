'''bash
python -m venv venv
sudo venv/bin/activate
pip install -r requirements/prod.txt
source .env
python manage.py runserver
