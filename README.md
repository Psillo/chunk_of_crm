Запуск (миграции пересоздавать не советую))))):
```
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata data.json
python3 manage.py runserver
```
API по адресу http://127.0.0.1:8000/api/
