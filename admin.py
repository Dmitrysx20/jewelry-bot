from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db
from config import ADMIN_ID
from data import get_product_by_id, format_price
import json

def is_admin(user_id: int) -> bool:
    """Проверить, является ли пользователь админом"""
    return str(user_id) == str(ADMIN_ID)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /admin"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ У вас нет доступа к админ-панели.")
        return
    
    await show_admin_menu(update.message)

async def show_admin_menu(message):
    """Показать админ-меню"""
    keyboard = [
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("📨 Сообщения", callback_data="admin_messages")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    
    await message.reply_text(
        "🔧 Админ-панель\n\nВыберите раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик админ callback'ов"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.edit_message_text("❌ У вас нет доступа к админ-панели.")
        return
    
    callback_data = query.data
    
    if callback_data == "admin_users":
        await show_users_list(query)
    elif callback_data == "admin_messages":
        await show_messages_list(query)
    elif callback_data == "admin_stats":
        await show_statistics(query)
    elif callback_data.startswith("admin_user_"):
        user_id_to_view = callback_data.split("_")[2]
        await show_user_details(query, int(user_id_to_view))
    elif callback_data.startswith("admin_message_"):
        message_id = callback_data.split("_")[2]
        await show_message_details(query, int(message_id))
    elif callback_data.startswith("reply_to_"):
        user_id_to_reply = callback_data.split("_")[2]
        await start_reply_to_user(query, int(user_id_to_reply))

async def show_users_list(query):
    """Показать список пользователей"""
    users = db.get_all_users()
    
    if not users:
        await query.edit_message_text(
            "👥 Пользователи\n\nПользователей пока нет.",
            reply_markup=get_admin_back_keyboard()
        )
        return
    
    text = f"👥 Пользователи ({len(users)})\n\n"
    
    # Показываем только первых 10 пользователей
    for i, user in enumerate(users[:10], 1):
        name = f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
        if not name:
            name = user['username'] or f"Пользователь {user['user_id']}"
        
        text += f"{i}. {name}\n"
        text += f"   ID: {user['user_id']}\n"
        if user['phone']:
            text += f"   📞 {user['phone']}\n"
        text += f"   📅 {user['registration_date'][:10]}\n\n"
    
    if len(users) > 10:
        text += f"... и еще {len(users) - 10} пользователей"
    
    keyboard = []
    for user in users[:5]:  # Показываем кнопки для первых 5 пользователей
        name = f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
        if not name:
            name = user['username'] or f"ID: {user['user_id']}"
        
        keyboard.append([InlineKeyboardButton(
            f"👤 {name[:20]}", 
            callback_data=f"admin_user_{user['user_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="admin_back")])
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_user_details(query, user_id):
    """Показать детали пользователя"""
    user = db.get_user(user_id)
    if not user:
        await query.edit_message_text(
            "❌ Пользователь не найден.",
            reply_markup=get_admin_back_keyboard()
        )
        return
    
    name = f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
    if not name:
        name = user['username'] or f"Пользователь {user['user_id']}"
    
    text = f"👤 Детали пользователя\n\n"
    text += f"Имя: {name}\n"
    text += f"ID: {user['user_id']}\n"
    text += f"Username: @{user['username']}\n" if user['username'] else "Username: не указан\n"
    text += f"Телефон: {user['phone']}\n" if user['phone'] else "Телефон: не указан\n"
    text += f"Дата регистрации: {user['registration_date']}\n"
    text += f"Последняя активность: {user['last_activity']}\n"
    
    # Получаем корзину пользователя
    cart = db.get_cart(user_id)
    text += f"Товаров в корзине: {len(cart)}\n"
    
    keyboard = [
        [InlineKeyboardButton("💬 Написать пользователю", callback_data=f"reply_to_{user_id}")],
        [InlineKeyboardButton("🛒 Посмотреть корзину", callback_data=f"admin_cart_{user_id}")],
        [InlineKeyboardButton("🔙 Назад к пользователям", callback_data="admin_users")]
    ]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_messages_list(query):
    """Показать список сообщений"""
    messages = db.get_unread_messages()
    
    if not messages:
        await query.edit_message_text(
            "📨 Сообщения\n\nНепрочитанных сообщений нет.",
            reply_markup=get_admin_back_keyboard()
        )
        return
    
    text = f"📨 Непрочитанные сообщения ({len(messages)})\n\n"
    
    keyboard = []
    for i, message in enumerate(messages[:5], 1):
        name = f"{message['first_name'] or ''} {message['last_name'] or ''}".strip()
        if not name:
            name = message['username'] or f"Пользователь {message['user_id']}"
        
        text += f"{i}. От: {name}\n"
        text += f"   {message['message_text'][:50]}...\n"
        text += f"   {message['timestamp'][:16]}\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"📨 {name[:20]}", 
            callback_data=f"admin_message_{message['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="admin_back")])
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_message_details(query, message_id):
    """Показать детали сообщения"""
    # Получаем сообщение из базы
    messages = db.get_unread_messages()
    message = None
    for msg in messages:
        if msg['id'] == message_id:
            message = msg
            break
    
    if not message:
        await query.edit_message_text(
            "❌ Сообщение не найдено.",
            reply_markup=get_admin_back_keyboard()
        )
        return
    
    name = f"{message['first_name'] or ''} {message['last_name'] or ''}".strip()
    if not name:
        name = message['username'] or f"Пользователь {message['user_id']}"
    
    text = f"📨 Сообщение\n\n"
    text += f"От: {name}\n"
    text += f"ID пользователя: {message['user_id']}\n"
    text += f"Время: {message['timestamp']}\n\n"
    text += f"Текст:\n{message['message_text']}"
    
    keyboard = [
        [InlineKeyboardButton("✅ Прочитано", callback_data=f"mark_read_{message_id}")],
        [InlineKeyboardButton("💬 Ответить", callback_data=f"reply_to_{message['user_id']}")],
        [InlineKeyboardButton("🔙 Назад к сообщениям", callback_data="admin_messages")]
    ]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_statistics(query):
    """Показать статистику"""
    users = db.get_all_users()
    messages = db.get_unread_messages()
    
    text = "📊 Статистика\n\n"
    text += f"👥 Всего пользователей: {len(users)}\n"
    text += f"📨 Непрочитанных сообщений: {len(messages)}\n"
    
    # Статистика по дням регистрации
    from datetime import datetime, timedelta
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    new_users_week = 0
    for user in users:
        reg_date = datetime.strptime(user['registration_date'][:10], '%Y-%m-%d').date()
        if reg_date >= week_ago:
            new_users_week += 1
    
    text += f"🆕 Новых пользователей за неделю: {new_users_week}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_back")]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_reply_to_user(query, user_id):
    """Начать ответ пользователю"""
    user = db.get_user(user_id)
    if not user:
        await query.edit_message_text(
            "❌ Пользователь не найден.",
            reply_markup=get_admin_back_keyboard()
        )
        return
    
    name = f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
    if not name:
        name = user['username'] or f"Пользователь {user['user_id']}"
    
    # Сохраняем состояние для ответа
    query.from_user.id = user_id  # Временно сохраняем ID пользователя для ответа
    
    await query.edit_message_text(
        f"💬 Ответ пользователю {name}\n\nВведите ваш ответ:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Отмена", callback_data="admin_back")
        ]])
    )

def get_admin_back_keyboard():
    """Клавиатура возврата в админ-панель"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 Админ-панель", callback_data="admin_back")
    ]])

async def handle_admin_back(query):
    """Обработчик возврата в админ-панель"""
    await show_admin_menu(query.message) 