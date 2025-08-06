import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class Database:
    def __init__(self, db_path: str = "jewelry_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_admin BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Таблица сообщений
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message_text TEXT,
                    message_type TEXT DEFAULT 'user_message',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица корзины
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product_id TEXT,
                    quantity INTEGER DEFAULT 1,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    order_data TEXT,
                    total_price REAL,
                    status TEXT DEFAULT 'new',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Добавить нового пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получить пользователя по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def update_user_activity(self, user_id: int):
        """Обновить время последней активности пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_activity = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
    
    def set_user_phone(self, user_id: int, phone: str):
        """Установить телефон пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET phone = ? WHERE user_id = ?', (phone, user_id))
            conn.commit()
    
    def add_message(self, user_id: int, message_text: str, message_type: str = 'user_message'):
        """Добавить сообщение"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (user_id, message_text, message_type)
                VALUES (?, ?, ?)
            ''', (user_id, message_text, message_type))
            conn.commit()
    
    def get_unread_messages(self) -> List[Dict]:
        """Получить все непрочитанные сообщения"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, u.first_name, u.last_name, u.username
                FROM messages m
                JOIN users u ON m.user_id = u.user_id
                WHERE m.is_read = FALSE AND m.message_type = 'user_message'
                ORDER BY m.timestamp DESC
            ''')
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def mark_message_read(self, message_id: int):
        """Отметить сообщение как прочитанное"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE messages SET is_read = TRUE WHERE id = ?', (message_id,))
            conn.commit()
    
    def get_all_users(self) -> List[Dict]:
        """Получить всех пользователей"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY registration_date DESC')
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_user_messages(self, user_id: int) -> List[Dict]:
        """Получить сообщения пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM messages 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 50
            ''', (user_id,))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def add_to_cart(self, user_id: int, product_id: str, quantity: int = 1):
        """Добавить товар в корзину"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Проверяем, есть ли уже такой товар в корзине
            cursor.execute('''
                SELECT id, quantity FROM cart 
                WHERE user_id = ? AND product_id = ?
            ''', (user_id, product_id))
            
            existing = cursor.fetchone()
            
            if existing:
                # Обновляем количество
                new_quantity = existing[1] + quantity
                cursor.execute('''
                    UPDATE cart SET quantity = ? WHERE id = ?
                ''', (new_quantity, existing[0]))
            else:
                # Добавляем новый товар
                cursor.execute('''
                    INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (?, ?, ?)
                ''', (user_id, product_id, quantity))
            
            conn.commit()
    
    def get_cart(self, user_id: int) -> List[Dict]:
        """Получить корзину пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cart WHERE user_id = ?
                ORDER BY added_date DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def clear_cart(self, user_id: int):
        """Очистить корзину пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
            conn.commit()

# Создаем глобальный экземпляр базы данных
db = Database() 