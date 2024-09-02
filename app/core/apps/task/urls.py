from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.apps.task.views import add_likes, del_like, add_bookmarks, del_bookmarks, exit
from core.apps.task.views import GetHistory, AddTask, AddTask, AddCat, FilterLike, FilterBmarks, TaskListView, FilterCat, GetTask, CreateUser, AuthUser, UserTaskListAPIView, UserTaskAPIView


urlpatterns = [
    path('', TaskListView.as_view(), name='main'),
    path('tasks/<int:task_id>/', GetTask.as_view()),
    path('cat/<int:cat_id>/', FilterCat.as_view()),
    path('likes/<int:task_id>/', add_likes),
    path('like/<int:task_id>/', del_like),
    path('liked/', FilterLike.as_view()),
    path('bmarks/<int:task_id>/', add_bookmarks),
    path('bmark/<int:task_id>/', del_bookmarks),
    path('bookmarks/', FilterBmarks.as_view()),
    path('history/', GetHistory.as_view()),
    path('add_task/', AddTask.as_view(), name='add_task'),
    path('add_cat/', AddCat.as_view(), name='add_cat'),
    path('all/', TaskListView.as_view()),
    path('reg/', CreateUser.as_view(), name='reg'),
    path('auth/', AuthUser.as_view(), name='auth'),
    path('exit/', exit),
    path("api/tasks/", UserTaskListAPIView.as_view()),
    path("api/tasks/<int:task_id>/", UserTaskAPIView.as_view())
] + debug_toolbar_urls()
