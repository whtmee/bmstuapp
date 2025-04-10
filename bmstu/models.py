from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    subject_title = models.CharField(max_length=50, verbose_name='Название предмета')
    
    def __str__(self):
        return self.subject_title
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

class Homework(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено'),
        ('revision', 'На доработке'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='Название работы')
    description = models.TextField(max_length=50,verbose_name='Описание')
    file = models.FileField(upload_to='homeworks/', verbose_name='Файл с работой')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    
    def __str__(self):
        return f"{self.student.username} - {self.subject.subject_title} - {self.title}"
    
    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

class Lecture(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='Название лекции')
    description = models.TextField(max_length=50,verbose_name='Описание')
    file = models.FileField(upload_to='lectures/', verbose_name='Файл лекции')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    
    def __str__(self):
        return f"{self.author.username} - {self.subject.subject_title} - {self.title}"
    
    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='balance')
    coins = models.IntegerField(default=0, verbose_name='Баланс')
    
    def __str__(self):
        return f"Баланс пользователя {self.user.username}: {self.coins}"
    
    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
    


