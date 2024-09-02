from rest_framework import serializers
from core.apps.task.models import Task, Category
from django.contrib.auth.models import User


class AuthorCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class CategoryCommonSerializer(serializers.ModelSerializer):
    author = AuthorCommonSerializer()
    class Meta:
        model = Category
        fields = (
            "pk",
            "description",
            "author",
        )



class TaskCommonSerializer(serializers.ModelSerializer):
    category = CategoryCommonSerializer()
    author = AuthorCommonSerializer()
    class Meta:
        model = Task
        fields = (
            "pk",
            "description",
            "answer",
            "category",
            "author"
        )

