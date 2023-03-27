# Yatube REST API

### Описание

REST API для проекта Yatube: https://github.com/AndrewYatskevich/yatube

### Технологии

Python 3.7
Django 2.2.19
Django REST framework 3.12.4

### Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndrewYatskevich/api_final_yatube.git
```

```
cd api_final_yatube
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python3 manage.py migrate
```

- Запустить проект:

```
python3 manage.py runserver
```

Автор: Андрей Яцкевич https://github.com/AndrewYatskevich