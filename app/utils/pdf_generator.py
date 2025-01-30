from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def generar_informe_tasacion(datos_tasacion):
    pdf_path = f"informes/tasacion_{datos_tasacion['id']}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    elementos = []
    estilos = getSampleStyleSheet()
    
    elementos.append(Paragraph("Informe de Tasación BiciFlix", estilos['Title']))
    elementos.append(Spacer(1, 0.25*inch))
    
    datos_tabla = [
        ['Marca', datos_tasacion['marca']],
        ['Modelo', datos_tasacion['modelo']],
        ['Año', str(datos_tasacion['anio'])],
        ['Precio Estimado', f"${datos_tasacion['precio_estimado']:.2f}"]
    ]
    
    # Añadir transmisión y talla si están disponibles
    if 'transmision' in datos_tasacion:
        datos_tabla.append(['Transmisión', datos_tasacion['transmision']])
    if 'talla' in datos_tasacion:
        datos_tabla.append(['Talla', datos_tasacion['talla']])
    
    tabla = Table(datos_tabla)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    elementos.append(tabla)
    
    doc.build(elementos)
    
    return pdf_path