# lex/templatetags/lex_tags.py
from django import template
from lex.models import PracticeArea, News

# Регистрируем модуль тегов
register = template.Library()

# --------------------------------------------
# ПРОСТОЙ ТЕГ (simple_tag)
# --------------------------------------------

@register.simple_tag(name='get_categories')
def get_categories():
    """
    Простой тег, возвращающий список всех категорий.
    Используется когда нужно получить данные для обработки в шаблоне.
    """
    return PracticeArea.objects.all().order_by('name')


@register.simple_tag(name='get_news_count')
def get_news_count():
    """
    Простой тег для получения общего количества новостей.
    """
    return News.objects.filter(is_published=True).count()


# --------------------------------------------
# ТЕГ ВКЛЮЧЕНИЯ (inclusion_tag)
# --------------------------------------------

@register.inclusion_tag('inc/_categories_sidebar.html', name='show_categories')
def show_categories(arg1='Все категории'):
    """
    Тег включения для отображения списка категорий.
    Принимает аргумент arg1 для дополнительной информации.
    Рендерит шаблон inc/_categories_sidebar.html
    """
    categories = PracticeArea.objects.all().order_by('name')
    return {
        'categories': categories,
        'arg1': arg1
    }


@register.inclusion_tag('inc/_latest_news.html', name='show_latest_news')
def show_latest_news(count=3):
    """
    Тег включения для отображения последних новостей.
    Принимает параметр count - сколько новостей показать.
    Рендерит шаблон inc/_latest_news.html
    """
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:count]
    return {'latest_news': latest_news}