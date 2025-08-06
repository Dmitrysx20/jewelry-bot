import os
from dotenv import load_dotenv

load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Настройки базы данных (если понадобится)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///jewelry_bot.db')

# Настройки магазина
SHOP_NAME = "💎 Ювелирный Дом"
SHOP_DESCRIPTION = "Эксклюзивные украшения ручной работы"
SHOP_PHONE = "+7 (999) 123-45-67"
SHOP_EMAIL = "info@jewelry-shop.ru"
SHOP_ADDRESS = "г. Москва, ул. Примерная, д. 1"

# Категории украшений
JEWELRY_CATEGORIES = {
    'rings': '💍 Кольца',
    'earrings': '👂 Серьги', 
    'necklaces': '📿 Колье',
    'bracelets': '💫 Браслеты',
    'watches': '⌚ Часы'
} 