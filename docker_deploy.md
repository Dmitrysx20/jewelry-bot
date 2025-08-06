# 🐳 Развертывание с Docker

## Быстрый старт

### 1. Установите Docker
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows
# Скачайте Docker Desktop с https://docker.com
```

### 2. Создайте .env файл
```bash
cp env_example.txt .env
```

Отредактируйте `.env`:
```env
BOT_TOKEN=7569172964:AAHrUYPE04vKqUhN-Si5UJC1fZNVGSShJOk
ADMIN_ID=ваш_telegram_id
```

### 3. Запустите с Docker Compose
```bash
docker-compose up -d
```

### 4. Проверьте логи
```bash
docker-compose logs -f
```

## Команды управления

### Запуск
```bash
docker-compose up -d
```

### Остановка
```bash
docker-compose down
```

### Перезапуск
```bash
docker-compose restart
```

### Обновление
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Развертывание на сервере

### 1. Установите Docker на сервер
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/jewelry-bot.git
cd jewelry-bot
```

### 3. Настройте переменные
```bash
cp env_example.txt .env
nano .env
```

### 4. Запустите
```bash
docker-compose up -d
```

## Преимущества Docker
- Изолированная среда
- Легкое развертывание
- Масштабируемость
- Переносимость
- Автоматический перезапуск 