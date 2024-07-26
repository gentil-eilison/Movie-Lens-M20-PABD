# Generated by Django 5.0.7 on 2024-07-26 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0001_initial'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('genres', models.ManyToManyField(to='movies.genre', verbose_name='Genres')),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
            },
        ),
        migrations.CreateModel(
            name='MovieGenomeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField(unique=True, verbose_name='User ID')),
                ('genome_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_genome_tag', to='genome.genometag', verbose_name='Genome Tag')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_genome_tag', to='movies.movie', verbose_name='Movie')),
            ],
            options={
                'verbose_name': 'Movie Genome Tags By User',
                'verbose_name_plural': 'Movie Genome Tags By User',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='genome_tags',
            field=models.ManyToManyField(through='movies.MovieGenomeTag', to='genome.genometag'),
        ),
    ]
