from django.contrib import admin

from core.apps.task.models import Task, Category, UserTaskLike, UserBookmarks, BrowHistory
# Register your models here.
@admin.register(Task, Category)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author')

    
@admin.register(UserTaskLike)
class User(admin.ModelAdmin):
    list_display = ('pk', "user")

@admin.register(UserBookmarks)
class User(admin.ModelAdmin):
    list_display = ('pk', "user")

@admin.register(BrowHistory)
class User(admin.ModelAdmin):
    list_display = ('pk', "user")