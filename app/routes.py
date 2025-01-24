from flask import jsonify, request
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
    
    nueva_tasacion = Tasacion(
        email=data.get('email'),
        tipo_operacion=data.get('tipo_operacion'),
        tipo_bicicleta=data.get('tipo_bicicleta'),
        marca=data.get('marca'),
        modelo=data.get('modelo'),
        anio=data.get('anio'),
        transmision=data.get('transmision'),
        talla=data.get('talla')
    )
    
    precio = calcular_precio(data)
    nueva_tasacion.precio_estimado = precio
    
    db.session.add(nueva_tasacion)
    db.session.commit()
    
    return jsonify({
        "id": nueva_tasacion.id, 
        "precio_estimado": precio
    }), 201