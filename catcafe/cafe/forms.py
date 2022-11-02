from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import OrderDetail, Profile, Comment


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'simple-input',
                                                             'placeholder': 'your username'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'simple-input',
                                                                 'placeholder': 'your password'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'simple-input',
                                                             'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'simple-input',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'class': 'simple-input',
                                                                  'placeholder': 'Repeat password'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'simple-input',
                                                            'placeholder': 'Email'}))
    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(attrs={'class': 'simple-input',
                                                               'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'class': 'simple-input',
                                                              'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "email", "first_name", "last_name")


class ProfileForm(forms.ModelForm):
    ship_address = forms.CharField(label='Default ship address',
                                   widget=forms.TextInput(attrs={'class': 'simple-input',
                                                                 'placeholder': 'Ship address'}))
    image = forms.ImageField(label="Profile avatar")

    class Meta:
        model = Profile
        fields = ('ship_address', 'image')


class CommentForm(forms.ModelForm):
    dish = forms.ChoiceField(choices=[], required=True, )
    mark = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'simple-input', 'min': 1, 'max': 5}),
                              required=True)
    title = forms.CharField(label='Comment title',
                            widget=forms.TextInput(attrs={'class': 'simple-input',
                                                          'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'big-input'}),
                              required=True)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        dishes = self.initial['dish']
        query = OrderDetail.objects.values_list('dish__pk', 'dish__name').filter(dish__in=dishes)
        self.fields['dish'].choices = [q for q in query]
        self.fields['dish'].choices.insert(0, ('', 'Choose dish'))

    class Meta:
        model = Comment
        fields = ('dish', 'mark', 'title', 'content')