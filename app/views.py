from django.db.models import SET
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, DetailView
from .models import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    user = request.user
    par = {
        'header': 'Main page',
        'user': user

    }
    return render(request, 'MainPage.html', context=par)


class ChannelForm(forms.ModelForm):
    class Meta(object):
        model = Channel
        fields = ['channel_name', 'rating', 'type', 'videos', 'picture', 'ChannelId']

    def save(self):
        channel = Channel()
        channel.channel_name = self.cleaned_data.get('name')
        channel.rating = self.cleaned_data.get('price')
        channel.type = self.cleaned_data.get('type')
        channel.videos = self.cleaned_data.get('quantity')
        picture = self.cleaned_data.get('picture')
        channel.picture = picture
        channel.save()


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Повторите ввод')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Email')


def registration_1(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False
        if is_val:
            new_user = User.objects.create_user(data['username'], data['email'], data['password'])
            print(new_user)
            user1 = User1()
            user1.user1 = new_user
            user1.email = data['email']
            user1.last_name = data['last_name']
            user1.first_name = data['first_name']
            user1.save()
            return HttpResponseRedirect('/login1')
        else:
            form = RegistrationForm()
    return render(request, 'registration_1.html', {'form': form})


def registration_form(request):
    errors = {}
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        if not last_name:
            errors['last_name'] = 'Введите Фамилию'

        first_name = request.POST.get('first_name')
        if not first_name:
            errors['first_name'] = 'Введите имя'

        email = request.POST.get('Email')
        if not email:
            errors['Email'] = 'Введите Email'

        username = request.POST.get('username')
        if not username:
            errors['username'] = 'Введите логин'
        elif len(username) < 8:
            errors['username'] = 'Логин должен превышать 5 символов'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Данный логин занят'

        password = request.POST.get('password')
        if not password:
            errors['password'] = 'Введите пароль'
        elif len(password) < 8:
            errors['password'] = 'Длина пароля должна превышать 6 символов'
        password_repeat = request.POST.get('password2')
        if password != password_repeat:
            errors['password_repeat'] = 'Пароли должны совпадать'
        print(username, password, "1")

        if not errors:
            new_user = User.objects.create_user(username, email, password)
            print(new_user)
            user1 = User1()
            user1.user1 = new_user
            user1.email = email
            user1.last_name = last_name
            user1.first_name = first_name
            user1.save()
            return HttpResponseRedirect('/login2')
        else:
            context = {'errors': errors, 'username': username, 'email': email, 'last_name': last_name,
                       'first_name': first_name, 'password': password, 'password_repeat': password_repeat}
            return render(request, 'registration.html', context)
    return render(request, 'registration.html', {'errors': errors})


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


def log_in(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            errors['username'] = 'Введите логин'
        elif len(username) < 5:
            errors['username'] = 'Слишком короткий логин. Минимальная длина-5 знаков'

        password = request.POST.get('password')
        if not password:
            errors['password'] = 'Введите пароль'
        elif len(password) < 8:
            errors['password'] = 'Слишком короткий пароль. Минимальная длина-8 знаков'

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None and 'username' not in errors.keys() and 'password' not in errors.keys():
            errors['login'] = 'Логин или пароль введены неверно'

        if not errors:
            login(request, user)
            return HttpResponseRedirect('/channels')
        else:
            context = {'errors': errors}
            return render(request, 'UserLogin.html', context)
    return render(request, 'UserLogin.html', {'errors':errors})


def log_in1(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        data = form.cleaned_data

        if form.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])
            print(len(data['username']), len(data['password']))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/channels')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
    else:
        form = LoginForm()
    return render(request, 'UserLogin_1.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'MainPage.html')


@login_required(login_url='/login2')
def logged_in(request):
    return render(request, 'items.html')


def logged_in_view(request):
    if request.user.is_authenticated:
        return render(request, 'items.html')
    else:
        return HttpResponseRedirect('/login1')


def new_channel(request):
    errors = {}
    if request.method == 'POST':
        channel_name = request.POST.get('channel_name')
        if not channel_name:
            errors['channel_name'] = 'Введите Название Канала'
        if Channel.objects.filter(channel_name=channel_name).exists():
            errors['channel_name'] = 'Данный канал уже существует'

        rating = request.POST.get('rating')
        if not rating:
            errors['rating'] = 'Введите рейтинг'
        if Channel.objects.filter(rating=rating).exists():
            errors['rating'] = 'Команда с таким значением рейтинга уже существует'

        type = request.POST.get('type')
        if not type:
            errors['type'] = 'Введите тип канала'

        videos = request.POST.get('videos')
        if not videos:
            errors['videos'] = 'Введите кол-во видео канала'

        picture = request.FILES.get('picture')
        if not picture:
            errors['picture'] = 'Загрузите фото'
        if not errors:
            channel = Channel(channel_name=channel_name, rating=rating, type=type, videos=videos,
                        picture=picture)
            channel.save()
            ChannelId = channel.ChannelId
            return HttpResponseRedirect('/channel/' + str(ChannelId))
        else:
            context = {'errors': errors, 'channel_name': channel_name, 'rating': rating, 'type': type,
                       'videos': videos, 'picture': picture}

    return render(request, 'new_item.html', locals())


class ChannelsView(View):
    def get(self, request):
        dict_users = {}
        channels = Channel.objects.all()
        channels1 = Channel.objects.all()
        form = ChannelForm()
        paginator = Paginator(channels, 4)
        page = request.GET.get('page')
        try:
            channels = paginator.page(page)
        except PageNotAnInteger:
            channels = paginator.page(1)
        except EmptyPage:
            channels = paginator.page(paginator.num_pages)
        return render(request, 'items.html', context={'channels': channels, 'users': dict_users, 'form': form,
                                                      'channels1': channels1})


class ChannelObject(DetailView):
    model = Channel
    context_object_name = 'ChannelObject'
    template_name = 'obj.html'


def new_subscriber(request, channel):
    errors = {}
    if request.method == 'POST':


        subc = Subc()
        uid = request.user.id
        user = User.objects.get(id=uid)
        subc.user = user
        subc_id = subc.id
        if Channel.objects.filter(subc__user=user).exists():
            errors['username'] = 'Вы уже подписанны на данный канал'
        channel1 = Channel.objects.get(ChannelId=int(channel))
        date = datetime.today()
        subc.date = date
        if not errors:
            subc.save()
            subc2 = SubcChannel()
            subc2.channel_id = channel1.ChannelId
            subc2.id = subc_id
            subc2.subc_id = subc.id
            subc2.user_id = uid
            subc2.save()
            return HttpResponseRedirect('/channel/'+str(channel1.ChannelId)+'/')
        else:
            context = {'errors': errors, 'username': user}

    return render(request, 'new_bet.html', locals())


def subcribers_users(request, channel):
    subcribers = []
    channel1 = Channel.objects.get(ChannelId=int(channel))
    users = User1.objects.all()
    subc3 = []
    subc = SubcChannel.objects.filter(channel_id=channel1.ChannelId).all()
    for b in subc:
        subc1 = Subc.objects.filter(id=b.subc_id).all()
        if len(subc1) != 0:
            subc3.append(b.id)
    for i in subc3:
        subcribers.append(Subc.objects.get(id=i))
    return render(request, 'bets.html', context={"subcribers": subcribers, "users": users, 'channel': channel})
