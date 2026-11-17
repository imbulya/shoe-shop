# ShoesShop — система учёта и заказов обуви

Учебный проект демонстрационного экзамена: десктопное приложение для просмотра
каталога обуви и работы с заказами. База данных — PostgreSQL.

## Возможности
- вход по логину и паролю или вход гостем;
- каталог товаров с фотографией, ценой, скидкой и количеством на складе
  (скидка больше 15 % и отсутствие товара выделяются цветом);
- сортировка, фильтрация и поиск товаров;
- для администратора: добавление, редактирование и удаление товаров;
- для администратора и менеджера: просмотр, создание, изменение и удаление заказов.

## Роли пользователей
Гость, авторизованный клиент, менеджер, администратор.

## Требования
- Python 3.9 или новее
- PostgreSQL 14
- библиотеки из файла requirements.txt (PySide6, psycopg2-binary)

## Установка и запуск
1. Клонировать репозиторий: `git clone <адрес репозитория>`
2. Создать окружение и установить зависимости:
   `python -m venv venv`, `venv\Scripts\activate`, `pip install -r requirements.txt`
3. Создать базу данных `shoes_shop` и загрузить скрипт `sql/shoes_shop.sql`.
4. Скопировать `config.ini.example` в `config.ini` и указать параметры подключения.
5. Запустить приложение: `python main.py`

## Структура репозитория
- `main.py` — точка входа, переходы между страницами
- `database.py` — работа с базой данных
- `ui/` — окна и виджеты приложения
- `resources/` — фотографии товаров, логотип, заглушка
- `sql/` — скрипт базы данных с данными
- `docs/` — ER-диаграмма

## Автор
Погребенная У.К., группа ЩПКО-04-23

## ER-диаграмма базы данных
Файл диаграммы: `docs/er-diagram.pdf`. Основные таблицы:
- `products` — товары (артикул, название, цена, скидка, категория, количество);
- `users`, `roles` — пользователи и их роли;
- `warehouses` — пункты выдачи заказов;
- `orders`, `order_items` — заказы и состав заказов;
- `stock_levels` — остатки товаров по складам.

## Запуск PostgreSQL через Docker Compose

Требования: Docker Desktop (Linux containers) с Docker Compose v2.

1. Скопировать `.env.example` в `.env` и заменить `POSTGRES_PASSWORD` на свой локальный пароль (файл `.env` в Git не попадает).
2. Запустить сервисы: `docker compose up --build -d`
3. Проверить состояние: `docker compose ps` (db — healthy, db-check — Exited (0) после проверки).
4. Импортировать базу (из корня проекта):
   `docker compose cp sql/shoes_shop.sql db:/tmp/shoes_shop.sql`
   `docker compose exec db psql -v ON_ERROR_STOP=1 -U postgres -d shoes_shop -f /tmp/shoes_shop.sql`
5. Проверить таблицы: `docker compose run --rm db-check` (ожидается «OK: база=shoes_shop; таблиц=7»).
6. В `config.ini` указать `host = localhost`, `port = 5433`, `name = shoes_shop`, `user = postgres` и пароль из `.env`.
7. Запустить приложение: `python main.py`
8. Остановить: `docker compose stop`, снова запустить: `docker compose start`. Команду `docker compose down -v` не использовать: она удаляет данные.

Адреса: приложение на Windows подключается к `localhost:5433`, сервис db-check внутри Compose — к `db:5432`.

## Постоянное хранение и сети

Данные PostgreSQL хранятся в именованном томе `db_data` и сохраняются после пересоздания контейнера.
Сервисы db и db-check подключены к пользовательской сети `shoe-backend`.

Резервная копия (папка backups/ не попадает в Git):
`docker compose exec db pg_dump -U postgres -d shoes_shop -f /tmp/shoes_shop_before_volume.sql`
`docker compose cp db:/tmp/shoes_shop_before_volume.sql backups/shoes_shop_before_volume.sql`

Восстановление в пустую базу:
`docker compose cp backups/shoes_shop_before_volume.sql db:/tmp/restore.sql`
`docker compose exec db psql -v ON_ERROR_STOP=1 -U postgres -d shoes_shop -f /tmp/restore.sql`

Запуск: `docker compose up --build -d`; пересоздание только БД: `docker compose up -d --force-recreate db`.

Адреса: приложение на Windows подключается к `localhost:5433` (порт открыт только на 127.0.0.1), db-check внутри сети Compose — к `db:5432`.

Внимание: команда `docker compose down -v` удаляет том с данными и в этом проекте не используется.