def calcular_precio(data):
    precio_base = 3000
    
    # Ajuste por antigüedad más preciso
    antiguedad = 2024 - data.get('anio', 2024)
    depreciacion = max(0.2 * antiguedad, 0.8)
    precio_depreciado = precio_base * depreciacion
    
    # Ajustes por transmisión y talla
    if data.get('transmision') == 'Electrónica':
        precio_depreciado *= 1.1
    
    if data.get('talla') in ['XS', 'S', 'XL']:
        precio_depreciado *= 0.97
    
    return round(precio_depreciado, 2)