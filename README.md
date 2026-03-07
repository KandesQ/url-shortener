# URL Shortener

Сервис для сокращения ссылок с возможностью отслеживания переходов


## Запуск
<hr>

1. Запустите [Docker](https://www.docker.com/)
2. В терминале введите:
```bash
  docker-compose up -d
```

## Эндпоинты
<hr>

- Получить short_id, __POST__: http://localhost:8000/api/v1/shorten
- Перейти на исходный url, __GET__: http://localhost:8000/api/v1/{short_id}
- Получить количество переходов, __GET__: http://localhost:8000/api/v1/stats/{short_id}

Тестировал работу через __Chrome__ и __Postman__

## Тесты
<hr>

- Для тестов также должен быть запущен [Docker](https://www.docker.com/)
- В терминале введите:
```bash
  pytest
```