from flask import jsonify, request, abort
import re
from flask_cors import cross_origin
from app import app, db
from app.models import Tasacion
from app.utils.pricing_algorithm import calcular_precio
from app.utils.pdf_generator import generar_informe_tasacion
from app.utils.email_sender import enviar_informe
from datetime import datetime

@app.route('/tasacion', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def crear_tasacion():
    print("Solicitud recibida en /tasacion")
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    print("Datos recibidos:", data)
    
    try:
        # Validaciones
        if not data:
            raise ValueError("No se enviaron datos en la solicitud.")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
            raise ValueError("Email inválido")
        
        anio = int(data.get('year', 0))
        if anio < 2000 or anio > datetime.now().year:
            raise ValueError(f"Año inválido. Debe estar entre 2000 y {datetime.now().year}.")
        
        if not data.get('marca') or not isinstance(data['marca'], str):
            raise ValueError("Marca inválida o faltante.")
        
        if data.get('transmision') not in ['Mecánica', 'Electrónica']:
            raise ValueError("Transmisión inválida. Debe ser 'Mecánica' o 'Electrónica'.")

        # Crear una nueva tasación
        nueva_tasacion = Tasacion(
            email=data['email'],
            tipo_operacion='comprar',
            marca=data['marca'],
            modelo=data['modelo'],
            anio=anio,
            transmision=data['transmision'],
            talla=data['talla']
        )
        
        # Calcular el precio estimado
        precio = calcular_precio(data)
        nueva_tasacion.precio_estimado = precio

        # Guardar en la base de datos
        db.session.add(nueva_tasacion)
        db.session.commit()

        print(f"Tasación creada: ID={nueva_tasacion.id}, Precio={precio}")

        # Generar PDF
        datos_pdf = {
            'id': nueva_tasacion.id,
            'marca': nueva_tasacion.marca,
            'modelo': nueva_tasacion.modelo,
            'anio': nueva_tasacion.anio,
            'precio_estimado': nueva_tasacion.precio_estimado,
            'transmision': nueva_tasacion.transmision,
            'talla': nueva_tasacion.talla
        }
        
        try:
            pdf_path = generar_informe_tasacion(datos_pdf)
            print(f"PDF generado: {pdf_path}")
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            pdf_path = None #En caso de error, establecemos PDF_PATH A nONE

        # Enviar email
    if pdf_path:
        try:
            enviar_informe(nueva_tasacion.email, 'Informe de Tasación BiciFlix', pdf_path)
            print(f"Email enviado a {nueva_tasacion.email}")
        except Exception as e:
            print(f"Error al enviar el email: {str(e)}")
    else:
        print("No se pudo enviar el email porque no se generó el PDF")
            # No lanzamos una excepción aquí para que la tasación se complete incluso si falla el envío del email

        return jsonify({
            "id": nueva_tasacion.id, 
            "marca": nueva_tasacion.marca,
            "modelo": nueva_tasacion.modelo,
            "anio": nueva_tasacion.anio,
            "precio_estimado": precio,
            "informe_pdf": pdf_path
        }), 201

        except ValueError as e:
            print(f"Error de validación: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500

# Puedes agregar más rutas según sea necesario

if __name__ == '__main__':
    app.run(debug=True)