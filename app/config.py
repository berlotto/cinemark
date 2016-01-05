# -*- encoding: utf-8 -*-

# Configuration file

DEBUG = True  # Em producao isto deve ser False

SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

MOIP_RAZAO_PAGAMENTO="Colaboradores - compra de ingresso"
MOIP_SANDBOX_URL="https://desenvolvedor.moip.com.br/sandbox"
MOIP_PROD_URL="https://www.moip.com.br"

# Digite os cupons sempre em MInusculo
CUPOM_DESCONTO="colaboradores"
CUPOM_FREE="colaboradoresfree#"

# Valor da venda do infresso neste site
VALOR_INGRESSO=9.90
# Valor original dos ingressos vendidos nas bilheterias normais
# para base de cálculo da porcentagem de desconto oferecida
VALOR_ORIGINAL=28
