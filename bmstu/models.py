from django.db import models
from users.models import UserProfile
from django.db.models import Count, Q

class Subject(models.Model):
    subject_title = models.CharField(max_length=50, verbose_name='Название предмета')
    
    def __str__(self):
        return self.subject_title
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

class Vote(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь')
    homework = models.ForeignKey('Homework', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Домашняя работа')
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Лекция')
    is_like = models.BooleanField(verbose_name='Лайк')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = [('user', 'homework'), ('user', 'lecture')]

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
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Студент')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    
    def update_status(self):
        likes = Vote.objects.filter(homework=self, is_like=True).count()
        dislikes = Vote.objects.filter(homework=self, is_like=False).count()

        if likes == 0 and dislikes == 0:
            self.status = 'pending'
        elif dislikes > likes and dislikes - likes >= 2:
            self.status = 'rejected'
        elif likes > dislikes and likes - dislikes >= 2:
            self.status = 'approved'
        else:
            self.status = 'revision'

        self.save()
        self.update_balance()

    def update_balance(self):
        from bmstu.models import Balance
        balance, created = Balance.objects.get_or_create(user=self.student)
        
        if self.status == 'approved':
            balance.coins += 10
        elif self.status == 'revision':
            balance.coins += 5
        elif self.status == 'rejected':
            balance.coins -= 1
        
        balance.save()

    def get_votes_count(self):
        likes = Vote.objects.filter(homework=self, is_like=True).count()
        dislikes = Vote.objects.filter(homework=self, is_like=False).count()
        return {'likes': likes, 'dislikes': dislikes}
    
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
        ('revision', 'На доработке'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='Название лекции')
    description = models.TextField(max_length=50,verbose_name='Описание')
    file = models.FileField(upload_to='lectures/', verbose_name='Файл лекции')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Автор')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    
    def update_status(self):
        likes = Vote.objects.filter(lecture=self, is_like=True).count()
        dislikes = Vote.objects.filter(lecture=self, is_like=False).count()

        if likes == 0 and dislikes == 0:
            self.status = 'pending'
        elif dislikes > likes and dislikes - likes >= 2:
            self.status = 'rejected'
        elif likes > dislikes and likes - dislikes >= 2:
            self.status = 'approved'
        else:
            self.status = 'revision'

        self.save()
        self.update_balance()

    def update_balance(self):
        from bmstu.models import Balance
        balance, created = Balance.objects.get_or_create(user=self.author)
        
        if self.status == 'approved':
            balance.coins += 10
        elif self.status == 'revision':
            balance.coins += 5
        elif self.status == 'rejected':
            balance.coins -= 1
        
        balance.save()

    def get_votes_count(self):
        likes = Vote.objects.filter(lecture=self, is_like=True).count()
        dislikes = Vote.objects.filter(lecture=self, is_like=False).count()
        return {'likes': likes, 'dislikes': dislikes}
    
    def __str__(self):
        return f"{self.author.username} - {self.subject.subject_title} - {self.title}"
    
    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        
class Balance(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='balance')
    coins = models.IntegerField(default=0, verbose_name='Баланс')
    
    def __str__(self):
        return f"Баланс пользователя {self.user.username}: {self.coins}"
    
    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
    
def update_user_balance(user):
    
    balance, created = Balance.objects.get_or_create(user=user)
    homeworks = Homework.objects.filter(student=user)
    lectures = Lecture.objects.filter(author=user)
    
    total_coins = 0
    for homework in homeworks:
        if homework.status == 'approved':
            total_coins += 10
        elif homework.status == 'revision':
            total_coins += 5
        elif homework.status == 'rejected':
            total_coins -= 1
            
    for lecture in lectures:
        if lecture.status == 'approved':
            total_coins += 10
        elif lecture.status == 'revision':
            total_coins += 5
        elif lecture.status == 'rejected':
            total_coins -= 1
    
    if user.username == 'admin':
        total_coins = 999999
        
    balance.coins = total_coins
    balance.save()
    return balance


