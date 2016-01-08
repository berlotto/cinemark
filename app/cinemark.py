# -*- encoding: utf-8 -*-
#

from flask import Flask, render_template, jsonify, request
from moipy import Moip
from hashlib import md5
from cinemas import CINEMAS
from database import db_session, create, Venda, SuperSaver
from simpleauth import requires_auth
# from flask_mail import Mail, Message
from enviar_email import dispatch_mail
from datetime import datetime as dt
import os

#Temporatio
#from random import choice
#import string

app = Flask(__name__)
app.config.from_object('config')

# mail = Mail(app)

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
@requires_auth
def background():
    total = len(Venda.query.all())
    vendas = Venda.query.filter(Venda.falhou == False).filter(Venda.email_enviado == True).all()
    vendas_falhas = Venda.query.filter(Venda.falhou == True).all()
    vendas_sem_email = Venda.query.filter(Venda.falhou == False).filter(Venda.email_enviado == False).all()
    return render_template(
        "listagem.html",
        vendas=vendas,
        vendas_falhas=vendas_falhas,
        vendas_sem_email=vendas_sem_email,
        total=total,
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
def send_mail(venda):

    agora = dt.now()
    try:
        dispatch_mail(venda,app)
        venda.email_enviado = True
        venda.data_envio = agora.strftime('%d/%m/%Y %H:%M:%S')
    except Exception, e:
        print "Erro ao enviar o email para %s " % venda.email_cliente
        print e
        venda.email_enviado = False

    #Atualiza data de envio na base
    db_session.add(venda)
    db_session.commit()

@app.route("/nasp",methods=("POST",))
def nasp():
    #Este método é chamado pelo MOIP somente enviando dados dos pagamentos
    #que ficaram pendentes
    try:
        dados = request.get_json()
    except Exception, e:
        dados = request.args

    id_transacao = dados.get("id_transacao")
    status_pagamento = dados.get("status_pagamento")

    venda = Venda.query.filter( Venda.id_proprio == id_transacao ).first()
    if not venda:
        print "MOIP enviou aviso para venda %s porem esta não foi encontrada na base!" % id_transacao
    else:
        if status_pagamento in ("Autorizado", "Concluido"):
            print "MOIP avisou pagamento OK para venda %s " % id_transacao
            #Então confirma o pagto e envia os SuperSaver
            retorno = SuperSaver.query.filter(SuperSaver.usado == False).limit(venda.quantidade).all()
            resposta = {
                "codigos": [ s.cupom for s in retorno ]
            }
            #Atualiza os cupons já utilizados
            for ss in retorno:
                ss.usado = True
                db_session.add(ss)
            venda.super_savers = ",".join([ s.cupom for s in retorno ])
            send_mail(venda)
        else:
            #Marca a venda como falha
            classificacao = dados.get("classificacao")
            cod_moip = dados.get("cod_moip")
            print "MOIP avisou pagamento NAO OK (status '%s') para venda %s " % (status_pagamento, id_transacao)
            venda.falhou = True
            venda.token_moip = "NASP: %s, moip_id: %s " % (classificacao,cod_moip)

        db_session.add(venda)
        db_session.commit()

    return "Ok, processado"


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

    send_mail(venda)

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
            'venda' : venda.id,
            'id_proprio': venda.id_proprio,
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
        else:
            moip.set_ambiente("producao")

        moip.set_valor( str(int(dados.get("quantidade")) * app.config.get("VALOR_INGRESSO")) )
        moip.set_data_vencimento('2016-01-20')
        moip.set_id_proprio(venda.id_proprio)
        moip.set_checkout_transparente()
        print "Enviando pagto..."
        moip.envia()
        print "pegando resposta..."
        resposta = moip.get_resposta() # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}
        print "Resposta retornada"
        if resposta['sucesso'] == "Sucesso":
            venda.token_moip = resposta['token']
            create(venda)
        else:
            venda.falhou = True
            venda.token_moip = resposta['token'] # Neste caso vem a mensagem de erro
            create(venda)
        print "Resposta:", resposta
        resposta['dados_retorno'] = dados_retorno
        resposta['tudogratis'] = False
        resposta['venda'] = venda.id
        resposta['id_proprio'] = venda.id_proprio

    return jsonify(resposta)

#============================================================================
if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
