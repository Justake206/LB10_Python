from django.contrib import admin
from .models import Case, PracticeArea, News  # Добавляем News

class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'title', 'client', 'practice_area', 'status', 'created_at')
    list_filter = ('status', 'practice_area', 'is_confidential')
    search_fields = ('case_number', 'title', 'client')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'category')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)

admin.site.register(PracticeArea, PracticeAreaAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(News, NewsAdmin)  # Регистрируем News