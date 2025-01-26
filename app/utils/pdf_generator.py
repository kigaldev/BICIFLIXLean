from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors

def generar_informe_tasacion(datos_tasacion):
    pdf_path = f"informes/tasacion_{datos_tasacion['id']}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    elementos = []
    estilos = getSampleStyleSheet()
    
    # Título
    titulo = Paragraph("Informe de Tasación BiciFlix", estilos['Title'])
    elementos.append(titulo)
    
    # Datos de la tasación
    datos_tabla = [
        ['Campo', 'Valor'],
        ['Marca', datos_tasacion['marca']],
        ['Modelo', datos_tasacion['modelo']],
        ['Año', str(datos_tasacion['anio'])],
        ['Precio Estimado', f"${datos_tasacion['precio_estimado']:.2f}"]
    ]
    
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