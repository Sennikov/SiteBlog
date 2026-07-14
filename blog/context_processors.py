from .models import MenuItem, Category

def menu_items(request):
    items = []

    # 1. Ручные пункты меню
    for item in MenuItem.objects.filter(is_active=True).order_by('order'):
        items.append({
            'title': item.title,
            'url': item.url,
            'order': item.order,
        })

    # 2. Категории с галочкой show_in_menu
    for cat in Category.objects.filter(show_in_menu=True).order_by('menu_order'):
        items.append({
            'title': cat.name,
            'url': cat.get_absolute_url(),
            'order': cat.menu_order + 1000,  # смещение, чтобы после ручных пунктов (можно настроить)
        })

    # Сортируем общий список по полю 'order'
    items.sort(key=lambda x: x['order'])
    return {'menu_items': items}