from django.urls import path
from . import views

# app_name позволяет использовать имена маршрутов с префиксом 'lex:'
# Например: {% url 'lex:news_detail' news.id %}
app_name = 'lex'

urlpatterns = [
    # ОСНОВНЫЕ МАРШРУТЫ
    # Каждый path имеет параметр name для обращения по имени в шаблонах
    path('', views.index, name='index'),  # Главная страница Lex
    path('test/', views.test, name='test'),  # Тестовая страница
    path('about/', views.about, name='about'),  # О нас

    # МАРШРУТЫ ДЛЯ НОВОСТЕЙ (ЛАБОРАТОРНАЯ 7)
    path('news/', views.news_list, name='news_list'),  # Список всех новостей
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),  # Детальная страница новости
    # новый маршрут для фильтрации по категориям
    # <int:category_id> - параметр, который будет передан в view
    path('news/category/<int:category_id>/', views.news_by_category, name='news_by_category'),

    # МАРШРУТЫ ДЛЯ СУДЕБНЫХ ДЕЛ
    path('cases/', views.case_list, name='case_list'),  # Список дел
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),  # Детали дела
    path('practice-areas/', views.practice_areas_list, name='practice_areas_list'),  # Области практики
    path('cases/add/', views.add_case, name='add_case'),  # Добавление дела
    path('cases/<int:case_id>/edit/', views.edit_case, name='edit_case'),  # Редактирование
    path('search/', views.search_cases, name='search_cases'),  # Поиск

    # API МАРШРУТЫ
    path('api/cases/', views.api_case_list, name='api_case_list'),
    path('api/cases/<int:case_id>/', views.api_case_detail, name='api_case_detail'),

    # ТЕСТОВЫЕ МАРШРУТЫ ИЗ ЛАБОРАТОРНОЙ 6
    path('test/bootstrap/', views.test_bootstrap, name='test_bootstrap'),
    path('test/template-tags/', views.test_template_tags, name='test_template_tags'),
]