# Generated by Django 2.0.5 on 2018-05-07 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_auto_20180507_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
