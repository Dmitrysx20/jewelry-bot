#!/usr/bin/env python3
"""
Тестирование базы данных бота
"""

from database import db
from data import DEMO_PRODUCTS

def test_database():
    """Тестирование функций базы данных"""
    print("🧪 Тестирование базы данных...")
    
    # Тест добавления пользователя
    print("\n1. Тестирование пользователей:")
    db.add_user(123456789, "test_user", "Тест", "Пользователь")
    user = db.get_user(123456789)
    if user:
        print(f"✅ Пользователь добавлен: {user['first_name']} {user['last_name']}")
    
    # Тест добавления сообщения
    print("\n2. Тестирование сообщений:")
    db.add_message(123456789, "Тестовое сообщение")
    messages = db.get_unread_messages()
    print(f"✅ Непрочитанных сообщений: {len(messages)}")
    
    # Тест корзины
    print("\n3. Тестирование корзины:")
    db.add_to_cart(123456789, "ring_1")
    db.add_to_cart(123456789, "earrings_1")
    cart = db.get_cart(123456789)
    print(f"✅ Товаров в корзине: {len(cart)}")
    
    # Тест получения всех пользователей
    print("\n4. Тестирование списка пользователей:")
    users = db.get_all_users()
    print(f"✅ Всего пользователей: {len(users)}")
    
    # Очистка тестовых данных
    print("\n5. Очистка тестовых данных:")
    db.clear_cart(123456789)
    print("✅ Корзина очищена")

def show_database_structure():
    """Показать структуру базы данных"""
    print("\n📊 Структура базы данных:")
    
    import sqlite3
    with sqlite3.connect("jewelry_bot.db") as conn:
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Таблица: {table_name}")
            
            # Получаем структуру таблицы
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование базы данных ювелирного бота\n")
    
    test_database()
    show_database_structure()
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    main() 