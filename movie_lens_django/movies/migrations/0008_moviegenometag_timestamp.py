# Generated by Django 5.0.7 on 2024-08-11 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_movielinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviegenometag',
            name='timestamp',
            field=models.DateTimeField(default='2022-02-02 12:47', verbose_name='Timestamp'),
            preserve_default=False,
        ),
    ]
