from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User1(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    phone = models.PositiveIntegerField(unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    birthday = models.DateField(blank=True, null=True)
    passport = models.PositiveIntegerField(unique=True, null=True)

    def __str__(self):
        return str(self.last_name)


class Channel(models.Model):
    ChannelId = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=30, unique=True, null=True)
    rating = models.PositiveSmallIntegerField(null=True, unique=True)
    type = models.CharField(max_length=30, null=True)
    videos = models.PositiveSmallIntegerField(null=True)
    picture = models.ImageField(upload_to='pics/', null=True, blank=True)

    def __str__(self):
        return str(self.channel_name)


class Subc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ManyToManyField(Channel, through="SubcChannel")
    date = models.DateField()
    amount = models.FloatField(null=True)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.id)


class SubcChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    subc = models.ForeignKey(Subc, on_delete=models.CASCADE)
    id = models.AutoField( primary_key=True)
    def __str__(self):
        return str(self.id)