from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
@admin.register(User1)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('last_name', 'first_name', 'email')
    list_filter = ('last_name',)
    search_fields = ['last_name', 'first_name', 'email']


class SubcChannel(admin.TabularInline):
    model = SubcChannel
    extra = 1


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('channel_name','rating','type','videos')
    list_filter = ('channel_name',)
    search_fields = ['channel_name','type']

    inlines = (SubcChannel,)

    def channels(self, request):
        channels = []
        for s in SubcChannel.objects.filter(team=request.name):
            channels.append(s)
        return channels


@admin.register(Subc)
class SubcAdmin(admin.ModelAdmin):
    empty_value_display = 'null'

    def user_last_name(self, obj):
        return "{}".format(obj.user)

    inlines = (SubcChannel,)

    list_display = ('id', 'user_last_name', 'date')
    list_filter = ('id',)
    search_fields = ['user_last_name', 'date']



