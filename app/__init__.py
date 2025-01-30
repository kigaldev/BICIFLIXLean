import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail  # Importar Flask-Mail

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'biciflix.db')

app = Flask(__name__)

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Asegurar que el directorio database exista
os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)

# Configuración de CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kikegallegopt@gmail.com'  # Cambia esto a tu dirección de correo
app.config['MAIL_PASSWORD'] = 'xuxj ffpw bpug fyxn'   # Cambia esto a tu contraseña o clave de aplicación
app.config['MAIL_DEFAULT_SENDER'] = 'kikegallegopt@gmail.com'
app.config['MAIL_DEFAULT_CHARSET'] = 'utf-8'


# Inicializar extensiones
db = SQLAlchemy(app)
mail = Mail(app)  # Inicializar Flask-Mail

from app import routes, models
