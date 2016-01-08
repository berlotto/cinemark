# -*- encoding: utf-8 -*-
import smtplib
import os
# import codecs

texto_email = u"""
Olá {nome_cliente}

Seus dados foram validados e seu pagamento foi confirmado com sucesso!

Confira abaixo os códigos dos Cupons Super Saver Eletrônico que deverão ser usados no site da Ingresso.com.

{cupons}

Acesse agora o site da ingresso.com, escolha um cinemar, filme e horário para reservar sua sessão com o SUPER SAVER ELETRÔNICO acima.

Lembre-se que este Cupons devem ser utilizados até o dia {prazo_cupons} e servem para filmes 2D de Cinemas Cinemark.

Caso você tenha dúvidas relacionadas à troca dos Cupons Super Saver Eletrónico, clique <a href="https://cinemafacil.com.br/UtilizacaoSuperSaverEletronicosCinemark.pdf">aqui</a>
para acessar o passo-a-passo. Ou envie um e-mail para suporte@colaboradores.com.br.

Atenciosamente,
Equipe Colaboradores
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
