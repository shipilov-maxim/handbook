# Handbook API

REST API для работы со справочником организаций, зданий и видов деятельности.  
Реализовано на **FastAPI**, с использованием **SQLAlchemy**, **Pydantic** и **Alembic**.  
Поддерживается работа в **Docker** и документация в **Swagger UI** / **ReDoc**.

## Возможности
- CRUD-операции с организациями, видами деятельности и зданиями
- Фильтрация по зданиям, видам деятельности (включая вложенные) и геолокации
- Ограничение вложенности видов деятельности до 3 уровней
- Авторизация через API-Key

## Технологии
- Python 3.12+
- FastAPI
- SQLAlchemy (Async)
- Alembic
- PostgreSQL
- Docker & Docker Compose

## Запуск проекта

1. **Клонировать репозиторий**:
   ```bash
   git clone https://github.com/shipilov-maxim/handbook.git
   cd handbook
2. **Создать .env файл на основе .env_sample и указать свои переменные.**

3. **Запустить через Docker:**

```bash
docker compose up --build
```
4. **Документация API:**

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc