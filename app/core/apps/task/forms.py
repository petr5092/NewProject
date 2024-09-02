from typing import Any
from django import forms
from django.contrib.auth.models import User
from core.apps.task.models import Category, Task
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.contrib.auth import login, authenticate, logout

class TaskCreate(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'answer', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,}),
            'answer': forms.TextInput(attrs=({'class':'form-control'})),
            'category':forms.Select(attrs=({'class':'form-control'})),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        print(description, 12345)
        if description == "":
            return self.add_error("description", "а-та-та")
        return description
    
    def clean_answer(self):
        answer = self.cleaned_data.get("answer")
        print(answer, 12345)
        if answer == "":
            return self.add_error("answer", "а-та-та")
        return answer
    
    def clean_author(self):
        author = self.cleaned_data.get("author")
        print(author, 12345)
        if author == "":
            return self.add_error("author", "а-та-та")
        return author
    
    def clean_category(self):
        category = self.cleaned_data.get("category")
        print(category, 1)
        if not(category):
            return self.add_error("category", "а-та-та")
        return category
    
    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-valid"}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-invalid"}
                )
        return super().is_valid()
    



class CategoryCreate(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        print(description, 12345)
        if description == "":
            return self.add_error("description", "а-та-та")
        return description
    
    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-valid"}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-invalid"}
                )
        return super().is_valid()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'rows': 1,}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'rows': 1,}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.Textarea(attrs={'class': 'form-control', 'rows': 1,}),
        }
    
    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-valid"}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-invalid"}
                )
        return super().is_valid()

class UserAuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 1,})
        )
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'rows': 1,}),
    )
    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            print(field)
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-valid"}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-invalid"}
                )
        return super().is_valid()
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == '':
            self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            return self.add_error('username', 'Электронная почта не может быть пустой :(')
        try:
            user = User.objects.get(email=username)
            self.fields['username'].widget.attrs.update({'class': 'form-control is-valid'})
            return username
        except User.DoesNotExist:
            return self.add_error('username', 'Пользователя с таким логином не существует')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if password == '':
            self.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
            raise forms.ValidationError('Пароль не может быть пустым :(')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверный пароль :(')
            else:
                self.fields['password'].widget.attrs.update({'class': 'form-control is-valid'})
                return password
'''
class TaskCreate(forms.Form):
    description = forms.CharField(max_length=10000, widget=forms.Textarea(attrs=
                                                                          {'class': 'form-control', 'rows': 4,}))
    answer = forms.CharField(max_length=100, widget=forms.TextInput(attrs=({'class':'form-control'})))
    author = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.Select(attrs=({'class':'form-control'}))
    )
    likes = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), widget=forms.Select(attrs=({'class':'form-control'}))
    )
'''