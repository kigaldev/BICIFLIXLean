import pytest
from app import app, db
from app.models import Tasacion
from app.utils.pricing_algorithm import calcular_precio

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

def test_calculo_precio():
    datos_bicicleta = {
        "anio": 2020,
        "transmision": "Mecánica",
        "talla": "M"
    }
    
    precio = calcular_precio(datos_bicicleta)
    
    assert isinstance(precio, float)
    assert precio > 0

def test_datos_invalidos(client):
    datos_invalidos = {
        "email": "correo_invalido",
        "anio": -1,
        "transmision": "Otro"
    }
    
    response = client.post('/tasacion', json=datos_invalidos)
    assert response.status_code == 400

def test_calculo_precio_edge_cases():
    casos_prueba = [
        {"anio": 2024, "transmision": "Electrónica", "talla": "XS"},
        {"anio": 2010, "transmision": "Mecánica", "talla": "XL"}
    ]
    
    for caso in casos_prueba:
        precio = calcular_precio(caso)
        assert precio > 0