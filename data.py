import mysql.connector
import json

# conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="admision_undac"
)

cursor = conn.cursor(dictionary=True)

query = """
SELECT 
p.NOMBRE AS proceso,
c.ESCUELA_COMPLETA,
reg.DNI,
reg.AP_PATERNO,
reg.AP_MATERNO,
reg.NOMBRES,
r.PUNT_T,
r.ORDEN_MERITO_1,
r.EST_OPCION
FROM resultados r
JOIN registros reg ON r.DNI = reg.DNI
JOIN procesos p ON r.PROCESO = p.ID
JOIN carreras c ON r.COD_CARRERA = c.CODIGO_ESCUELA
ORDER BY 
p.NOMBRE,
c.ESCUELA_COMPLETA,
r.ORDEN_MERITO_1 IS NULL,
r.ORDEN_MERITO_1
"""

cursor.execute(query)
rows = cursor.fetchall()

data = {}

for row in rows:

    proceso = row["proceso"]
    carrera = row["ESCUELA_COMPLETA"]

    nombre_completo = f"{row['AP_PATERNO']} {row['AP_MATERNO']} {row['NOMBRES']}"

    postulante = {
        "nombre": nombre_completo,
        "dni": row["DNI"],
        "puntaje": float(row["PUNT_T"]) if row["PUNT_T"] else 0,
        "orden_merito": row["ORDEN_MERITO_1"],
        "estado": row["EST_OPCION"]
    }

    if proceso not in data:
        data[proceso] = {}

    if carrera not in data[proceso]:
        data[proceso][carrera] = []

    data[proceso][carrera].append(postulante)

resultado = []

for proceso, carreras in data.items():

    lista_carreras = []

    for carrera, postulantes in carreras.items():
        lista_carreras.append({
            "carrera": carrera,
            "postulantes": postulantes
        })

    resultado.append({
        "proceso": proceso,
        "carreras": lista_carreras
    })

# guardar json
with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("JSON generado correctamente -> resultados.json")

cursor.close()
conn.close()