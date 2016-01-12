# -*- encoding: utf-8 -*-
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

texto_email = u"""
<html><body>
<p>Olá {nome_cliente}</p>

<p>Seus dados foram validados e seu pagamento foi confirmado com sucesso!</p>

<p>Confira abaixo os códigos dos Cupons Super Saver Eletrônico que deverão ser usados no site da Ingresso.com.</p>

<p>
<ul>
{cupons}
</ul>
</p>

<p>Acesse agora o site da ingresso.com, escolha um Cinemark, filme e horário para reservar sua sessão com o SUPER SAVER ELETRÔNICO acima.</p>

<p>Lembre-se que este Cupons devem ser utilizados até o dia {prazo_cupons} e servem para filmes 2D de Cinemas Cinemark.</p>

<p>Caso você tenha dúvidas relacionadas à troca dos Cupons Super Saver Eletrónico, clique <a href="https://cinemafacil.com.br/UtilizacaoSuperSaverEletronicosCinemark.pdf">aqui</a>
para acessar o passo-a-passo. Ou envie um e-mail para suporte@colaboradores.com.br.</p>

<p>
Atenciosamente,<br/>
Equipe Colaboradores
</p>
</body></html>
"""

def dispatch_mail(venda, app):
  dados={
      "nome_cliente": venda.nome_cliente,
      "numero_pedido": venda.id_proprio,
      "quantidade": venda.quantidade,
      "cupons": "<li>"+venda.super_savers.replace(",","<li>"),
      "prazo_cupons": app.config.get("PRAZO_CUPONS")
  }

  mensagem = texto_email.format(**dados)
  part2 = MIMEText(mensagem.encode("UTF-8"), 'html', 'utf-8')

  fromaddr = app.config.get("MAIL_DEFAULT_SENDER")
  toaddrs = venda.email_cliente
  # msg = unicode("\r\n".join([
  #   "From: %s" % fromaddr,
  #   "To: %s" % toaddrs[0],
  #   "Subject: %s" % app.config.get("MAIL_SUBJECT"),
  #   "",
  #   mensagem
  #   ]))

  msg = MIMEMultipart('alternative')
  msg['Subject'] = app.config.get("MAIL_SUBJECT")
  msg['From'] = fromaddr
  msg['To'] = toaddrs
  # msg.attach(part1)
  msg.attach(part2)

  try:
      server = smtplib.SMTP('in-v3.mailjet.com:587')
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login( app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD") )
      server.sendmail(fromaddr, toaddrs, msg.as_string())
      server.quit()
  except Exception, e:
      raise e
