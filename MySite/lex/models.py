from django.db import models


class PracticeArea(models.Model):
    """Области юридической практики"""
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название области практики'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание области практики'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область практики'
        verbose_name_plural = 'Области практики'
        ordering = ['name']


class Case(models.Model):
    """Судебные дела/кейсы"""
    title = models.CharField(max_length=200, verbose_name='Название дела')
    case_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер дела'
    )
    client = models.CharField(max_length=200, verbose_name='Клиент')
    content = models.TextField(verbose_name='Описание дела')

    STATUS_CHOICES = [
        ('active', 'Активное'),
        ('closed', 'Закрыто'),
        ('pending', 'На рассмотрении'),
        ('appeal', 'Апелляция'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус дела'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата принятия дела'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    court_documents = models.FileField(
        upload_to='court_docs/%Y/%m/%d/',
        blank=True,
        verbose_name='Судебные документы'
    )

    is_confidential = models.BooleanField(
        default=False,
        verbose_name='Конфиденциальное дело'
    )

    practice_area = models.ForeignKey(
        PracticeArea,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Область практики'
    )

    def __str__(self):
        return f"{self.case_number}: {self.title}"

    # Метод для отображения в шаблоне (для лабораторной работы 6)
    def get_case_info(self):
        """Возвращает краткую информацию о деле"""
        return f"Дело №{self.case_number} - {self.client}"

    # Метод для определения статуса дела (цвет)
    def get_status_color(self):
        """Возвращает цвет статуса для Bootstrap"""
        colors = {
            'active': 'success',
            'closed': 'secondary',
            'pending': 'warning',
            'appeal': 'info',
        }
        return colors.get(self.status, 'secondary')

    class Meta:
        verbose_name = 'Судебное дело'
        verbose_name_plural = 'Судебные дела'
        ordering = ['-created_at']


class News(models.Model):
    """Новости юридической фирмы"""
    title = models.CharField(max_length=200, verbose_name='Заголовок новости')
    content = models.TextField(verbose_name='Содержание новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    # Поле для изображения (добавлено в лабораторной работе 6)
    photo = models.ImageField(
        upload_to='news_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение новости'
    )

    # Связь с PracticeArea
    category = models.ForeignKey(
        PracticeArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория новости'
    )

    def __str__(self):
        return self.title

    # Методы для использования в шаблонах (лабораторная работа 6)
    def get_short_title(self):
        """Метод для получения сокращенного заголовка"""
        if len(self.title) > 30:
            return self.title[:27] + '...'
        return self.title

    def get_news_type(self):
        """Метод для определения типа новости по категории"""
        if self.category:
            return f"Категория: {self.category.name}"
        return "Общие новости"

    def has_photo(self):
        """Проверяет, есть ли у новости изображение"""
        return bool(self.photo)

    def get_content_preview(self, words=50):
        """Возвращает превью контента"""
        words_list = self.content.split()
        if len(words_list) > words:
            return ' '.join(words_list[:words]) + '...'
        return self.content

    def days_since_publication(self):
        """Возвращает количество дней с момента публикации"""
        from django.utils import timezone
        delta = timezone.now() - self.created_at
        return delta.days

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']