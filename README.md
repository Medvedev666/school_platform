# Установка

Python v3.12.2

Создайте виртуальное окружение
```
python -m venv venv
```

Установите зависимости
```
pip install -r requirements.txt
```

Добавьте миграции
```
python manage.py makemigrations
python manage.py migrate
```

Создайте администратора
```
python manage.py createsuperuser
```

Запустите сервер
```
python manage.py runserver
```
Первым делом, создайте пользовательские группы/классы в панели администратора
После этого можно можно создавать профили для преподавателей и студентов


TG: @Bearmed6