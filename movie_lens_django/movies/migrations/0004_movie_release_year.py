# Generated by Django 5.0.7 on 2024-07-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_moviegenometag_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='release_year',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Release Year'),
            preserve_default=False,
        ),
    ]
