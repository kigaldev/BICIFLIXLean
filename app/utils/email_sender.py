from flask_mail import Message
from app import mail, app

def enviar_informe(destinatario, asunto, pdf_path):
    print(f"Intentando enviar email a {destinatario}")
    with app.app_context():
        try:
            msg = Message(
                asunto, 
                sender='tu_email@gmail.com', 
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
            print("Email enviado con éxito")
        except Exception as e:
            print(f"Error al enviar el email: {str(e)}")
            raise