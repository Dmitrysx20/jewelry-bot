from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import JEWELRY_CATEGORIES

def get_main_menu_keyboard():
    """Главное меню бота"""
    keyboard = [
        [InlineKeyboardButton("💍 Каталог украшений", callback_data="catalog")],
        [InlineKeyboardButton("📦 Мои заказы", callback_data="orders")],
        [InlineKeyboardButton("🛒 Корзина", callback_data="cart")],
        [InlineKeyboardButton("📞 Консультация", callback_data="consultation")],
        [InlineKeyboardButton("💬 Написать админу", callback_data="write_admin")],
        [InlineKeyboardButton("⚙️ О нас / Доставка / Контакты", callback_data="info")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_catalog_keyboard():
    """Клавиатура каталога"""
    keyboard = []
    for key, value in JEWELRY_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(value, callback_data=f"category_{key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_category_keyboard(category):
    """Клавиатура для категории товаров"""
    keyboard = [
        [InlineKeyboardButton("🔍 Фильтры", callback_data=f"filters_{category}")],
        [InlineKeyboardButton("💰 По цене", callback_data=f"sort_price_{category}")],
        [InlineKeyboardButton("⭐ По популярности", callback_data=f"sort_popular_{category}")],
        [InlineKeyboardButton("🔙 Назад к каталогу", callback_data="catalog")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_keyboard(product_id):
    """Клавиатура для товара"""
    keyboard = [
        [
            InlineKeyboardButton("🛒 В корзину", callback_data=f"add_to_cart_{product_id}"),
            InlineKeyboardButton("❤️ В избранное", callback_data=f"favorite_{product_id}")
        ],
        [InlineKeyboardButton("📞 Заказать звонок", callback_data="call_request")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_category")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cart_keyboard():
    """Клавиатура корзины"""
    keyboard = [
        [InlineKeyboardButton("💳 Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart")],
        [InlineKeyboardButton("🔙 Продолжить покупки", callback_data="catalog")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_contact_keyboard():
    """Клавиатура для отправки контакта"""
    keyboard = [[KeyboardButton("📞 Отправить контакт", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def get_info_keyboard():
    """Клавиатура информации о магазине"""
    keyboard = [
        [InlineKeyboardButton("🏢 О нас", callback_data="about")],
        [InlineKeyboardButton("🚚 Доставка", callback_data="delivery")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard) 