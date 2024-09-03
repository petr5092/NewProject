from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=100, verbose_name="Категория")

    author = models.ForeignKey(
        User,
        related_name="Category",
        verbose_name="Автор",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "Category"

    def __str__(self):
        return f"Категория №{self.pk}"


class Task(models.Model):
    description = models.TextField(max_length=10000, verbose_name="Условие задачи")
    answer = models.CharField(max_length=100, verbose_name="Ответ")
    category = models.ForeignKey(
        Category,
        related_name="tasks",
        verbose_name="Категория",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        User,
        related_name="tasks",
        verbose_name="Автор",
        on_delete=models.PROTECT,
    )
    likes = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        db_table = "tasks"

    def __str__(self):
        return f"Задача №{self.pk}"


class UserTaskLike(models.Model):
    user = models.ForeignKey(
        User,
        related_name="like",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
    )
    task = models.ForeignKey(
        Task,
        related_name="like",
        verbose_name="Задача",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = (
            "task",
            "user",
        )


class UserBookmarks(models.Model):
    user = models.ForeignKey(
        User,
        related_name="bmarks",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
    )
    task = models.ForeignKey(
        Task,
        related_name="bmarks",
        verbose_name="Задача",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"
        unique_together = (
            "task",
            "user",
        )


class BrowHistory(models.Model):
    user = models.ForeignKey(
        User,
        related_name="bhistory",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
    )
    task = models.ForeignKey(
        Task,
        related_name="bhistory",
        verbose_name="Задача",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "История просмотров"
        verbose_name_plural = "Истории просмотров"
        unique_together = (
            "task",
            "user",
        )
