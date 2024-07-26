# Generated by Django 5.0.7 on 2024-07-26 19:09

import django.db.models.deletion
import movie_lens_django.genome.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0001_initial'),
        ('movies', '0002_movie_moviegenometag_movie_genome_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevance', models.FloatField(validators=[movie_lens_django.genome.validators.validate_positive], verbose_name='Relevance')),
                ('genome_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genome.genometag', verbose_name='Genome Tag')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie', verbose_name='Movie')),
            ],
            options={
                'verbose_name': 'Genome Score',
                'verbose_name_plural': 'Genome Scores',
            },
        ),
        migrations.AddConstraint(
            model_name='genomescore',
            constraint=models.UniqueConstraint(fields=('movie', 'genome_tag'), name='genome_score_movie_genome_tag_unique_together'),
        ),
    ]
