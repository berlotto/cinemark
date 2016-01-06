# Cinemark
Site de venda de tickets - Colaboradores

## Ambiente de desenvolvimento

    $ mkvirtualenv cinemark
    $ git clone https://github.com/berlotto/cinemark.git
    $ cd cinemark
    $ pip install -r requirements.txt
    $ python app/cinemark.py

## Configurações

As configurações estão em app/config.py, edite-o em seu editor de textos
preferido

- *DEBUG*: Modo debug ou não [True/False]
- *SECRET_KEY*: Chave secreta distinta (ver abaixo como gerar)

### Chave Secreta

Com um simples código vc pode gerar a chave secreta pseudo-randômica para sua
aplicação

    $ python
    >>> import os
    >>> os.urandom(24)

## Banco de dados

Configure em "config.py" a url de conexão ao banco

Depois execute um terminal python simples e os comandos abaixo:

    >>> from app.database import init_db
    >>> init_db()

Feito! O banco de dados estará criado.
