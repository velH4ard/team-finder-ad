# Team Finder

Team Finder - платформа для поиска единомышленников для совместной работы над pet-проектами.

## Возможности

- просмотр списка актуальных проектов;
- регистрация и вход по email и паролю;
- просмотр публичных профилей пользователей;
- редактирование своего профиля;
- создание и редактирование своих проектов;
- добавление проектов в избранное;
- участие в чужих проектах;
- просмотр списка пользователей с фильтрацией по варианту 1;
- административное управление пользователями, профилями, проектами и избранным через Django admin.

## Стек

- Python 3.9
- Django 3.2
- Django REST Framework
- PostgreSQL 16
- Docker Compose
- Pillow
- python-decouple

## Структура интерфейса

Пользовательская часть проекта работает через шаблоны Django:

- `/` и `/projects/list/` - список проектов;
- `/users/register/` - регистрация;
- `/users/login/` - вход;
- `/users/<id>/` - профиль пользователя;
- `/users/edit-profile/` - редактирование профиля;
- `/users/change-password/` - смена пароля;
- `/users/list/` - список пользователей;
- `/projects/<id>/` - страница проекта;
- `/projects/create-project/` - создание проекта;
- `/projects/<id>/edit/` - редактирование проекта;
- `/projects/favorites/` - избранные проекты.

API также сохранен и доступен отдельно по префиксу `/api/v1/`.

## Подготовка `.env`

Скопируйте `.env_example` в `.env` и заполните значения.

Пример:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Для локального запуска без Docker в `POSTGRES_HOST` можно указать `localhost`, а в `POSTGRES_PORT` - порт локальной базы.

## Запуск через Docker Compose

1. Создайте файл `.env` на основе `.env_example`.
2. Соберите и запустите контейнеры:

```bash
docker compose up --build -d
```

3. Примените миграции:

```bash
docker compose exec web python manage.py migrate
```

4. Создайте суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser
```

5. Откройте проект:

- сайт: `http://127.0.0.1:8000/`
- админка: `http://127.0.0.1:8000/admin/`

## Локальный запуск без Docker

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Подготовьте PostgreSQL и заполните `.env`.
3. Выполните миграции:

```bash
python manage.py migrate
```

4. Запустите сервер:

```bash
python manage.py runserver
```

## Для ревьюера

- проект использует PostgreSQL;
- шаблонная часть реализована через Django views и templates;
- API не удалялось и доступно отдельно;
- настройки берутся из `.env`;
- медиафайлы сохраняются в `media/`;
- данные PostgreSQL в Docker сохраняются в volume `postgres_data`.

## Автор

Елена Есина

- GitHub: `https://github.com/velH4ard`
