# Generated by Django 3.2 on 2021-05-11 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='for_anonymous_users',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='favorites',
            name='in_order',
            field=models.BooleanField(default=True),
        ),
    ]
