from flask import jsonify, request, abort
import re
from flask_cors import cross_origin
from app import app, db
from app.models import Tasacion
from app.utils.pricing_algorithm import calcular_precio
from app.utils.pdf_generator import generar_informe_tasacion  # Importar la función para generar PDFs
from app.utils.email_sender import enviar_informe  # Importar la función para enviar correos

@app.route('/tasacion', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def crear_tasacion():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()

    # Validaciones
    if not data:
        abort(400, description="No se enviaron datos en la solicitud.")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
        abort(400, description="Email inválido")
    
    anio = data.get('anio', 0)
    if not isinstance(anio, int) or anio < 2000 or anio > 2024:
        abort(400, description="Año inválido. Debe estar entre 2000 y 2024.")
    
    if not data.get('tipo_bicicleta') or not isinstance(data['tipo_bicicleta'], str):
        abort(400, description="Tipo de bicicleta inválido o faltante.")
    
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

    # Generar PDF después de crear la tasación
    datos_pdf = {
        'id': nueva_tasacion.id,
        'marca': nueva_tasacion.marca,
        'modelo': nueva_tasacion.modelo,
        'anio': nueva_tasacion.anio,
        'precio_estimado': nueva_tasacion.precio_estimado
    }
    
    pdf_path = generar_informe_tasacion(datos_pdf)

    # Enviar PDF por correo
    enviar_informe(
        nueva_tasacion.email,
        'Informe de Tasación BiciFlix',
        pdf_path
    )

    # Responder con el ID, precio estimado e informe PDF
    return jsonify({
        "id": nueva_tasacion.id, 
        "precio_estimado": precio,
        "informe_pdf": pdf_path
    }), 201
