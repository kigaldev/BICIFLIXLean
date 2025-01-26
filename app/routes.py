from flask import jsonify, request, abort
import re
from flask_cors import cross_origin
from app import app, db
from app.models import Tasacion
from app.utils.pricing_algorithm import calcular_precio

@app.route('/tasacion', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def crear_tasacion():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()

    # Validaciones
    if not data:
        abort(400, description="No se enviaron datos en la solicitud.")
    
    # Validar el correo electrónico
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
        abort(400, description="Email inválido")
    
    # Validar el año de la bicicleta
    anio = data.get('anio', 0)
    if not isinstance(anio, int) or anio < 2000 or anio > 2024:
        abort(400, description="Año inválido. Debe estar entre 2000 y 2024.")
    
    # Validar otros campos según sea necesario (ejemplo: tipo de bicicleta)
    if not data.get('tipo_bicicleta') or not isinstance(data['tipo_bicicleta'], str):
        abort(400, description="Tipo de bicicleta inválido o faltante.")
    
    # Validar que la transmisión sea uno de los valores esperados
    if data.get('transmision') not in ['Mecánica', 'Electrónica']:
        abort(400, description="Transmisión inválida. Debe ser 'Mecánica' o 'Electrónica'.")
    
    # Crear una nueva tasación
    nueva_tasacion = Tasacion(
        email=data.get('email'),
        tipo_operacion=data.get('tipo_operacion'),
        tipo_bicicleta=data.get('tipo_bicicleta'),
        marca=data.get('marca'),
        modelo=data.get('modelo'),
        anio=anio,
        transmision=data.get('transmision'),
        talla=data.get('talla')
    )
    
    # Calcular el precio estimado
    precio = calcular_precio(data)
    nueva_tasacion.precio_estimado = precio
    
    # Guardar en la base de datos
    db.session.add(nueva_tasacion)
    db.session.commit()
    
    # Responder con el ID y el precio estimado
    return jsonify({
        "id": nueva_tasacion.id, 
        "precio_estimado": precio
    }), 201
