# Generated by Django 2.0 on 2018-01-18 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('ChannelId', models.AutoField(primary_key=True, serialize=False)),
                ('channel_name', models.CharField(max_length=30, null=True, unique=True)),
                ('rating', models.PositiveSmallIntegerField(null=True, unique=True)),
                ('type', models.CharField(max_length=30, null=True)),
                ('videos', models.PositiveSmallIntegerField(null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pics/')),
            ],
        ),
        migrations.CreateModel(
            name='Subc',
            fields=[
                ('date', models.DateField()),
                ('amount', models.FloatField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SubcChannel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Channel')),
                ('subc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Subc')),
            ],
        ),
        migrations.CreateModel(
            name='User1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('phone', models.PositiveIntegerField(null=True, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('passport', models.PositiveIntegerField(null=True, unique=True)),
                ('user1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subc',
            name='channel',
            field=models.ManyToManyField(through='app.SubcChannel', to='app.Channel'),
        ),
        migrations.AddField(
            model_name='subc',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
