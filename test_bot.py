#!/usr/bin/env python3
"""
Тестовый файл для проверки функциональности бота
"""

from data import DEMO_PRODUCTS, get_products_by_category, get_product_by_id, format_price, get_product_text

def test_data_functions():
    """Тестирование функций работы с данными"""
    print("🧪 Тестирование функций работы с данными...")
    
    # Тест получения товаров по категории
    rings = get_products_by_category('rings')
    print(f"✅ Кольца найдено: {len(rings)}")
    
    # Тест получения товара по ID
    product = get_product_by_id('ring_1')
    if product:
        print(f"✅ Товар найден: {product['name']}")
    
    # Тест форматирования цены
    price = format_price(150000)
    print(f"✅ Форматированная цена: {price}")
    
    # Тест получения текста товара
    if product:
        text = get_product_text(product)
        print(f"✅ Текст товара:\n{text}")

def test_categories():
    """Тестирование категорий"""
    print("\n📂 Тестирование категорий...")
    
    for category, name in DEMO_PRODUCTS.items():
        products = get_products_by_category(category)
        print(f"✅ {name}: {len(products)} товаров")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов ювелирного бота\n")
    
    test_data_functions()
    test_categories()
    
    print("\n✅ Все тесты завершены!")

if __name__ == "__main__":
    main() 