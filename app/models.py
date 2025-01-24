from app import db
from datetime import datetime

class Tasacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    tipo_operacion = db.Column(db.String(10), nullable=False)  # "comprar" o "vender"
    tipo_bicicleta = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    transmision = db.Column(db.String(20))
    talla = db.Column(db.String(10))
    precio_estimado = db.Column(db.Float)
    fecha_tasacion = db.Column(db.DateTime, default=datetime.utcnow)