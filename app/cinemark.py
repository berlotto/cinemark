# -*- encoding: utf-8 -*-

#

from flask import Flask, render_template, jsonify
from moipy import Moip

app = Flask(__name__)
app.config.from_object('config')


@app.route("/", methods=("GET",))
def index():
    if app.config.get("DEBUG"):
        MOIP_URL = app.config.get("MOIP_SANDBOX_URL")
    else:
        MOIP_URL = app.config.get("MOIP_PROD_URL")
    return render_template("index.html",MOIP_URL=MOIP_URL)

@app.route("/contact", methods=("POST",))
def contact():

    moip = Moip('Razao do Pagamento')

    #Dados necessários para checkout transparent
    endereco = dict(
        Logradouro='Rua xxxxx',
        Numero='222',
        Bairro='xxxx',
        Cidade='xxxx',
        Estado='xx',
        CEP='xxxxxx',
        TelefoneFixo='xxxxxxxxxx'
    )
    moip.set_pagador(
        Nome='xxxx',
        Email='xxxxxx',
        Apelido='vitalbh',
        IdPagador='x',
        EnderecoCobranca=endereco
    )

    moip.set_credenciais(token='seu_token',key='sua_key')

    if app.config.get("debug"):
        moip.set_ambiente('sandbox')

    moip.set_valor('12345')
    moip.set_data_vencimento('yyyy-mm-dd')
    moip.set_id_proprio('abc123')
    moip.set_checkout_transparent()
    moip.envia()

    resposta = moip.get_resposta() # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}

    return jsonify(resposta)

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
