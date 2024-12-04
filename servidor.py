from flask import Flask, redirect, render_template, request, url_for
import pyodbc
import json  # Para serializar distribuciones correctamente

app = Flask(__name__)

DATABASE_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'tiusr3pl.cuc-carrera-ti.ac.cr',
    'database': 'proyetoR',
    'username': 'sitios',
    'password': 'SitiosC32024'
}

def get_db_connection():
    connection_string = (
        f"DRIVER={DATABASE_CONFIG['driver']};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']};"
        f"Timeout=30;"
    )
    return pyodbc.connect(connection_string)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener nombres de las columnas desde la base de datos
        cursor.execute("SELECT TOP 0 * FROM procedimientos")
        columnas = [desc[0] for desc in cursor.description]

        # Leer los valores de los filtros enviados por el usuario
        valores_filtro = {col: request.form.get(col, '') for col in columnas}

        # Generar valores únicos para cada columna (para los filtros)
        filtros = {}
        for columna in columnas:
            cursor.execute(f"SELECT DISTINCT RTRIM(LTRIM({columna})) AS {columna} FROM procedimientos")
            filtros[columna] = [row[0] for row in cursor.fetchall() if row[0] is not None]

        # Construir consulta dinámica con los filtros seleccionados
        query = f"SELECT {', '.join(columnas)} FROM procedimientos WHERE 1=1"
        params = []
        for col, valor in valores_filtro.items():
            if valor:
                query += f" AND {col} = ?"
                params.append(valor)

        # Ejecutar la consulta con los filtros
        cursor.execute(query, params)
        procedimientos = cursor.fetchall()

        # Recalcular distribuciones basadas en los datos filtrados
        distribuciones = {}
        for columna in columnas:
            cursor.execute(f"""
                SELECT RTRIM(LTRIM({columna})) AS valor, COUNT(*) AS cantidad
                FROM procedimientos
                WHERE 1=1 {''.join([f" AND {c} = ?" if valores_filtro[c] else '' for c in columnas])}
                GROUP BY {columna}
            """, params)
            resultados = cursor.fetchall()
            distribuciones[columna] = [{"valor": row[0], "cantidad": row[1]} for row in resultados if row[0] is not None]

        cursor.close()
        conn.close()

        # Serializamos distribuciones como JSON
        distribuciones_json = json.dumps(distribuciones)

        return render_template(
            'index.html',
            columnas=columnas,
            filtros=filtros,  
            procedimientos=procedimientos,
            valores_filtro=valores_filtro,
            distribuciones_json=distribuciones_json  
        )
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"

<<<<<<< Updated upstream
# Procedimientos
@app.route('/procedimientos')
def listar_procedimientos():
    conn = get_db_connection()
    procedimientos = conn.execute('SELECT * FROM Procedimientos').fetchall()
    conn.close()
    return render_template('procedimientos.html', procedimientos=procedimientos)

@app.route('/create_procedimiento', methods=('GET', 'POST'))
def create_procedimiento():
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        conn = get_db_connection()
        query = """
            INSERT INTO Procedimientos (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado,
            idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit_procedimiento/<string:idEje>', methods=('GET', 'POST'))
def edit_procedimiento(idEje):
    conn = get_db_connection()
=======
# Ruta para listar los registros
@app.route('/procedimientos')
def procedimientos():
    conn = get_db_connection()
    procedimientos = conn.execute('SELECT * FROM Procedimientos').fetchall()
    conn.close()
    return render_template('procedimientos.html', procedimientos=procedimientos)

# Ruta para crear un nuevo registro
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        conn = get_db_connection()
        query = """
            INSERT INTO Procedimientos (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado,
            idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Ruta para actualizar un registro
@app.route('/edit/<string:idEje>', methods=('GET', 'POST'))
def edit(idEje):
    conn = get_db_connection()
>>>>>>> Stashed changes
    procedimiento = conn.execute('SELECT * FROM Procedimientos WHERE idEje = ?', (idEje,)).fetchone()

    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        query = """
            UPDATE Procedimientos SET 
            idArea = ?, idDependencia = ?, tipoProcedimiento = ?, estado = ?, teletrabajado = ?,
            idMacroproceso = ?, idEjeEstrategico = ?, tipoDocumento = ?, nombreProcedimiento = ?, 
            apoyoTecnologico = ?, anioActualizacion = ?
            WHERE idEje = ?
        """
        conn.execute(query, (*data.values(), idEje))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', procedimiento=procedimiento)

<<<<<<< Updated upstream
@app.route('/delete_procedimiento/<string:idEje>', methods=('POST',))
def delete_procedimiento(idEje):
=======
# Ruta para eliminar un registro
@app.route('/delete/<string:idEje>', methods=('POST',))
def delete(idEje):
>>>>>>> Stashed changes
    conn = get_db_connection()
    conn.execute('DELETE FROM Procedimientos WHERE idEje = ?', (idEje,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

<<<<<<< Updated upstream
# Áreas
@app.route('/areas')
def listar_areas():
    conn = get_db_connection()
    procedimientos = conn.execute('SELECT * FROM areas').fetchall()
    conn.close()
    return render_template('areas.html', procedimientos=procedimientos)

@app.route('/create_area', methods=('GET', 'POST'))
def create_area():
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        conn = get_db_connection()
        query = """
            INSERT INTO area (idArea, nombreArea)
            VALUES (?, ?)
        """
        conn.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit_area/<string:idArea>', methods=('GET', 'POST'))
def edit_area(idArea):
    conn = get_db_connection()
    procedimiento = conn.execute('SELECT * FROM area WHERE idArea = ?', (idArea,)).fetchone()

    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        query = """
            UPDATE area SET 
            idArea = ?, nombreArea = ?
            WHERE idArea = ?
        """
        conn.execute(query, (*data.values(), idArea))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', procedimiento=procedimiento)
=======
>>>>>>> Stashed changes

@app.route('/delete_area/<string:idArea>', methods=('POST',))
def delete_area(idArea):
    conn = get_db_connection()
    conn.execute('DELETE FROM area WHERE idArea = ?', (idArea,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)