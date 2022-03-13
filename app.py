import os

from flask import Flask, render_template, request
from flask_cors import CORS

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask('MascEmailService')
CORS(app)


@app.route("/")
def index():
   return render_template('index.html')


@app.route("/enviar", methods=['POST'])
def Enviar_email():
   dominio = 'smtp.gmail.com'
   porta = 587
   usuario = 'mascemailservice@gmail.com'
   senha = '*******************'

   servidor = smtplib.SMTP(dominio, porta)

   servidor.ehlo()
   servidor.starttls()
   servidor.login(usuario, senha)

   dados = request.get_json()

   email_msg = MIMEMultipart()
   email_msg['From'] = usuario
   email_msg['To'] = dados["para"]
   email_msg['Subject'] = dados["assunto"]

   email_msg.attach(MIMEText(dados["mensagem"], 'plain'))

   servidor.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
   servidor.quit()

   return "E-mail enviado com sucesso!"


if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
   app.run(debug=True, port=port)
