# Django stripe-test
Django-приложение для создания Stripe Checkout Sessions.
- создавать товары через Django Admin;
- просматривать информацию о товаре;
- создавать Stripe Checkout Session;
- оплачивать товары через Stripe Checkout;
- создавать заказы из нескольких товаров;
- применять скидки;
- применять налоги;
- использовать разные Stripe-конфигурации для USD и EUR.

## Стек
- Python 3.14
- Django 6.1
- PostgreSQL 17
- Stripe API
- Docker
- Docker Compose
- JavaScript
- HTML
- Stripe.js

## Запуск
### 1. Создание .env
Скопировать пример конфигурации:
```bash
cp .env.example .env
```
Заполнить Stripe keys:
```dotenv
STRIPE_USD_SECRET_KEY=
STRIPE_USD_PUBLISHABLE_KEY=

STRIPE_EUR_SECRET_KEY=
STRIPE_EUR_PUBLISHABLE_KEY=
```
Остальные параметры настроены для запуска через Docker.

### 2. Запуск приложения
```bash
docker compose up -d --build
```

### 3. Миграции
```bash
docker compose exec web python manage.py migrate
```

### 4. Создание администратора
```bash
docker compose exec web python manage.py createsuperuser
```
После этого Django Admin доступен по адресу:
```url
http://localhost:8000/admin/
```

## API
### GET /item/\<id>/
Возвращает HTML-страницу выбранного товара.\
Пример:
```url
GET /item/1/
```

### GET /buy/\<id>/
Создает Stripe Checkout Session для выбранного товара.\
Пример:
```url
GET /buy/1/
```
Пример ответа:
```json
{
  "id": "cs_test_..."
}
```

### GET /
Возвращает HTML-страницу со списком товаров.

### GET /order-list/
Возвращает HTML-страницу со списком заказов.

###  GET /order/\<id>/
Возвращает HTML-страницу выбранного заказа.\
Пример:
```url
GET /order/1/
```

### GET /buy-order/\<id>/
Создает Stripe Checkout Session для выбранного заказа.\
Пример:
```url
GET /buy-order/1/
```
Пример ответа:
```json
{
  "id": "cs_test_..."
}
```