# -*- encoding: utf-8 -*-

#

from flask import Flask, render_template, jsonify, request
from moipy import Moip
from hashlib import md5
from cinemas import CINEMAS

#Temporatio
from random import choice
import string

app = Flask(__name__)
app.config.from_object('config')

# Metodo que gerencia os IDs de transcoes conforme necessario
def get_next_trans_id():
    uid = ''.join([ choice(string.letters+string.digits) for x in range(6) ])
    return uid

def get_super_savers(qtd):
    l = []
    for nro in range(int(qtd)):
        uid = ''.join([ choice(string.letters+string.digits) for x in range(6) ])
        l.append(uid)
    return l


@app.route("/", methods=("GET",))
def index():
    if app.config.get("DEBUG"):
        MOIP_URL = app.config.get("MOIP_SANDBOX_URL")
    else:
        MOIP_URL = app.config.get("MOIP_PROD_URL")
    md5_cupom = md5(app.config.get("CUPOM_DESCONTO")).hexdigest()
    md5_free = md5(app.config.get("CUPOM_FREE")).hexdigest()

    desconto_dado = int(round(100-((app.config.get("VALOR_INGRESSO")*100)/app.config.get("VALOR_ORIGINAL")),0))

    return render_template(
        "index.html",
        MOIP_URL=MOIP_URL,config=app.config,
        cupom_desconto=md5_cupom, cupom_free=md5_free,
        valor_ingresso=app.config.get("VALOR_INGRESSO"),
        valor_desconto=desconto_dado,
        cinemas=CINEMAS)

@app.route("/ss", methods=("POST",))
def ss():
    resposta = {
        "codigos":get_super_savers(request.form.get("q"))
    }
    return jsonify(resposta)

@app.route("/contact", methods=("POST",))
def contact():

    dados = request.form
    tudogratis = False

    if dados.get("cupom").lower() == app.config.get("CUPOM_FREE"):
        #Aqui não necessita pagar nada e somente retorna ok para a tela
        #de confirmacao dos super-savers
        tudogratis = True
        resposta = {
            "sucesso":'Sucesso',
            'token':'',
            "tudogratis":True
        }
    else:

        moip = Moip(app.config.get("MOIP_RAZAO_PAGAMENTO"))

        #Dados necessários para checkout transparent
        endereco = dict(
            Logradouro=dados.get("rua"),
            Numero=dados.get("nro"),
            Complemento=dados.get("complemento"),
            Bairro=dados.get("bairro"),
            Cidade=dados.get("cidade"),
            Estado=dados.get("uf"),
            CEP=dados.get("cep"),
            TelefoneFixo=dados.get("telefone")
        )
        moip.set_pagador(
            Nome=dados.get("nome"),
            Email=dados.get("email"),
            # Apelido='vitalbh',
            IdPagador='CLI_003',
            EnderecoCobranca=endereco
        )

        dados_retorno = {
            "Forma": "CartaoCredito",
            "Instituicao": dados.get("cardtype"),
            "Parcelas": "1",
            "CartaoCredito": {
                "Numero": dados.get("nrocartao"),
                "Expiracao": dados.get("data_expiracao"),
                "CodigoSeguranca": dados.get("cod_seguranca"),
                "Portador": {
                    "Nome": dados.get("nome_cartao"),
                    "DataNascimento": dados.get("data_nascimento"),
                    "Telefone": dados.get("telefone"),
                    "Identidade": dados.get("cpf")
                }
            }
        }

        moip.set_credenciais(token=app.config.get("MOIP_TOKEN"),key=app.config.get("MOIP_KEY"))

        if app.config.get("DEBUG"):
            moip.set_ambiente('sandbox')

        moip.set_valor( str(int(dados.get("quantidade")) * app.config.get("VALOR_INGRESSO")) )
        moip.set_data_vencimento('2016-01-20')
        moip.set_id_proprio(get_next_trans_id())
        moip.set_checkout_transparente()
        print "Enviando pagto..."
        moip.envia()
        resposta = moip.get_resposta() # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}
        print "Resposta:", resposta
        resposta['dados_retorno'] = dados_retorno
        resposta['tudogratis'] = False

    return jsonify(resposta)

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
