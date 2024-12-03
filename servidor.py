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
@app.route('/add', methods=['POST'])
def add_procedimiento():
    if request.method == 'POST':
        idEje = request.form['idEje']
        idArea = request.form['idArea']
        idDependencia = request.form['idDependencia']
        tipoProcedimiento = request.form['tipoProcedimiento']
        estado = request.form['estado']
        teletrabajado = request.form['teletrabajado']
        idMacroproceso = request.form['idMacroproceso']
        idEjeEstrategico = request.form['idEjeEstrategico']
        tipoDocumento = request.form['tipoDocumento']
        nombreProcedimiento = request.form['nombreProcedimiento']
        apoyoTecnologico = request.form['apoyoTecnologico']
        anioActualizacion = request.form['anioActualizacion']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Procedimientos 
            (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado, idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (idEje, idArea, idDependencia, tipoProcedimiento, estado, teletrabajado, idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion))
        conn.commit()
        conn.close()
        flash('Procedimiento agregado exitosamente!')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods=['POST'])
def delete_procedimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Procedimientos WHERE idEje = ?', (id,))
    conn.commit()
    conn.close()
    flash('Procedimiento eliminado exitosamente!')
    return redirect(url_for('index'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit_procedimiento(id):
    if request.method == 'POST':
        idArea = request.form['idArea']
        idDependencia = request.form['idDependencia']
        tipoProcedimiento = request.form['tipoProcedimiento']
        estado = request.form['estado']
        teletrabajado = request.form['teletrabajado']
        idMacroproceso = request.form['idMacroproceso']
        idEjeEstrategico = request.form['idEjeEstrategico']
        tipoDocumento = request.form['tipoDocumento']
        nombreProcedimiento = request.form['nombreProcedimiento']
        apoyoTecnologico = request.form['apoyoTecnologico']
        anioActualizacion = request.form['anioActualizacion']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Procedimientos 
            SET idArea = ?, idDependencia = ?, tipoProcedimiento = ?, estado = ?, teletrabajado = ?, 
                idMacroproceso = ?, idEjeEstrategico = ?, tipoDocumento = ?, nombreProcedimiento = ?, 
                apoyoTecnologico = ?, anioActualizacion = ?
            WHERE idEje = ?
        ''', (idArea, idDependencia, tipoProcedimiento, estado, teletrabajado, idMacroproceso, idEjeEstrategico, tipoDocumento, nombreProcedimiento, apoyoTecnologico, anioActualizacion, id))
        conn.commit()
        conn.close()
        flash('Procedimiento actualizado exitosamente!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
