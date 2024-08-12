# Movie Lens Django

Movie Lens 20 data importer and movies info listing assignment for PABD course.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Referências do Dataset
Foi utilizado [dataset do MovieLens](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset), um serviço de recomendação de filmes. Nele, os usuários podem recomendar vários filmes, avaliando eles
por de 0 a 5, além de aplicar _tags_ aos filmes. Os arquivos utilizados foram:

**tags.csv**

\- Objetivo: Contém as tags aplicadas pelos usuários aos filmes.

\- Colunas:

* _userId_: Identificador ́unico do usu ́ario.
* _movieId_: Identificador único do filme.
* _tag_: Tag aplicada ao filme.
* _timestamp_: Carimbo de data/hora representando quando a tag foi aplicada (em
segundos desde a meia-noite UTC de 1o de janeiro de 1970).

**movie.csv**

\- Objetivo: Fornece informações básicas sobre os filmes.

\- Colunas:

* _movieId_: Identificador único do filme.
* _title_: Título do filme, incluindo o ano de lançamento entre parênteses.
* _genres_: Lista separada por pipe dos gêneros associados ao filme.

**links.csv**

\- Objetivo: Fornece identificadores externos para os filmes no IMDb e no TMDb, permi-
tindo a conexão com outras bases de dados de filmes.

\- Colunas:

* _movieId_: Identificador único do filme.
* _imdbId_: Identificador do filme no IMDb.
* _tmdbId_: Identificador do filme no TMDb (The Movie Database).

**genome-scores.csv**

\- Objetivo: Contém pontuações de relevância de tags para os filmes, representando como
fortemente um filme exibe as características descritas pelas tags.

\- Colunas:

* _movieId_: Identificador único do filme.
* _tagId_: Identificador único da tag.
* _relevance_: Pontuação de relevância indicando a intensidade com que o filme exibe
a característica representada pela tag (valor entre 0 e 1).

**genome-tags.csv**
\- Objetivo: Fornece as descrições das tags usadas no arquivo genome-scores.csv.

\- Colunas:

* _tagId_: Identificador único da tag.
* _tag_: Descrição textual da tag.

## APIs Utilizadas para Exibir Detalhes Sobre os Filmes
- https://www.omdbapi.com/
- https://www.themoviedb.org/

## Logical diagram of data persistence
![movie lens django drawio](https://github.com/user-attachments/assets/2541df87-1a5b-491e-b59d-0cae22d85c82)

## 
## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy movie_lens_django

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd movie_lens_django
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd movie_lens_django
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd movie_lens_django
celery -A config.celery_app worker -B -l info
```

## Deployment

The following details how to deploy this application.
