from flask_mail import Message
from app import mail, app

def enviar_informe(destinatario, asunto, pdf_path):
    with app.app_context():
        msg = Message(
            asunto, 
            sender='kikegallegopt@gmail.com', 
            recipients=[destinatario]
        )
        msg.body = 'Informe de tasación de bicicleta adjunto'
        with open(pdf_path, 'rb') as pdf:
            msg.attach(
                'tasacion.pdf', 
                'application/pdf', 
                pdf.read()
            )
        mail.send(msg)