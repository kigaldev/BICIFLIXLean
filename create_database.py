import sqlite3

# Ruta donde se creará la base de datos
db_path = "database/biciflix.db"

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla de tasaciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    tipo TEXT,
    marca TEXT,
    modelo TEXT,
    anio INTEGER,
    transmision TEXT,
    talla TEXT,
    estado TEXT,
    precio_estimado REAL
)
""")

print("Tabla 'tasaciones' creada exitosamente.")

# Cerrar la conexión
conn.commit()
conn.close()
