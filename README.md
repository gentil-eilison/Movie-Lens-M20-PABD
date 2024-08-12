# Movie Lens Django

Este projeto consiste em uma aplicação que foi feita exclusivamente para realizar a importação dos dados presentes no _dataset_ do Movie Lens Django. Além de realizar a importação, também foi implementado uma listagem com os filmes disponíveis, contendo diversos filtros os quais o usuário pode utilizar para refinar sua busca. Ao entrar na página de detalhes do filme em específico, serão exibidos dados adicionais vindos de outras APIs, sendo elas a do OMDB e do TMDB.

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

## Diagrama Lógico de Persistência de Dados
![movie lens django drawio](https://github.com/user-attachments/assets/2541df87-1a5b-491e-b59d-0cae22d85c82)

## Visão Funcional do Projeto
![image](https://github.com/user-attachments/assets/11bfce25-e272-4cd3-9020-3f22d5597081)

Nosso projeto é composto por 4 componentes de alto nível: O projeto Django, que irá ser responsável pela aplicação _web_ em si; o Celery _worker_ em conjunto com o Redis como seu _broker_ para processamento de arquivos CSVs maiores; E um banco de dados relacional, sendo ele o PostgreSQL.

É importante mencionar que nem todos os arquivos irão para o Celery. Quando o processamento do arquivo não travar o navegador do usuário, sendo muito rápido para processar, a tarefa não é enviada ao Celery, mas sim ao próprio servidor do Django. O Celery está operando como _worker_ único, ou seja, sem paralelismo de tarefas. Sua utilização foi necessária para que o usuário não tivesse sua requisição travada no navegador ao tentar processar arquivos muito grandes. Ao delegar essa tarefa para o _worker_, o usuário consegue continuar utilizando o site normalmente. 

## Explicação Detalhada e Técnicas Utilizadas

O desenvolvimento do projeto se deu no estilo Kanban. A metodologia ágil utilizada foi a XP Programming, usando a técnica da programação em pares. Além disso, também foi utilizado o GitHub para versionamento do código e o Git para o desenvolvimento de várias _branches_ ao mesmo tempo em alguns momentos. A importação, como já foi explicado, pode ocorrer de duas maneiras: pelo Django, quando o arquivo é pequeno; e pelo Celery, quando é grande.

### Importação pelo Django

Para a importação pelo Django, foi criado a classe base `CSVImportMetaDataForm`, que usa o modelo `CSVImportMetaData`. Ela é definida da seguinte maneira.

![image](https://github.com/user-attachments/assets/7fe5f537-3804-4557-9290-9763b52d81c1)

O formulário possui somente o campo do arquivo nele, pois os outros atributos são metadados que serão preenchidos durante o processamento de dados. A partir dessa classe, foi criado outra, definida assim:

![image](https://github.com/user-attachments/assets/1fdae6a8-5b98-46fa-b5e2-88dc692e0305)

A classe acima sobrescreve o método `save` para que a atualização dos metadados ocorra. Além disso, define também um metódo abstrato -- `add_csv_rows` -- que deverá ser sobrescrito pela classe que herda desta e deverá conter o código de adicionar as tuplas ao banco de dados.

Foi criada uma _view_ no _app core_, que será utilizada para esses formulários. Basta fazer com que a _view_ herde dela e sobrescrever os atributos `form_class` e `template_name`.

![image](https://github.com/user-attachments/assets/8771ea24-db69-4214-add9-d12f646d59e9)

### Importação pelo Celery

Para as importações que travariam o navegador do usuário, foram criadas algumas classes que, em conjunto, realizam o trabalho da importação. A primeira delas foi uma classe abstrata chamada de `ConcurrentImport`, definida da seguinte maneira:

![image](https://github.com/user-attachments/assets/c817d5b6-8e2d-4306-8981-88bf74f9570b)

Nela, um método estático e abstrato é definido. Ele se chama `process_csv_chunk` e irá realizar o processamento do pedaço específico do CSV. Também foi definido outro método estático, chamado `call_import_task`. Como ele está com o _decorator_ `shared_task`, o sistema irá entendê-lo como uma tarefa a ser executada pelo Celery. Ele recebe o nome da subclasse que implementa o método `process_csv_chunk`; o nome do arquivo csv; e o ID da tupla de `CSVImportMetaData` para atualização dos metadados.

O método que serve como tarefa do Celery pega a _string_ passada que representa a subclasse do `ConcurrentImport` e realiza a importação dinâmica dela. Após isso, o pandas é utilizado para a leitura do arquivo em pedaços para que o processamento não trave ou ocupe muito espaço na memória principal. Para cada peçado, o método que os processa é chamado. Esse método deve retornar a quantidade de linhas que deram certo e as que não deram. Após todas as linhas serem processadas, os metadados do CSV são atualizados.

Após isso, também foi criado uma _view_ específica para esse tipo de importação, dentro do _app core_. Ela consiste no seguinte código:

![image](https://github.com/user-attachments/assets/1260d6f1-cc4f-4efa-9f1a-cdd2ceb74140)

Ela sobrescreve o método `form_valid` da `CreateView`, pois só é possível fazer o processamento dos dados depois que o formulário foi enviado com sucesso. É chamado o `form.save` para que a instância do `CSVImportMetaData` seja salva no banco. Após isso, a classe que foi definida no `concurrent_import_class` chamará o seu método `call_import_task` com o `.delay`, delegando a tarefa pro Celery e liberando a _thread_ da requisição do usuário para continuar.

Dentro do método `process_csv_chunk` foram utilizadas algumas técnicas para garantir que o processamento fosse feito da forma mais eficiente possível. As principais diretrizes foram:
1. Utilizar a _lazy creation_ do Django para criar os objetos e depois utilizar o `bulk_create` para inserção em lotes;
2. Evitar validação por meio dos formulários do Django de dados da linha que contenham colunas que fazem referências de chave estrangeira;
3. Caso necessário, utilizar SQL puro para fazer as inserções.

![image](https://github.com/user-attachments/assets/fa38e70e-4ae3-4f14-a751-511ebefa50e1)

A imagem acima é um exemplo do ponto 3. Nela, para verificação de chaves estrangeiras, foi trazido a lista dos ids dos filmes em uma única consulta, convertendo todos eles em um conjunto. O mesmo foi feito para os ids das tags. Não foi utilizado uma lista porque ela é mais lenta que o conjunto para a operação `in` do Python, sendo essa operação utilizada para verificação de colunas de chave estrangeira. Caso as chaves estrangeiras não batessem, uma linha errada é considerada. No fim, executa-se o comando para a inserção. Caso ocorra um `IntegrityError`, nenhuma linha é inserida, fazendo com que a contagem de erros seja igual ao tamanho do pedaço processado. Caso contrário, é possível acessar a quantidade de linhas afetadas pelo comando usando o `cursor.rowcount`. O `ON CONFLICT DO NOTHING` foi utilizado para o caso de duplicação de inserções.

É importante mencionar que em outras inserções, como a de filmes, é necessário criar mais de uma entidade. No de filmes, por exemplo, faz-se necessário criar os gêneros associados ao filme da linha -- caso já não tenham sido criados -- e já associar ao filme, levando a um tempo de processamento a mais.

### Listagem de Filmes e Filtros

A listagem dos filmes, junto com os filtros associados e paginação, foi feita com a biblioteca `django-filter`, junto das _features_ de paginação padrão do Django. Porém, o tempo de carregamento da página estava em torno dos 8s, um tempo inaceitável. Através da utilização da Django Debug Toolbar, foi possível ver, além do tempo de carregamento, quais consultas estavam demorando mais.

![image](https://github.com/user-attachments/assets/77937cb4-c580-4f9a-ae1b-c03e861f6ebf)

![image](https://github.com/user-attachments/assets/e90347e2-877a-4bef-abbb-d0ac7750afce)

Devido a dados resultados de cálculos que eram feitos a partir da tabela `Rating` -- que possui mais de 20 milhões de tuplas --, a listagem de filmes estava sendo um gargalo. A partir disso, criamos um índice no atributo `movie_id` e incluímos o campo `rating` que estava sendo trago na consulta no índice, para que não fosse necessário buscar essa informação na tabela principal, já que o PostgreSQL guarda os índices em uma área separada. O modelo ficou da seguinte maneira:

![image](https://github.com/user-attachments/assets/12d1face-3bd7-4e25-b176-358d52f5c831)

Com isso, os resultados foram os seguintes:

![image](https://github.com/user-attachments/assets/519b5b32-6928-406e-b80f-bbac959e4324)

![image](https://github.com/user-attachments/assets/1c4aa325-99f0-4909-ae51-d1df1f7ca12c)

O carregamento foi reduzido para **200 ms**.

### Página de Detalhe dos Filmes

Ao entrar na página de detalhe, requisições são feitas para os serviços do OMDB e TMDB. Foram criadas duas classes Façade para interação que, por baixo, têm uma implementação simples utilizando a biblioteca `requests` do Python. Com isso, na `DetailView` do filme, duas chaves foram adicionadas ao dicionário do contexto para que as informações estivessem disponíveis no _template_. A _view_ ficou da seguinte forma:

![image](https://github.com/user-attachments/assets/03fd5efa-d6c4-4269-99b7-a8465cc50750)

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
