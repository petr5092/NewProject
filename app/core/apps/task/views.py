from typing import Any
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models.query import QuerySet
from django.contrib.auth.models import User, AnonymousUser
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from core.apps.task.models import Task, UserTaskLike, UserBookmarks, BrowHistory, Category
from core.apps.task.serializers import TaskCommonSerializer
from core.apps.task.forms import TaskCreate, CategoryCreate, UserCreateForm, UserAuthForm
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib.auth import login, authenticate, logout

class TaskListView(ListView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().prefetch_related('bmarks', "like").select_related('category').all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print(isinstance(self.request.user, AnonymousUser), 111111111111111111111111111)
        context = super().get_context_data(**kwargs)
        if not(isinstance(self.request.user, AnonymousUser)):
            context['like'] = Task.objects.filter(like__user=self.request.user)
            context['bmarks'] = Task.objects.filter(bmarks__user=self.request.user)
        context['title'] = 'Мой заголовок'
        return context


class GetHistory(TaskListView):
    def get_queryset(self) -> QuerySet[Task]:
        if isinstance(self.request.user, AnonymousUser):
            return render(self.request, 'task/auth_user.html', context={'form': UserAuthForm})
        return super().get_queryset().filter(bhistory__user=self.request.user).prefetch_related('bmarks', "like").select_related('category').all()


class FilterLike(TaskListView):
    def get_queryset(self) -> QuerySet[Task]:
        if isinstance(self.request.user, AnonymousUser):
            return render(self.request, 'task/auth_user.html', context={'form': UserAuthForm})
        return super().get_queryset().filter(like__user=self.request.user).prefetch_related('bmarks', "like").select_related('category').all()


class FilterBmarks(TaskListView):
    def get_queryset(self) -> QuerySet[Task]:
        if isinstance(self.request.user, AnonymousUser):
            return render(self.request, 'task/auth_user.html', context={'form': UserAuthForm})
        return super().get_queryset().filter(bmarks__user=self.request.user).prefetch_related('bmarks', "like").select_related('category').all()
    

class AddCat(CreateView):
    model = Category
    form_class = CategoryCreate
    template_name = 'task/create_cat.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('add_cat')


class AddTask(CreateView):
    model = Task
    form_class = TaskCreate
    template_name = 'task/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('add_task')
    

class CreateUser(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'task/user_create.html'

    def get_success_url(self):
        return reverse('main')
    



class FilterCat(TaskListView):
    def get_queryset(self) -> QuerySet[Task]:
        return super().get_queryset().filter(category_id=self.kwargs['cat_id']).prefetch_related('bmarks', "like").select_related('category').all()



class GetTask(DetailView):
    model = Task
    template_name = 'task/task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print(self.get_object().pk)
        if not(isinstance(self.request.user, AnonymousUser)):
            bhistory = BrowHistory(user=self.request.user, task=self.get_object())
            bhistory.save()
        return super().get_context_data(**kwargs)


class AuthUser(TemplateView): 
    form_class = UserAuthForm
    template_name = 'task/auth_user.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('main')
        print(form.errors.as_data(), form.fields)
        return render(request, self.template_name, context={'form': form})


class UserTaskListAPIView(ListAPIView):
    serializer_class = TaskCommonSerializer
    
    def get_queryset(self):
        return Task.objects.all().select_related('category__author', "author").all()



class UserTaskAPIView(RetrieveAPIView):
    serializer_class = TaskCommonSerializer
    def get_queryset(self, *args, **kwargs):
        print(kwargs, args, 2)
        return

def exit(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def add_likes(request, task_id):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'task/auth_user.html', context={'form': UserAuthForm})
    task = Task.objects.get(pk=task_id)
    like = UserTaskLike(user=request.user, task=task)
    like.save()
    task.likes += 1
    task.save()
    print(task.likes)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def del_like(request, task_id):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'task/auth_user.html', context={'form': UserAuthForm})
    task = Task.objects.get(pk=task_id)
    like = UserTaskLike.objects.get(user=request.user, task=task)
    like.delete()
    task.likes -= 1
    task.save()
    print(task.likes)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def add_bookmarks(request, task_id):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'task/auth_user.html', context={'form': UserAuthForm})
    task = Task.objects.get(pk=task_id)
    bmarks = UserBookmarks(user=request.user, task=task)
    bmarks.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def del_bookmarks(request, task_id):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'task/auth_user.html', context={'form': UserAuthForm})
    task = Task.objects.get(pk=task_id)
    bmarks = UserBookmarks.objects.get(user=request.user, task=task)
    bmarks.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])





'''
def index(request):
    print(request.user, 111111111111111111111111111)
    queryset = Task.objects.prefetch_related('bmarks', "like").select_related('category').all()
    queryset2 = Task.objects.filter(like__user=request.user)
    queryset3 = Task.objects.filter(bmarks__user=request.user)
    return render(request, 'task/index.html', {'title': 'Главная страница', 'tasks': queryset, 'like': queryset2, 'bmarks': queryset3})

def get_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    bhistory = BrowHistory(user=request.user, task=task)
    bhistory.save()
    return render(request, 'task/index.html', {'title': task, 'tasks': [task]})

def get_history(request):
    tasks = Task.objects.filter(bhistory__user=request.user)
    tasks.reverse()
    return render(request, 'task/index.html', {'title': 'Главная страница', 'tasks': tasks})


def filter_cat(request, cat_id):
    queryset = Task.objects.filter(category_id=cat_id)
    return render(request, 'task/index.html', {'title': f'Категория №{cat_id}', 'tasks': queryset})


def filter_like(request):
    tasks = Task.objects.filter(like__user=request.user)
    return render(request, 'task/index.html', {'title': 'Главная страница', 'tasks': tasks})




def filter_bmarks(request):
    tasks = Task.objects.filter(bmarks__user=request.user)
    return render(request, 'task/index.html', {'title': 'Главная страница', 'tasks': tasks})




def add_category(request):
    if request.method == "POST":
        form = CategoryCreate(request.POST)
        if form.is_valid():
            new_cat = Category.objects.create(description=form.cleaned_data['description'],
                                              author=request.user)
            new_cat.save()
            return redirect(reverse('add_cat'))
    else:
        form = CategoryCreate()
    return render(request, "task/create_cat.html", {'form': form})

def add_task(request):
    if request.method == "POST":
        form = TaskCreate(request.POST)
        if form.is_valid():
            new_task = Task.objects.create(description=form.cleaned_data['description'],
                                           answer=form.cleaned_data['answer'],
                                           author=request.user,
                                           category=form.cleaned_data['category'])
            new_task.save()
            return redirect(reverse('add_task'))
    else:
        form = TaskCreate()
    return render(request, "task/create.html", {'form': form})'''