# 🖥️ Развертывание на VPS

## Подготовка сервера

### 1. Подключитесь к серверу
```bash
ssh user@your-server-ip
```

### 2. Обновите систему
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Установите Python и зависимости
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

### 4. Создайте пользователя для бота
```bash
sudo adduser botuser
sudo usermod -aG sudo botuser
su - botuser
```

## Развертывание бота

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/jewelry-bot.git
cd jewelry-bot
```

### 2. Создайте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Создайте .env файл
```bash
cp env_example.txt .env
nano .env
```

Добавьте:
```env
BOT_TOKEN=7569172964:AAHrUYPE04vKqUhN-Si5UJC1fZNVGSShJOk
ADMIN_ID=ваш_telegram_id
```

### 5. Создайте systemd сервис
```bash
sudo nano /etc/systemd/system/jewelry-bot.service
```

Содержимое:
```ini
[Unit]
Description=Jewelry Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/jewelry-bot
Environment=PATH=/home/botuser/jewelry-bot/venv/bin
ExecStart=/home/botuser/jewelry-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Запустите сервис
```bash
sudo systemctl daemon-reload
sudo systemctl enable jewelry-bot
sudo systemctl start jewelry-bot
```

## Мониторинг

### Просмотр логов
```bash
sudo journalctl -u jewelry-bot -f
```

### Статус сервиса
```bash
sudo systemctl status jewelry-bot
```

### Перезапуск
```bash
sudo systemctl restart jewelry-bot
```

## Обновление
```bash
cd jewelry-bot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart jewelry-bot
```

## Рекомендуемые VPS провайдеры
- **DigitalOcean** - от $5/месяц
- **Linode** - от $5/месяц  
- **Vultr** - от $2.50/месяц
- **Contabo** - от €4/месяц 