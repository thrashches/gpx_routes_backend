
## GPX Project

---

### Структура проекта
```
.
├── Makefile
├── README.md
├── deploy
│   ├── docker-compose.base.yml # Базовый docker-compose для сборки
│   ├── docker-compose.local.yml # Сборка и запуск приложения в локальном окружении 
│   └── env_file # Переменные для docker-compose service: server-local и database
└── gpx_dev
    ├── Dockerfile
    ├── api
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   └── v1
    │       ├── __init__.py
    │       ├── serializers
    │       │   ├── __init__.py
    │       │   └── user_serializers.py
    │       ├── test_api
    │       │   ├── __init__.py
    │       │   └── test_user_api.py
    │       ├── urls.py
    │       └── views
    │           ├── __init__.py
    │           └── user_views.py
    ├── db.sqlite3
    ├── gpx_routes_backend  # Ядро проекта
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── poetry.lock
    ├── pyproject.toml
    ├── start.sh    # Команды после старта контейнера
    └── users
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        │   ├── 0001_initial.py
        │   ├── 0002_follow.py
        │   ├── 0003_alter_user_options_alter_follow_unique_together_and_more.py
        │ └── __init__.py
        ├── models.py
        ├── tests.py
        └── views.py
```

### Запуск проекта локально

Для запуска проекта локально необходимо:
1. Если необходимо, создайте папку куда будет склонирован проект, перейти в созданную папку:
   ```output
   ╰─$ mkdir <name dir>
   ╰─$ cd <name dir> # created in the previous step 
   ```
2. В текущей папке создать виртуальное окружение:
   ```output
    ╰─$ python3.11 -m venv .
   ```
3. Склонировать репозиторий в локальную папку
   ```output
   ╰─$ git clone git@github.com/thrashches/gpx_routes_backend.git src
   ```
   У Вас должна получиться следующая структура коталогов:
   ```output
    ╰─$
    ├── bin
    ├── include
    ├── lib
    ├── pyvenv.cfg
    └── src
   ```
4. Активируйте виртуальное окружение, выполнив команду:
   ```output
   ╰─$ source ./bin/activate
   ```
   После выполнения команды, отображение приглашения измениться:
   ```
   (<name venv>)╰─$
   ```
5. Перейдите в директорию `src` выполнив команду:
   ```output
   (<name venv>)╰─$ cd src
   ```
   Структура директории:
   ```output
    ├── .dockerignore
    ├── .env
    ├── .git
    ├── .gitignore
    ├── Makefile
    ├── README.md
    ├── deploy
    └── gpx_routes_backend
   ```
6. Перейдите в директорию `gpx_dev` выполнив команду:
    ```bash
   (<name venv>)╰─$ cd gpx_dev
   ```
    Структура директории:
   ```output
    ├── Dockerfile
    ├── api
    ├── gpx_routes_backend
    ├── manage.py
    ├── poetry.lock
    ├── pyproject.toml
    └── start.sh
   ```

7. Выполните комманду `poetry install`:
   >Warning:
   >---
   >Убедитесь, что у Вас установлен poetry `╰─$ poetry --version`

    ```output
   (<name venv>)╰─$ poetry install
   ```

   >Note:  
   >После установки всех пакетов локально, можно проверить что сервер запускается корректно:
   >```output
   >(<name venv>)╰─$ python manage.py runserver
   >```

8. Для запуска проекта в контейнерах:
   
   - Вернуться на уровень каталога выше:
    ```
    (<name venv>)╰─$ cd ..
    ```
    - Убедитесь, что находитесь в директории с файлами:
    ```Output
    ├── .gitignore
    ├── Makefile
    ├── README.md
    ├── deploy
    └── gpx_dev
   ```
   - Выполните команду:
    ```
    (<name venv>)╰─$ make start-local
    ```
    После скачивания необходимых образов, установки пакетов, проект запустится в контейнерах.

    Для проверки корректрной установки и доступности проекта в браузере перейдите по ссылке:
    `http://localhost:8000/` либо `http://0.0.0.0:8000/`

    Отобразится стартовая страница Django Project

NOTE:
---
Для запуска через docker-compose необходимо в директории deploy:
 - создать файл .env и в нем определить переменную `PG_TAG` - версия POSTGRES,
например `PG_TAG=15.2`
 - создать каталог `env_file`,  внутри которого необходимо создать файл с именем `.env_app`
 - в `.env_app` необходимо задать следующие переменные:
   - `DB_ENGINE`=django.db.backends.postgresql - 
   - `DB_NAME` - имя базы данных
   - `DB_USER` - имя пользователя БД
   - `DB_PASSWORD` - Пароль для БД
   - `DB_HOST` - Хост, на котором работает ваша БД
   - `DB_PORT` - Порт, на котором работает ваша БД
   - `POSTGRES_PASSWORD` - Пароль для БД, рекомендуется такой же как `DB_PASSWORD`
   - `SECRET_KEY` - секретный ключ Django
   - `ALLOWED_HOSTS` - в режиме `DEBUG=True` добавит `['localhost', '127.0.0.1', '[::1]']`
   - `DJANGO_SUPERUSER_USERNAME` Пример admin
   - `DJANGO_SUPERUSER_PASSWORD` 
   - `DJANGO_SUPERUSER_EMAIL` admin@admin.com
   - `DEBUG` - в режиме отладки `True`


Доступные команды:
```
make start-local # Запуск проекта в локальном окружении в контейнерах 
make down-local # Остановка проект и удаление volume
make logs-local # Просмотр логов в консоли
make test # Запуск тестов (В разработке)  
python manage.py runserver # Запуск проекта в режиме разработки(НЕ для production)
```
