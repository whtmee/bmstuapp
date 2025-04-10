from django.contrib import admin
from bmstu.models import Subject, Homework, Lecture, Balance

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_title',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'student', 'uploaded_at', 'status')
    list_filter = ('status', 'subject', 'uploaded_at')
    search_fields = ('title', 'description', 'student__username', 'subject__subject_title')
    readonly_fields = ('uploaded_at',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('status',)
        return self.readonly_fields

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'author', 'uploaded_at', 'status')
    list_filter = ('status', 'subject', 'uploaded_at')
    search_fields = ('title', 'description', 'author__username', 'subject__subject_title')
    readonly_fields = ('uploaded_at',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('status',)
        return self.readonly_fields
    
@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins')
