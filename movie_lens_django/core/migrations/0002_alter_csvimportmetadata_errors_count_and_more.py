# Generated by Django 5.0.7 on 2024-07-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvimportmetadata',
            name='errors_count',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Errors Count'),
        ),
        migrations.AlterField(
            model_name='csvimportmetadata',
            name='inserted_data_count',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Inserted Data Count'),
        ),
        migrations.AlterField(
            model_name='csvimportmetadata',
            name='upload_time_in_minutes',
            field=models.PositiveIntegerField(default=0, verbose_name='Upload Time in Minutes'),
        ),
    ]
