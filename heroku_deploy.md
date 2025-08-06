# 🚀 Развертывание на Heroku

## Быстрый старт

### 1. Установите Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Скачайте с https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Войдите в Heroku
```bash
heroku login
```

### 3. Создайте приложение
```bash
heroku create ваш-ювелирный-бот
```

### 4. Настройте переменные окружения
```bash
heroku config:set BOT_TOKEN=7569172964:AAHrUYPE04vKqUhN-Si5UJC1fZNVGSShJOk
heroku config:set ADMIN_ID=ваш_telegram_id
```

### 5. Разверните приложение
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

### 6. Запустите воркер
```bash
heroku ps:scale worker=1
```

## Мониторинг
```bash
# Просмотр логов
heroku logs --tail

# Статус приложения
heroku ps
```

## Обновление
```bash
git add .
git commit -m "Update"
git push heroku main
``` 