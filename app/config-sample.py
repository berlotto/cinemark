# -*- encoding: utf-8 -*-

# Configuration file

DEBUG = True  # Em producao isto deve ser False

SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

MOIP_TOKEN="bbb"
MOIP_KEY="aaa"
MOIP_RAZAO_PAGAMENTO="Colaboradores - compra de ingresso"

# Digite os cupons sempre em MInusculo
CUPOM_DESCONTO="colaboradores"
CUPOM_FREE="colaboradoresfree#"

# Valor da venda do infresso neste site
VALOR_INGRESSO=9.90
# Valor original dos ingressos vendidos nas bilheterias normais
# para base de cálculo da porcentagem de desconto oferecida
VALOR_ORIGINAL=28

#Simples user e senha para acesso a listagem das vendas
AUTH_USER = "colab"
AUTH_PASSWORD = "secret"

#----------------------------------------------------------------------------
#MAIL_SERVER : default ‘localhost’
#MAIL_PORT : default 25
#MAIL_USE_TLS : default False
#MAIL_USE_SSL : default False
#MAIL_DEBUG : default app.debug
#MAIL_USERNAME : default None
#MAIL_PASSWORD : default None
#MAIL_DEFAULT_SENDER : default None
#MAIL_MAX_EMAILS : default None
#MAIL_SUPPRESS_SEND : default app.testing
#MAIL_ASCII_ATTACHMENTS : default False

MAIL_SENDER = "services@colaboradores.com.br"

#----------------------------------------------------------------------------
#Provavelmente você não necessita alterar estas linhas
MOIP_SANDBOX_URL="https://desenvolvedor.moip.com.br/sandbox"
MOIP_PROD_URL="https://www.moip.com.br"

DATABASE_URL='sqlite:////tmp/test.db'
