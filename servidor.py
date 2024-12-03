from flask import Flask, jsonify, render_template, request
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
@app.route('/procedimientos', methods=['GET'])
def get_procedimientos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Procedimientos')
    rows = cursor.fetchall()
    conn.close()
    procedimientos = [
        {
            'idEje': row[0],
            'idArea': row[1],
            'idDependencia': row[2],
            'tipoProcedimiento': row[3],
            'estado': row[4],
            'teletrabajado': row[5],
            'idMacroproceso': row[6],
            'idEjeEstrategico': row[7],
            'tipoDocumento': row[8],
            'nombreProcedimiento': row[9],
            'apoyoTecnologico': row[10],
            'anioActualizacion': row[11]
        }
        for row in rows
    ]
    return jsonify(procedimientos)

@app.route('/procedimientos/<int:id>', methods=['GET'])
def get_procedimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Procedimientos WHERE idEje = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        procedimiento = {
            'idEje': row[0],
            'idArea': row[1],
            'idDependencia': row[2],
            'tipoProcedimiento': row[3],
            'estado': row[4],
            'teletrabajado': row[5],
            'idMacroproceso': row[6],
            'idEjeEstrategico': row[7],
            'tipoDocumento': row[8],
            'nombreProcedimiento': row[9],
            'apoyoTecnologico': row[10],
            'anioActualizacion': row[11]
        }
        return jsonify(procedimiento)
    return jsonify({'message': 'Procedimiento no encontrado'}), 404

@app.route('/procedimientos', methods=['POST'])
def create_procedimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Procedimientos 
        (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado, idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['idEje'], data['idArea'], data['idDependencia'], data['tipoProcedimiento'], data['estado'],
          data['teletrabajado'], data['idMacroproceso'], data['idEjeEstrategico'], data['tipoDocumento'],
          data['nombreProcedimiento'], data['apoyoTecnologico'], data['anioActualizacion']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento creado exitosamente'}), 201

@app.route('/procedimientos/<int:id>', methods=['PUT'])
def update_procedimiento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Procedimientos 
        SET idArea = ?, idDependencia = ?, tipoProcedimiento = ?, estado = ?, teletrabajado = ?, 
            idMacroproceso = ?, idEjeEstrategico = ?, tipoDocumento = ?, nombreProcedimiento = ?, 
            apoyoTecnologico = ?, anioActualizacion = ?
        WHERE idEje = ?
    ''', (data['idArea'], data['idDependencia'], data['tipoProcedimiento'], data['estado'], 
          data['teletrabajado'], data['idMacroproceso'], data['idEjeEstrategico'], data['tipoDocumento'], 
          data['nombreProcedimiento'], data['apoyoTecnologico'], data['anioActualizacion'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento actualizado exitosamente'})

@app.route('/procedimientos/<int:id>', methods=['DELETE'])
def delete_procedimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Procedimientos WHERE idEje = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Procedimiento eliminado exitosamente'})



if __name__ == '__main__':
    app.run(debug=True)
