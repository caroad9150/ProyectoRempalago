from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
server = 'tiusr3pl.cuc-carrera-ti.ac.cr'  # IP o nombre del servidor SQL
database = 'proyetoR'
username = 'sitios'
password = 'SitiosC32024'

# Función para establecer la conexión a la base de datos
def get_db_connection():
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    return conn

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# CRUD para la tabla Procedimientos
@app.route('/procedimientos', methods=['POST'])
def create_procedimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Procedimientos (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado, 
        idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data['idEje'], data['idArea'], data['idDependencia'], data['tipoProcedimiento'], data['estado'], 
         data['teletrabajado'], data['idMacroproceso'], data['idEjeEstrategico'], data['tipoDocumento'], 
         data['nombreProcedimiento'], data['apoyoTecnologico'], data['anioActualizacion'])
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento creado exitosamente'}), 201
 
@app.route('/procedimientos', methods=['GET'])
def get_procedimientos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Procedimientos")
    rows = cursor.fetchall()
    conn.close()
 
    procedimientos = []
    for row in rows:
        procedimientos.append({
            'idEje': row.idEje,
            'idArea': row.idArea,
            'idDependencia': row.idDependencia,
            'tipoProcedimiento': row.tipoProcedimiento,
            'estado': row.estado,
            'teletrabajado': row.teletrabajado,
            'idMacroproceso': row.idMacroproceso,
            'idEjeEstrategico': row.idEjeEstrategico,
            'tipoDocumento': row.tipoDocumento,
            'nombreProcedimiento': row.nombreProcedimiento,
            'apoyoTecnologico': row.apoyoTecnologico,
            'anioActualizacion': row.anioActualizacion
        })
    return jsonify(procedimientos)
 
@app.route('/procedimientos/<idEje>', methods=['PUT'])
def update_procedimiento(idEje):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Procedimientos
        SET idArea = ?, idDependencia = ?, tipoProcedimiento = ?, estado = ?, teletrabajado = ?, 
            idMacroproceso = ?, idEjeEstrategico = ?, tipoDocumento = ?, nombreProcedimiento = ?, 
            apoyoTecnologico = ?, anioActualizacion = ?
        WHERE idEje = ?
    """, data['idArea'], data['idDependencia'], data['tipoProcedimiento'], data['estado'], 
         data['teletrabajado'], data['idMacroproceso'], data['idEjeEstrategico'], data['tipoDocumento'], 
         data['nombreProcedimiento'], data['apoyoTecnologico'], data['anioActualizacion'], idEje)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento actualizado exitosamente'})
 
@app.route('/procedimientos/<idEje>', methods=['DELETE'])
def delete_procedimiento(idEje):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Procedimientos WHERE idEje = ?", idEje)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento eliminado exitosamente'})
##area 
#vista de nueva
@app.route('/nueva_area')
def nueva_area():
    return render_template('nueva_area.html')

@app.route('/enviar_area', methods=['POST'])
def enviar_area():
    # Recoger datos del formulario
    id_area = request.form['idrearea']
    nombre_area = request.form['nombreArea']
    
    # Validación opcional
    if not id_area or not nombre_area:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))  

    try:
        # Insertar datos en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Area (idArea, nombreArea)
            VALUES (?, ?)
        ''', (id_area, nombre_area))
        conn.commit()
        conn.close()
        flash('Área registrada exitosamente.')
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('index'))  

    return redirect(url_for('index'))  

#vista de consulta
@app.route('/consulta_area', methods=['GET'])
def consulta_area():
    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT idArea, nombreArea FROM Area')
        areas = cursor.fetchall()
        conn.close()
        # Renderiza los datos en la interfaz de consulta
        return render_template('consulta_area.html', areas=areas)
    except Exception as e:
        flash(f'Error al consultar áreas: {str(e)}')
        return redirect(url_for('index')) 

@app.route('/eliminar_area')
def eliminar_area():
    return render_template('eliminar_area.html')

@app.route('/eliminarT_area', methods=['POST'])
def enviarT_dependencia():
    id_dependencia = request.form['idDependencia']
    
    # Validación opcional
    if not id_dependencia:
        flash('El campo  es obligatorio.')
        return redirect(url_for('eliminar_dependencia'))
    
    try:
        # Buscar la dependencia en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM area WHERE idArea = ?
        ''', (id_dependencia,))
        dependencia = cursor.fetchone()
        
        if dependencia:
            # Eliminar la dependencia
            cursor.execute('''
                DELETE FROM area WHERE idArea = ?
            ''', (id_dependencia,))
            conn.commit()
            flash('Eliminada exitosamente.')
        else:
            flash('No se encontró una dependencia con ese ID.')
        
        conn.close()
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('eliminar_area'))
    
    return redirect(url_for('eliminar_area'))

@app.route('/editar_area')
def editar_area():
    return render_template('editar_area.html')

@app.route('/editarT_area', methods=['POST'])
def enviarT_editar_dependencia():
    id_area = request.form['idArea']
    nuevo_nombre = request.form['nuevoNombre']
    
    # Validación opcional
    if not id_area or not nuevo_nombre:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('editar_area'))
    
    try:
        # Buscar la dependencia en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Dependencia WHERE idDependencia = ?
        ''', (id_area,))
        dependencia = cursor.fetchone()
        
        if dependencia:
            # Actualizar la dependencia
            cursor.execute('''
                UPDATE area
                SET nombreArea = ?
                WHERE idArea = ?
            ''', (nuevo_nombre, id_area))
            conn.commit()
            flash('Atualizada exitosamente.')
        else:
            flash('No se encontró una area con ese ID.')
        
        conn.close()
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('editar_area'))
    
    return redirect(url_for('editar_area'))

##dependencia
#vista de nueva
@app.route('/nueva_dependencia')
def nueva_dependencia():
    return render_template('nueva_dependencia.html')

@app.route('/enviar_dependencia', methods=['POST'])
def enviar_dependencia():
    # Recoger datos del formulario
    id_area = request.form['idreDependencia']
    nombre_area = request.form['nombreDependencia']
    
    # Validación opcional
    if not id_area or not nombre_area:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))  

    try:
        # Insertar datos en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Area (idArea, nombreArea)
            VALUES (?, ?)
        ''', (id_area, nombre_area))
        conn.commit()
        conn.close()
        flash('Área registrada exitosamente.')
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('index'))  

    return redirect(url_for('index'))  

#vista de consulta
@app.route('/consulta_area', methods=['GET'])
def consulta_area():
    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT idArea, nombreArea FROM Area')
        areas = cursor.fetchall()
        conn.close()
        # Renderiza los datos en la interfaz de consulta
        return render_template('consulta_area.html', areas=areas)
    except Exception as e:
        flash(f'Error al consultar áreas: {str(e)}')
        return redirect(url_for('index')) 

@app.route('/eliminar_area')
def eliminar_area():
    return render_template('eliminar_area.html')

@app.route('/eliminarT_area', methods=['POST'])
def enviarT_dependencia():
    id_dependencia = request.form['idDependencia']
    
    # Validación opcional
    if not id_dependencia:
        flash('El campo  es obligatorio.')
        return redirect(url_for('eliminar_dependencia'))
    
    try:
        # Buscar la dependencia en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM area WHERE idArea = ?
        ''', (id_dependencia,))
        dependencia = cursor.fetchone()
        
        if dependencia:
            # Eliminar la dependencia
            cursor.execute('''
                DELETE FROM area WHERE idArea = ?
            ''', (id_dependencia,))
            conn.commit()
            flash('Eliminada exitosamente.')
        else:
            flash('No se encontró una dependencia con ese ID.')
        
        conn.close()
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('eliminar_area'))
    
    return redirect(url_for('eliminar_area'))

@app.route('/editar_area')
def editar_area():
    return render_template('editar_area.html')

@app.route('/editarT_area', methods=['POST'])
def enviarT_editar_dependencia():
    id_area = request.form['idArea']
    nuevo_nombre = request.form['nuevoNombre']
    
    # Validación opcional
    if not id_area or not nuevo_nombre:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('editar_area'))
    
    try:
        # Buscar la dependencia en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Dependencia WHERE idDependencia = ?
        ''', (id_area,))
        dependencia = cursor.fetchone()
        
        if dependencia:
            # Actualizar la dependencia
            cursor.execute('''
                UPDATE area
                SET nombreArea = ?
                WHERE idArea = ?
            ''', (nuevo_nombre, id_area))
            conn.commit()
            flash('Atualizada exitosamente.')
        else:
            flash('No se encontró una area con ese ID.')
        
        conn.close()
    except Exception as e:
        flash(f'Ocurrió un error: {str(e)}')
        return redirect(url_for('editar_area'))
    
    return redirect(url_for('editar_area'))


if __name__ == '__main__':
    app.run(debug=True)
