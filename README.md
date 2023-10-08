
<h2 style="text-align: center;">GPX Project</h2>

---

<h3 style="text-align: center;">Структура проекта</h3>
```bash
╰─$
├── .gitignore
├── Makefile
├── README.md
├── deploy # Сборка проекта
│   ├── .env # Переменные для docker-compose engine
│   ├── docker-compose.base.yml # Базовый docker-compose для сборки
│   ├── docker-compose.local.yml # Сборка и запуск приложения в локальном окружении 
│   └── env_file
│        └── .env_app # Переменные для docker-compose service: server-local и database
└── gpx_dev
    ├── .env
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
    ├── core # Ядро проекта
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
    ├── docker-compose-dev.yml
    ├── env_file
    └── smartfact_dev
   ```
6. Перейдите в директорию `gpx_dev` выполнив команду:
    ```bash
   (<name venv>)╰─$ cd gpx_dev
   ```
    Структура директории:
   ```Output
    ├── Dockerfile
    ├── api
    ├── core
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
Admin User for Admin pannel:
   * Login: admin
   * Password: 1234

Определён в файле `/env_file/.env_app`

DJANGO_SUPERUSER_USERNAME=admin<br>
DJANGO_SUPERUSER_PASSWORD=1234<br>
DJANGO_SUPERUSER_EMAIL="admin@admin.com"<br>

Доступные команды:
```
make start-local # Запуск проекта в локальном окружении
make down-local # Остановка проект и удаление volume
make logs-local # Просмотр логов в консоли
make test # Запуск тестов (В разработке)  
```
