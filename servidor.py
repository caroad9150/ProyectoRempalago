from flask import Flask, render_template
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





if __name__ == '__main__':
    app.run(debug=True)
