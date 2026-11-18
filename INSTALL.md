# Установка и запуск ShoeStore

## Требования
- Windows 10/11
- Docker Desktop (Linux containers) с Docker Compose v2

## Что входит в комплект
EXE-приложение «Магазин обуви» (папка application\ShoeStore) и файлы для запуска PostgreSQL в Docker (папка deployment). База данных внутрь EXE не упакована: она работает в отдельном контейнере.

## 1. Запуск базы данных
1. В папке deployment скопируйте `.env.example` в `.env`.
2. В `.env` задайте свой локальный пароль в `POSTGRES_PASSWORD`. Не публикуйте этот файл.
3. Откройте cmd в папке deployment и выполните `docker compose up -d`.
4. Дождитесь статуса healthy: `docker compose ps`.

## 2. Первичная загрузка данных (только для пустой базы)
`docker compose cp database/shoes_shop.sql db:/tmp/shoes_shop.sql`
`docker compose exec db psql -v ON_ERROR_STOP=1 -U postgres -d shoes_shop -f /tmp/shoes_shop.sql`
Если база уже заполнена, повторный импорт не выполнять (будет ошибка «relation already exists»).

## 3. Настройка приложения
1. Скопируйте `config.ini.example` в `application\ShoeStore\config.ini`, то есть рядом с `ShoeStore.exe`.
2. Укажите: host = 127.0.0.1, port = 5433, name = shoes_shop, user = postgres, пароль из `.env`.

## 4. Запуск
Откройте `application\ShoeStore\ShoeStore.exe`. Папку нужно переносить целиком, одиночный EXE работать не будет.

## 5. Остановка
`docker compose stop`. Команду `docker compose down -v` не использовать: она удаляет данные.

## Типичные проблемы
- «Не удалось подключиться к базе данных»: проверьте `docker compose ps` (db healthy), порт и пароль в `config.ini`.
- port is already allocated: порт 5433 занят, задайте другой в `.env` (`POSTGRES_HOST_PORT`) и в `config.ini`.
- Нет картинок: EXE перенесён без папки `_internal`.