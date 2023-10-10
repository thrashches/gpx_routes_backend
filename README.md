
<h2 style="text-align: center;">GPX Project</h2>

---

<h3 style="text-align: center;">Структура проекта</h3>
```bash
╰─$
├── .gitignore
├── Makefile
├── README.md
├── deploy # Сборка проекта
│   ├── docker-compose.base.yml # Базовый docker-compose для сборки
│   ├── docker-compose.local.yml # Сборка и запуск приложения в локальном окружении 
│        └── .env_app # Переменные для docker-compose service: server-local и database
└── gpx_dev
    ├── Dockerfile
    ├── __init__.py
    ├── api
    │    ├── __init__.py
    │    ├── admin.py
    │    ├── apps.py
    │    ├── models.py
    │    ├── tests.py
    │    └── v1
    │       ├── __init__.py
    │       ├── urls.py
    │       └── views.py
    ├── gpx_routes_backend # Ядро проекта
    │    ├── __init__.py
    │    ├── asgi.py
    │    ├── settings.py
    │    ├── urls.py
    │    └── wsgi.py
    ├── manage.py
    ├── poetry.lock
    ├── pyproject.toml
    └── start.sh # Команды после старта контейнера 
   ```


<h3 style="text-align: center;">Запуск проекта локально</h3>

Для запуска проекта локально необходимо:
1. Если необходимо, создайте папку куда будет склонирован проект, перейти в созданную папку:
   ```bash
   ╰─$ mkdir <name dir>
   ╰─$ cd <name dir> # created in the previous step 
   ```
2. В текущей папке создать виртуальное окружение:
   ```bash
    ╰─$ python3.11 -m venv .
   ```
3. Склонировать репозиторий в локальную папку
   ```bash
   ╰─$ git clone git@github.com/thrashches/gpx_routes_backend.git src
   ```
   У Вас должна получиться следующая структура коталогов:
   ```bash
    ╰─$
    ├── bin
    ├── include
    ├── lib
    ├── pyvenv.cfg
    └── src
   ```
4. Активируйте виртуальное окружение, выполнив команду:
   ```bash
   ╰─$ source ./bin/activate
   ```
   После выполнения команды, отображение приглашения измениться:
   ```
   (<name venv>)╰─$
   ```
5. Перейдите в директорию `src` выполнив команду:
   ```bash
   (<name venv>)╰─$ cd src
   ```
   Структура директории:
   ```Output
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
   ```Output
    ├── Dockerfile
    ├── api
    ├── gpx_routes_backend
    ├── manage.py
    ├── poetry.lock
    ├── pyproject.toml
    └── start.sh
   ```

7. Выполните комманду `poetry install`:
   >Warning:<br>
   >---
   >Убедитесь, что у Вас установлен poetry `╰─$ poetry --version`

    ```bash
   (<name venv>)╰─$ poetry install
   ```

   >Note:<br>
   >После установки всех пакетов локально, можно проверить что сервер запускается корректно:
   >```bash
   >(<name venv>)╰─$ python manage.py runserver
   >```

8. Для запуска проекта в контейнерах:
   
   - Вернуться на уровень каталога выше:
    ```
    (<name venv>)╰─$ cd ..
    ```
    - Убедитесь, что находитесь в дериктории с файлами:
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
    После скачивания необходимых образов, установки пакетов, проект запуститься в контейнерах.

    Для проверки корректрной установки и доступности проекта в браузере перейдите по ссылке:
    `http://localhost:8000/` либо `http://0.0.0.0:8000/`

    Отобразится стартовая страница Django Project

NOTE:<br>
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
