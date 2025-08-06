# Демонстрационные данные товаров
DEMO_PRODUCTS = {
    'rings': [
        {
            'id': 'ring_1',
            'name': '💍 Кольцо с бриллиантом',
            'description': 'Элегантное кольцо с бриллиантом 0.5 карат в белом золоте',
            'price': 150000,
            'image': 'ring_diamond.jpg'
        },
        {
            'id': 'ring_2', 
            'name': '💍 Кольцо с сапфиром',
            'description': 'Красивое кольцо с натуральным сапфиром в желтом золоте',
            'price': 85000,
            'image': 'ring_sapphire.jpg'
        }
    ],
    'earrings': [
        {
            'id': 'earrings_1',
            'name': '👂 Серьги-гвоздики с бриллиантами',
            'description': 'Классические серьги-гвоздики с бриллиантами',
            'price': 95000,
            'image': 'earrings_studs.jpg'
        },
        {
            'id': 'earrings_2',
            'name': '👂 Серьги-люстры с изумрудами',
            'description': 'Роскошные серьги-люстры с изумрудами и бриллиантами',
            'price': 180000,
            'image': 'earrings_chandelier.jpg'
        }
    ],
    'necklaces': [
        {
            'id': 'necklace_1',
            'name': '📿 Колье с жемчугом',
            'description': 'Элегантное колье из натурального жемчуга',
            'price': 65000,
            'image': 'necklace_pearl.jpg'
        },
        {
            'id': 'necklace_2',
            'name': '📿 Колье с рубинами',
            'description': 'Яркое колье с рубинами в белом золоте',
            'price': 120000,
            'image': 'necklace_ruby.jpg'
        }
    ],
    'bracelets': [
        {
            'id': 'bracelet_1',
            'name': '💫 Браслет с бриллиантами',
            'description': 'Тонкий браслет с бриллиантами в белом золоте',
            'price': 110000,
            'image': 'bracelet_diamond.jpg'
        },
        {
            'id': 'bracelet_2',
            'name': '💫 Браслет с аметистами',
            'description': 'Стильный браслет с аметистами в серебре',
            'price': 45000,
            'image': 'bracelet_amethyst.jpg'
        }
    ],
    'watches': [
        {
            'id': 'watch_1',
            'name': '⌚ Часы женские с бриллиантами',
            'description': 'Элегантные женские часы с бриллиантами на ремешке',
            'price': 250000,
            'image': 'watch_ladies.jpg'
        },
        {
            'id': 'watch_2',
            'name': '⌚ Часы мужские золотые',
            'description': 'Классические мужские часы в желтом золоте',
            'price': 320000,
            'image': 'watch_mens.jpg'
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