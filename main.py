import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start_command, handle_callback, handle_text_message
from admin import admin_command, handle_admin_callback
from telegram import Update

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")

def main():
    """Основная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        return
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(CallbackQueryHandler(handle_admin_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 