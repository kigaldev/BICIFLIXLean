import pytest
import os
from app import app, db
from app.models import Tasacion
from app.utils.pricing_algorithm import calcular_precio
from app.utils.pdf_generator import generar_informe_tasacion
import PyPDF2  # Importar la librería para leer PDFs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

# Test para creación de tasación
def test_crear_tasacion(client):
    datos_bicicleta = {
        "email": "test@ejemplo.com",
        "tipo_operacion": "comprar",
        "tipo_bicicleta": "Mountain Bike",
        "marca": "Trek",
        "modelo": "X-Caliber",
        "anio": 2020,
        "transmision": "Mecánica",
        "talla": "M"
    }
    
    response = client.post('/tasacion', json=datos_bicicleta)
    
    assert response.status_code == 201
    data = response.get_json()
    
    assert 'id' in data
    assert 'precio_estimado' in data
    assert data['precio_estimado'] > 0

# Test para el cálculo del precio
def test_calculo_precio():
    datos_bicicleta = {
        "anio": 2020,
        "transmision": "Mecánica",
        "talla": "M"
    }
    
    precio = calcular_precio(datos_bicicleta)
    
    assert isinstance(precio, float)
    assert precio > 0

# Test para manejar datos inválidos
def test_datos_invalidos(client):
    datos_invalidos = {
        "email": "correo_invalido",
        "anio": -1,
        "transmision": "Otro"
    }
    
    response = client.post('/tasacion', json=datos_invalidos)
    assert response.status_code == 400

# Test para casos extremos en el cálculo del precio
def test_calculo_precio_edge_cases():
    casos_prueba = [
        {"anio": 2024, "transmision": "Electrónica", "talla": "XS"},
        {"anio": 2010, "transmision": "Mecánica", "talla": "XL"}
    ]
    
    for caso in casos_prueba:
        precio = calcular_precio(caso)
        assert precio > 0

# Test para la generación de PDF
def test_generar_pdf():
    datos_tasacion = {
        'id': 1,
        'marca': 'Trek',
        'modelo': 'X-Caliber',
        'anio': 2020,
        'precio_estimado': 2400.0
    }
    
    pdf_path = generar_informe_tasacion(datos_tasacion)
    
    assert os.path.exists(pdf_path)  # Verifica que el archivo se ha creado
    assert pdf_path.endswith('.pdf')  # Asegura que es un PDF
    assert os.path.getsize(pdf_path) > 0  # Verifica que no está vacío

# Test para contenido dentro del PDF usando PyPDF2
def test_pdf_contenido():
    datos_tasacion = {
        'id': 1,
        'marca': 'Trek',
        'modelo': 'X-Caliber',
        'anio': 2020,
        'precio_estimado': 2400.0
    }
    
    pdf_path = generar_informe_tasacion(datos_tasacion)
    
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        texto_pdf = ''
        for pagina in pdf_reader.pages:
            texto_pdf += pagina.extract_text()
    
    assert 'Trek' in texto_pdf
    assert 'X-Caliber' in texto_pdf
    assert '2020' in texto_pdf
