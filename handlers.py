from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards import *
from config import *
from data import get_products_by_category, get_product_text, get_product_by_id
from database import db
from admin import is_admin

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Регистрируем пользователя в базе данных
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.update_user_activity(user.id)
    
    welcome_text = f"""
🎉 Добро пожаловать в {SHOP_NAME}!

{SHOP_DESCRIPTION}

Выберите интересующий вас раздел:
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех callback запросов"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == "main_menu":
        await show_main_menu(query)
    elif callback_data == "catalog":
        await show_catalog(query)
    elif callback_data.startswith("category_"):
        category = callback_data.split("_")[1]
        await show_category(query, category)
    elif callback_data == "orders":
        await show_orders(query)
    elif callback_data == "cart":
        await show_cart(query)
    elif callback_data == "consultation":
        await request_consultation(query)
    elif callback_data == "info":
        await show_info_menu(query)
    elif callback_data == "about":
        await show_about(query)
    elif callback_data == "delivery":
        await show_delivery(query)
    elif callback_data == "contacts":
        await show_contacts(query)
    elif callback_data.startswith("product_"):
        product_id = callback_data.split("_", 1)[1]
        await show_product(query, product_id)
    elif callback_data.startswith("add_to_cart_"):
        product_id = callback_data.split("_")[-1]
        await add_to_cart(query, product_id)
    elif callback_data == "checkout":
        await start_checkout(query)
    elif callback_data == "clear_cart":
        await clear_cart(query)
    elif callback_data == "write_admin":
        await write_admin_request(query)
    elif callback_data == "admin_back":
        await handle_admin_back(query)
    # ИСПРАВЛЕНИЕ: Добавляем обработчики для кнопок "Назад"
    elif callback_data == "back_to_category":
        await show_catalog(query)
    elif callback_data == "catalog":
        await show_catalog(query)

async def show_main_menu(query):
    """Показать главное меню"""
    await query.edit_message_text(
        f"🏠 Главное меню {SHOP_NAME}\n\nВыберите раздел:",
        reply_markup=get_main_menu_keyboard()
    )

async def show_catalog(query):
    """Показать каталог"""
    await query.edit_message_text(
        "💍 Каталог украшений\n\nВыберите категорию:",
        reply_markup=get_catalog_keyboard()
    )

async def show_category(query, category):
    """Показать категорию товаров"""
    category_name = JEWELRY_CATEGORIES.get(category, "Категория")
    products = get_products_by_category(category)
    
    if not products:
        await query.edit_message_text(
            f"{category_name}\n\nВ данной категории пока нет товаров.",
            reply_markup=get_category_keyboard(category)
        )
        return
    
    # Создаем клавиатуру с товарами
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(
            f"{product['name']} - {product['price']:,} ₽".replace(",", " "),
            callback_data=f"product_{product['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад к каталогу", callback_data="catalog")])
    
    await query.edit_message_text(
        f"{category_name}\n\nВыберите товар:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_orders(query):
    """Показать заказы пользователя"""
    await query.edit_message_text(
        "📦 Мои заказы\n\nУ вас пока нет заказов.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]])
    )

async def show_cart(query):
    """Показать корзину"""
    user_id = query.from_user.id
    cart_items = db.get_cart(user_id)
    
    if not cart_items:
        await query.edit_message_text(
            "🛒 Корзина\n\nВаша корзина пуста.",
            reply_markup=get_cart_keyboard()
        )
        return
    
    text = "🛒 Ваша корзина:\n\n"
    total_price = 0
    
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            item_price = product['price'] * item['quantity']
            total_price += item_price
            text += f"• {product['name']}\n"
            text += f"  Количество: {item['quantity']}\n"
            text += f"  Цена: {format_price(item_price)}\n\n"
    
    text += f"💰 Итого: {format_price(total_price)}"
    
    await query.edit_message_text(
        text,
        reply_markup=get_cart_keyboard()
    )

async def request_consultation(query):
    """Запрос консультации"""
    await query.edit_message_text(
        "📞 Консультация\n\nДля получения консультации оставьте свой номер телефона:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📞 Отправить контакт", callback_data="send_contact")
        ], [
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]])
    )

async def show_info_menu(query):
    """Показать меню информации"""
    await query.edit_message_text(
        "⚙️ Информация\n\nВыберите интересующий раздел:",
        reply_markup=get_info_keyboard()
    )

async def show_about(query):
    """Показать информацию о магазине"""
    about_text = f"""
🏢 О нас

{SHOP_NAME}
{SHOP_DESCRIPTION}

Мы предлагаем эксклюзивные украшения ручной работы из драгоценных металлов и камней.
"""
    await query.edit_message_text(
        about_text,
        reply_markup=get_info_keyboard()
    )

async def show_delivery(query):
    """Показать информацию о доставке"""
    delivery_text = """
🚚 Доставка

• Курьерская доставка по Москве - 500₽
• Доставка по России - от 1000₽
• Самовывоз из магазина - бесплатно
• Доставка в день заказа при заказе до 15:00
"""
    await query.edit_message_text(
        delivery_text,
        reply_markup=get_info_keyboard()
    )

async def show_contacts(query):
    """Показать контакты"""
    contacts_text = f"""
📞 Контакты

Телефон: {SHOP_PHONE}
Email: {SHOP_EMAIL}
Адрес: {SHOP_ADDRESS}

Время работы: Пн-Вс 10:00-22:00
"""
    await query.edit_message_text(
        contacts_text,
        reply_markup=get_info_keyboard()
    )

async def show_product(query, product_id):
    """Показать товар"""
    product = get_product_by_id(product_id)
    if not product:
        await query.answer("Товар не найден!")
        return
    
    product_text = get_product_text(product)
    
    # Создаем клавиатуру для товара
    keyboard = [
        [
            InlineKeyboardButton("🛒 В корзину", callback_data=f"add_to_cart_{product_id}"),
            InlineKeyboardButton("❤️ В избранное", callback_data=f"favorite_{product_id}")
        ],
        [InlineKeyboardButton("📞 Заказать звонок", callback_data="call_request")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_category")]
    ]
    
    await query.edit_message_text(
        product_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def write_admin_request(query):
    """Запрос на написание админу"""
    await query.edit_message_text(
        "💬 Написать админу\n\nВведите ваше сообщение:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]])
    )

async def add_to_cart(query, product_id):
    """Добавить товар в корзину"""
    user_id = query.from_user.id
    db.add_to_cart(user_id, product_id)
    await query.answer("✅ Товар добавлен в корзину!")

async def start_checkout(query):
    """Начать оформление заказа"""
    await query.edit_message_text(
        "💳 Оформление заказа\n\nФункция в разработке...",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        ]])
    )

async def clear_cart(query):
    """Очистить корзину"""
    user_id = query.from_user.id
    db.clear_cart(user_id)
    await query.edit_message_text(
        "🗑️ Корзина очищена",
        reply_markup=get_cart_keyboard()
    )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user = update.effective_user
    message_text = update.message.text
    
    # Обновляем активность пользователя
    db.update_user_activity(user.id)
    
    # Если пользователь админ, проверяем специальные команды
    if is_admin(user.id):
        if message_text.startswith('/reply'):
            # Обработка ответа пользователю
            parts = message_text.split(' ', 2)
            if len(parts) >= 3:
                try:
                    target_user_id = int(parts[1])
                    reply_text = parts[2]
                    await send_message_to_user(context.bot, target_user_id, reply_text)
                    await update.message.reply_text(f"✅ Ответ отправлен пользователю {target_user_id}")
                except ValueError:
                    await update.message.reply_text("❌ Неверный формат. Используйте: /reply USER_ID текст")
            return
    
    # Сохраняем сообщение в базу данных
    db.add_message(user.id, message_text)
    
    # Отправляем уведомление админу
    await notify_admin_new_message(context.bot, user, message_text)
    
    # Отвечаем пользователю
    await update.message.reply_text(
        "📨 Ваше сообщение получено! Администратор свяжется с вами в ближайшее время.",
        reply_markup=get_main_menu_keyboard()
    )

async def send_message_to_user(bot, user_id: int, message_text: str):
    """Отправить сообщение пользователю"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"💬 Сообщение от администратора:\n\n{message_text}"
        )
    except Exception as e:
        print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

async def notify_admin_new_message(bot, user, message_text: str):
    """Уведомить админа о новом сообщении"""
    if not ADMIN_ID:
        return
    
    try:
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        if not name:
            name = user.username or f"Пользователь {user.id}"
        
        notification = f"📨 Новое сообщение!\n\n"
        notification += f"От: {name}\n"
        notification += f"ID: {user.id}\n"
        notification += f"Текст: {message_text[:100]}..."
        if len(message_text) > 100:
            notification += " (обрезано)"
        
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=notification
        )
    except Exception as e:
        print(f"Ошибка уведомления админа: {e}")

def format_price(price):
    """Форматировать цену"""
    return f"{price:,} ₽".replace(",", " ") 