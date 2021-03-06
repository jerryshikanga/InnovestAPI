# Generated by Django 2.0.5 on 2018-05-06 23:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('picture', models.ImageField(upload_to='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.CharField(max_length=100)),
            ],
        ),
    ]
