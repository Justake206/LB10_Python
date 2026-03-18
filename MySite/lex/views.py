from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Case, PracticeArea, News
from django.core.paginator import Paginator

# Функция get_categories_context УДАЛЕНА!
# Категории теперь получаются через теги в шаблонах (lex_tags.py)

# БАЗОВЫЕ ФУНКЦИИ - ГЛАВНЫЕ СТРАНИЦЫ
def index(request):
    """
    Главная страница приложения lex.
    """
    # Получаем последние 3 опубликованные новости для главной страницы
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]

    # Статистика для карточек на главной
    cases_count = Case.objects.count()
    practice_areas_count = PracticeArea.objects.count()
    news_count = News.objects.filter(is_published=True).count()

    # Создаем контекст - категории больше не передаем!
    context = {
        'latest_news': latest_news,
        'cases_count': cases_count,
        'practice_areas_count': practice_areas_count,
        'news_count': news_count,
        'title': 'Главная страница - Lex',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/index.html', context)


def test(request):
    """
    Простая тестовая страница для проверки работы приложения.
    """
    context = {
        'title': 'Тестовая страница',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/test.html', context)


def about(request):
    """
    Страница "О нас" с информацией о компании.
    """
    context = {
        'title': 'О нас - Юридическая фирма "Lex"',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/about.html', context)


# ФУНКЦИИ ДЛЯ НОВОСТЕЙ
def news_list(request):
    """
    Список всех новостей с пагинацией.
    """
    # Получаем только опубликованные новости, сортируем по дате (новые сверху)
    news_items = News.objects.filter(is_published=True).order_by('-created_at')

    # Пагинация - разбиваем новости на страницы по 6 штук
    paginator = Paginator(news_items, 6)
    page = request.GET.get('page')  # Получаем номер страницы из URL

    try:
        news_page = paginator.page(page)
    except:
        # Если страница не указана или не существует, показываем первую
        news_page = paginator.page(1)

    context = {
        'news_list': news_page,
        'news_count': news_items.count(),
        'title': 'Новости юридической фирмы "Lex"',
        'paginator': paginator,
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/news_list.html', context)


def news_detail(request, news_id):
    """
    Детальная страница отдельной новости.
    """
    news_item = get_object_or_404(News, id=news_id, is_published=True)

    context = {
        'news_item': news_item,
        'title': news_item.title,
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/news_detail.html', context)


# ФУНКЦИЯ ДЛЯ КАТЕГОРИЙ (ЛАБ. РАБОТА №7)
def news_by_category(request, category_id):
    """
    Функция для отображения новостей по категории (области практики).
    """
    # Получаем категорию по ID или возвращаем 404
    category = get_object_or_404(PracticeArea, id=category_id)

    # Получаем новости этой категории (только опубликованные)
    news_items = News.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')

    # Пагинация - 6 новостей на страницу
    paginator = Paginator(news_items, 6)
    page = request.GET.get('page')

    try:
        news_page = paginator.page(page)
    except:
        news_page = paginator.page(1)

    context = {
        'category': category,  # Передаем саму категорию для отображения названия
        'news_list': news_page,
        'news_count': news_items.count(),
        'title': f'Новости: {category.name}',  # Динамический заголовок
        'paginator': paginator,
        'active_category': category.id,  # Для подсветки активной категории в сайдбаре
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/category_news.html', context)


# ФУНКЦИИ ДЛЯ СУДЕБНЫХ ДЕЛ
def case_list(request):
    """
    Список всех судебных дел.
    """
    try:
        has_models = True
        cases = Case.objects.all()
        practice_areas = PracticeArea.objects.all()
    except:
        # Если таблицы еще не созданы, показываем предупреждение
        has_models = False
        cases = []
        practice_areas = []

    context = {
        'has_models': has_models,
        'cases': cases,
        'practice_areas': practice_areas,
        'title': 'Судебные дела',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/case_list.html', context)


def case_detail(request, case_id):
    """
    Детальная информация о конкретном судебном деле.
    """
    case = get_object_or_404(Case, id=case_id)
    context = {
        'case': case,
        'title': f'Дело {case.case_number}',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/case_detail.html', context)


def practice_areas_list(request):
    """
    Список всех областей практики (категорий).
    """
    practice_areas = PracticeArea.objects.all()
    context = {
        'practice_areas': practice_areas,
        'title': 'Области юридической практики',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/practice_areas.html', context)


# ВРЕМЕННЫЕ ФУНКЦИИ (ЗАГОТОВКИ)
def add_case(request):
    """
    Заготовка для формы добавления дела.
    """
    context = {
        'title': 'Добавление дела',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/add_case.html', context)


def edit_case(request, case_id):
    """
    Заготовка для формы редактирования дела.
    """
    context = {
        'title': f'Редактирование дела #{case_id}',
        'case_id': case_id,
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/edit_case.html', context)


def search_cases(request):
    """
    Заготовка для поиска дел.
    """
    context = {
        'title': 'Поиск дел',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/search_cases.html', context)


# API ФУНКЦИИ (ДЛЯ БУДУЩИХ ЛАБОРАТОРНЫХ)
def api_case_list(request):
    """
    Простой API для списка дел.
    """
    return HttpResponse("API: список дел", content_type="application/json")


def api_case_detail(request, case_id):
    """
    Простой API для деталей дела.
    """
    return HttpResponse(f'{{"id": {case_id}}}', content_type="application/json")


# ТЕСТОВЫЕ ФУНКЦИИ ИЗ ЛАБОРАТОРНОЙ 6
def test_bootstrap(request):
    """
    Тестовая страница для проверки компонентов Bootstrap.
    """
    context = {
        'title': 'Тест Bootstrap компонентов',
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/test_bootstrap.html', context)


def test_template_tags(request):
    """
    Тестовая страница для проверки тегов шаблонов.
    """
    news_items = News.objects.filter(is_published=True).order_by('-created_at')[:5]

    context = {
        'title': 'Тест тегов шаблонов',
        'news_items': news_items,
        'test_list': ['Первый', 'Второй', 'Третий', 'Четвертый', 'Пятый'],
        # **get_categories_context() - УДАЛЕНО!
    }
    return render(request, 'lex/test_template_tags.html', context)