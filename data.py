# Демонстрационные данные товаров
DEMO_PRODUCTS = {
    'rings': [
        {
            'id': 'ring_1',
            'name': '💍 Кольцо с бриллиантом',
            'description': 'Элегантное кольцо с бриллиантом 0.5 карат в белом золоте',
            'price': 150000,
            'image': 'ring_diamond.jpg'
        }
    ],
    'earrings': [
        {
            'id': 'earrings_1',
            'name': '👂 Серьги-гвоздики с бриллиантами',
            'description': 'Классические серьги-гвоздики с бриллиантами',
            'price': 95000,
            'image': 'earrings_studs.jpg'
        }
    ]
}

def get_products_by_category(category):
    """Получить товары по категории"""
    return DEMO_PRODUCTS.get(category, [])

def get_product_by_id(product_id):
    """Получить товар по ID"""
    for category_products in DEMO_PRODUCTS.values():
        for product in category_products:
            if product['id'] == product_id:
                return product
    return None

def format_price(price):
    """Форматировать цену"""
    return f"{price:,} ₽".replace(",", " ")

def get_product_text(product):
    """Получить текст для отображения товара"""
    return f"""
{product['name']}

{product['description']}

💰 Цена: {format_price(product['price'])}
""" 