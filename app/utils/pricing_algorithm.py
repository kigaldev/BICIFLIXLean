from datetime import datetime

def calcular_precio(data):
    precio_base = 3000  # Precio base de una bicicleta de gama media

    # Ajuste por antigüedad
    anio_actual = datetime.now().year
    antiguedad = anio_actual - int(data.get('year', anio_actual))
    factor_depreciacion = max(0.5, 1 - (antiguedad * 0.1))  # Máximo 50% de depreciación
    precio = precio_base * factor_depreciacion

    # Ajuste por marca
    marcas_premium = ['Specialized', 'Trek', 'Cannondale', 'Santa Cruz', 'Pinarello']
    if data.get('marca') in marcas_premium:
        precio *= 1.2  # 20% extra para marcas premium

    # Ajuste por transmisión
    if data.get('transmision') == 'Electrónica':
        precio *= 1.15  # 15% extra para transmisión electrónica

    # Ajuste por talla
    if data.get('talla') in ['XS', 'S', 'XL']:
        precio *= 0.95  # 5% menos para tallas menos comunes

    # Ajuste por intensidad de uso
    uso = data.get('uso', 'Moderado')
    if uso == 'Intensivo':
        precio *= 0.85  # 15% menos para uso intensivo
    elif uso == 'Regular':
        precio *= 0.92  # 8% menos para uso regular

    # Redondear el precio a dos decimales
    return round(precio, 2)