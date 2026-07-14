from django.db import models
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.urls import reverse

class SEOModel(models.Model):
    """Абстрактная модель для SEO-полей."""
    meta_title = models.CharField('Мета-заголовок', max_length=200, blank=True,
                                  help_text='Оставьте пустым для автоматической генерации')
    meta_description = models.TextField('Мета-описание', blank=True,
                                        help_text='Оставьте пустым для автогенерации')
    meta_keywords = models.CharField('Ключевые слова', max_length=300, blank=True)

    class Meta:
        abstract = True

class Category(SEOModel):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('URL-фрагмент', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    show_in_menu = models.BooleanField('Показывать в меню', default=False,
                                       help_text='Отметьте, чтобы категория автоматически появилась в меню')
    menu_order = models.PositiveIntegerField('Порядок в меню', default=0,
                                         help_text='Чем меньше число, тем выше позиция')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            # Используем описание категории или фразу с названием
            base = self.description if self.description else f'Статьи из категории «{self.name}»'
            self.meta_description = Truncator(strip_tags(base)).chars(160)
        super().save(*args, **kwargs)

class Article(SEOModel):
    title = models.CharField('Заголовок', max_length=250)
    slug = models.SlugField('URL-фрагмент', max_length=250, unique_for_date='pub_date')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='articles', verbose_name='Категория')
    image = models.ImageField('Изображение', upload_to='articles/%Y/%m/', blank=True, null=True)
    content = models.TextField('Содержание')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.pub_date.year,
                                                    self.pub_date.month,
                                                    self.pub_date.day,
                                                    self.slug])

    def save(self, *args, **kwargs):
        # Автоматическая генерация мета-заголовка
        if not self.meta_title:
            self.meta_title = self.title
        # Автоматическая генерация мета-описания из текста статьи
        if not self.meta_description:
            plain_text = strip_tags(self.content)
            self.meta_description = Truncator(plain_text).chars(160)
        super().save(*args, **kwargs)

class MenuItem(models.Model):
    """Пункты меню, редактируемые из админки."""
    title = models.CharField('Название', max_length=100)
    url = models.CharField('URL-адрес', max_length=250, blank=True,
                           help_text='Оставьте пустым, если это выпадающее меню без ссылки')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self):
        return self.title