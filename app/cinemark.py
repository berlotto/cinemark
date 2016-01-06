# -*- encoding: utf-8 -*-

#

from flask import Flask, render_template, jsonify, request
from moipy import Moip
from hashlib import md5
from cinemas import CINEMAS
from database import db_session, create, Venda, SuperSaver

#Temporatio
from random import choice
import string

app = Flask(__name__)
app.config.from_object('config')

#============================================================================
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#============================================================================
# def get_super_savers(qtd):
#     l = []
#     for nro in range(int(qtd)):
#         uid = ''.join([ choice(string.letters+string.digits) for x in range(6) ])
#         l.append(uid)
#     return l

#============================================================================
@app.route("/background",methods=("GET",))
def background():
    vendas = Venda.query.filter(Venda.falhou == False).all()
    return render_template(
        "listagem.html",
        vendas=vendas
        )

#============================================================================
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

#============================================================================
@app.route("/ss", methods=("POST",))
def ss():

    retorno = SuperSaver.query.filter(SuperSaver.usado == False).limit(request.form.get("q")).all()
    resposta = {
        "codigos": [ s.cupom for s in retorno ]
    }

    #Atualiza os cupons já utilizados
    for ss in retorno:
        ss.usado = True
        db_session.add(ss)

    #Atualiza os tokens utilizados no registro da venda
    venda = Venda.query.get( request.form.get("t") )
    venda.super_savers = ",".join([ s.cupom for s in retorno ])
    db_session.add(venda)

    db_session.commit()

    return jsonify(resposta)

#============================================================================
@app.route("/contact", methods=("POST",))
def contact():

    dados = request.form
    tudogratis = False

    venda = Venda(dados.get("nome"))
    venda.quantidade = dados.get("quantidade")
    venda.telefone_cliente = dados.get("telefone")
    venda.email_cliente = dados.get("email")
    venda.cpf_cliente = dados.get("cpf")
    venda.email_enviado = False
    venda.cupom_usado = dados.get('cupom')
    venda.valor_pago = int(dados.get("quantidade")) * app.config.get("VALOR_INGRESSO")
    create(venda)

    if dados.get("cupom").lower() == app.config.get("CUPOM_FREE"):
        #Aqui não necessita pagar nada e somente retorna ok para a tela
        #de confirmacao dos super-savers
        tudogratis = True
        resposta = {
            "sucesso":'Sucesso',
            'token':'',
            "tudogratis":True,
            'venda' : venda.id
        }

        venda.pagamento = "Free"
        venda.valor_pago = 0
        create(venda)

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
            IdPagador=str(venda.id),
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
        moip.set_id_proprio(venda.id_proprio)
        moip.set_checkout_transparente()
        print "Enviando pagto..."
        moip.envia()
        resposta = moip.get_resposta() # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}
        if resposta['sucesso'] == "Sucesso":
            venda.token_moip = resposta['token']
            create(venda)
        else:
            venda.falhou = True
            create(venda)
        print "Resposta:", resposta
        resposta['dados_retorno'] = dados_retorno
        resposta['tudogratis'] = False
        resposta['venda'] = venda.id

    return jsonify(resposta)

#============================================================================
if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
