def calcular_precio(data):
    # Implementación inicial del algoritmo de precios según el documento
    precio_base = 3000  # Ejemplo de precio base
    
    # Depreciación anual
    antiguedad = 2024 - data.get('anio', 2024)
    precio_depreciado = precio_base * (0.8 ** antiguedad)
    
    # Ajustes por transmisión
    if data.get('transmision') == 'Electrónica':
        precio_depreciado *= 1.1
    
    # Ajustes por talla
    if data.get('talla') in ['XS', 'S', 'XL']:
        precio_depreciado *= 0.97
    
    return round(precio_depreciado, 2)