# Billing Service — тарифы, подписки и платежи

## Назначение проекта

Управляет жизненным циклом подписки и связывает SaaS-приложение с платёжной системой ЮKassa.

## Функциональность

Создание и чтение тарифов, создание и поиск подписок, создание платежа в ЮKassa, обработчик уведомления об оплате, публикация события об оплате в Kafka.

## Архитектура

`main.py` подключает роутеры `tariffs.py`, `subscriptions.py` и `payments.py`. PostgreSQL хранит тарифы, подписки и платежи. `yookassa_service.py` оборачивает платёжный SDK, `kafka_producer.py` пишет в топик `payment`.

### С чего начать чтение кода

- [`payments.py`](payments.py)
- [`db_provider.py`](db_provider.py)
- [`kafka_producer.py`](kafka_producer.py)

[Граф связей Graphify](graphify-out/graph.html) · [Отчёт Graphify](graphify-out/GRAPH_REPORT.md)

Для поиска по графу из корня репозитория выполните `graphify god-nodes --top 5` или `graphify query "имя функции или модуля"`.

## Технологический стек

Python 3.11, FastAPI, Pydantic, SQLAlchemy, asyncpg, PostgreSQL, Alembic, Confluent Kafka, ЮKassa SDK, Docker Compose.

## Технические решения

Цена определяется по тарифу связанной подписки. Входная и платёжная модели разделены. Стартовый скрипт запускает Alembic перед Uvicorn.

## Запуск проекта

Задайте `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `KAFKA_BROKER_URL`, `YOOKASSA_SHOP_ID`, `YOOKASSA_SECRET_KEY`, `YOOKASSA_RETURN_URL`. Проверьте передачу настроек из окружения в контейнер по `compose.yml`. Подключите доступный Kafka и внешнюю сеть `saas_network`. Выполните `docker compose up --build`. API опубликован на 8008. Локальная миграция — `alembic upgrade head`.

## Примеры API

`GET /tariffs/`, `POST /tariffs/`, `POST /subscriptions/`, `GET /subscriptions/user/{user_id}`, `POST /create/`, `POST /webhook`.

```bash
curl -i http://localhost:8008/tariffs/
```

## Тестирование

В исходниках проекта отдельный набор автоматических тестов не обнаружен. Для ручной проверки используйте сценарий из раздела «Примеры API» на тестовой инфраструктуре.

## Ограничения и дальнейшее развитие

Нужны проверка происхождения и идемпотентность webhook, согласование Kafka-топика с получателями и проверка ошибок SDK.

## Мой вклад

TODO — описать свою роль, реализованные компоненты и принятые технические решения.

[Технический обзор проекта](PROJECT_REVIEW.md)
