import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

@app.route('/tickets', methods=['GET'])
def get_tickets():
    try:
        connection = get_db_connection()
    except Exception as e:
        return jsonify({"error": f"Error de conexión a la base de datos: {str(e)}"}), 500

    # Construir la consulta SQL dinámicamente
    base_query = "SELECT * FROM tickets"
    conditions = []
    params = []

    # Mapear los parámetros de la solicitud a las columnas de la BD
    query_params = {
        'ID': request.args.get('ID'),
        'Titulo': request.args.get('Titulo'),
        'Tipo de Ticket': request.args.get('Tipo de Ticket'),
        'MAIL': request.args.get('MAIL'),
        'ASIGNADO': request.args.get('ASIGNADO'),
        'SUB_CATEGORIA': request.args.get('SUB_CATEGORIA'),
        'CATEGORIA': request.args.get('CATEGORIA'),
        'PRIORIDAD': request.args.get('PRIORIDAD'),
        'EQUIPO_ASIGNADO': request.args.get('EQUIPO_ASIGNADO'),
        'PROPIETARIO': request.args.get('PROPIETARIO'),
        'Estado': request.args.get('Estado'),
        'Fecha de Creación': request.args.get('Fecha de Creacion'),
        'Fecha de Última Modificación': request.args.get('Fecha de Ultima Modificacion'),
        'Fecha de Resolución': request.args.get('Fecha de Resolucion'),
        'Días Transcurridos': request.args.get('Dias Transcurridos'),
        'Cumple resolución': request.args.get('Cumple resolucion'),
        'Cumple respuesta': request.args.get('Cumple respuesta'),
        'Tiempo de resolución ANS': request.args.get('Tiempo de resolucion ANS')
    }

    for key, value in query_params.items():
        if value:
            # Usar %s para prevenir inyección SQL
            conditions.append(f"`{key}` = %s") 
            params.append(value)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # Ejecutar la consulta
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(base_query, params)
            tickets = cursor.fetchall()
        
        connection.close()

        if tickets:
            return jsonify(tickets)
        else:
            return jsonify({"mensaje": "No se encontraron tickets con los parámetros dados."}), 404

    except Exception as e:
        return jsonify({"error": f"Error en la consulta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))