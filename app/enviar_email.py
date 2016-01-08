# -*- encoding: utf-8 -*-
import smtplib
import os
# import codecs

texto_email = u"""
Olá {nome_cliente}!

Confirmado o pagamento para o pedido de número {numero_pedido}  com  {quantidade} cupons.

Segue seus cupons SUPER SAVER ELETRÔNICO:

{cupons}

Agora basta acessar o site www.ingresso.com e reservar sua sessão em qualquer Sala Cinemark 2D.

Lembre-se que o cupons devem ser utilizados até {prazo_cupons} .

Se tiver dúvidas em como utilizar os cupons, clique aqui para ver o procedimento de troca do ingresso.

Bom divertimento! =)
"""

def dispatch_mail(venda, app):


    dados={
        "nome_cliente": venda.nome_cliente,
        "numero_pedido": venda.id_proprio,
        "quantidade": venda.quantidade,
        "cupons": venda.super_savers.replace(",","\n"),
        "prazo_cupons": app.config.get("PRAZO_CUPONS")
    }
    # text_file = codecs.open(os.path.dirname(os.path.realpath(__file__))+"/texto-email.txt", "r", "utf-8")
    # mensagem = text_file.read().format(**dados)
    mensagem = texto_email.format(**dados)
    fromaddr = app.config.get("MAIL_DEFAULT_SENDER")
    toaddrs = [venda.email_cliente]
    msg = unicode("\r\n".join([
      "From: %s" % fromaddr,
      "To: %s" % toaddrs[0],
      "Subject: %s" % app.config.get("MAIL_SUBJECT"),
      "",
      mensagem
      ]))

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login( app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD") )
        server.sendmail(fromaddr, toaddrs, msg.encode("utf-8"))
        server.quit()
    except Exception, e:
        raise e
