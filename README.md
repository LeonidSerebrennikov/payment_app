Приложение развертывается на Docker, запуск: ```docker-compose up --build```

Приложение реализовано на FastAPI, список эндпоинтов http://localhost:8000/docs

В настройках (app/core/config.py) указаны настройки по умолчанию, можно указать свои через .env, пример — .env.example
Создание пользователей и аккаунтов произойдет автоматически при первом развертывании приложения на докере. 

При логине будет возвращен JWT-токен, который в дальнейшем необходимо передавать в заголовке:
```
curl -X 'GET' \
  'http://localhost:8000/admin/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NTcxMzE0fQ.NuVj8ArOmxjf0IYWiF7X_erF7UjHyFzCrAsdCic1AGY'
```
Время действия токена по умолчанию — 30 минут, настраивается в .env

Данные для входа: 

Админ:
login: admin@example.com,
password: admin123 (перед первым развертыванием данные можно заменить в .env )

Пользователь:
login: user@example.com,
password: user123
