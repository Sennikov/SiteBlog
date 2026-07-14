from django.contrib import admin
from .models import Category, Article, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'show_in_menu', 'menu_order']
    list_editable = ['show_in_menu', 'menu_order']
    fieldsets = (
    ('Основное', {'fields': ('name', 'slug', 'description')}),
    ('Меню', {'fields': ('show_in_menu', 'menu_order')}),
    ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'pub_date', 'is_published']
    list_filter = ['category', 'is_published', 'pub_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'author', 'category',
                                 'image', 'content', 'is_published')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']