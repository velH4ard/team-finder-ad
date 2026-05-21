# Team Finder

Платформа для поиска единомышленников для совместной работы над Pet-проектами.

## Описание

Team Finder — это сервис, позволяющий разработчикам, дизайнерам и другим специалистам публиковать идеи проектов, собирать команду и откликаться на предложения.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/velH4ard/team-finder-ad
   cd team-finder-ad
   ```
2. Создайте файл `.env` на основе `.env_example` и заполните его.
3. Запустите проект с помощью Docker Compose:
   ```bash
   docker compose up --build
   ```
4. Примените миграции:
   ```bash
   docker compose exec web python3 manage.py migrate
   ```

## Примеры запросов

- Получить список проектов: `GET /api/v1/projects/`
- Зарегистрироваться: `POST /api/v1/users/register/` (реализовать)
- Добавить проект в избранное: `POST /api/v1/projects/{id}/favorite/`
