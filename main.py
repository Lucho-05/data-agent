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
        return jsonify({"error": f"Error de conexi\u00f3n a la base de datos: {str(e)}"}), 500

    # Construir la consulta SQL dinámicamente
    base_query = "SELECT * FROM tickets_data"
    conditions = []
    params = []

    # Mapear los parámetros de la solicitud a las columnas de la BD
    # **NUEVOS PARÁMETROS** - Más consistentes y sin errores de escritura
    query_params = {
        'ID': request.args.get('id'),
        'Titulo': request.args.get('titulo'),
        'Tipo de Ticket': request.args.get('tipo_de_ticket'),
        'MAIL': request.args.get('mail'),
        'ASIGNADO': request.args.get('asignado'),
        'SUB_CATEGORIA': request.args.get('sub_categoria'),
        'CATEGORIA': request.args.get('categoria'),
        'PRIORIDAD': request.args.get('prioridad'),
        'EQUIPO_ASIGNADO': request.args.get('equipo_asignado'),
        'PROPIETARIO': request.args.get('propietario'),
        'Estado': request.args.get('estado'),
        'Fecha de Creación': request.args.get('fecha_creacion'),
        'Fecha de Última Modificación': request.args.get('fecha_ultima_modificacion'),
        'Fecha de Resolución': request.args.get('fecha_resolucion'),
        'Días Transcurridos': request.args.get('dias_transcurridos'),
        'Cumple resolución': request.args.get('cumple_resolucion'),
        'Cumple respuesta': request.args.get('cumple_respuesta'),
        'Tiempo de resolución ANS': request.args.get('tiempo_resolucion_ans')
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
            return jsonify({"mensaje": "No se encontraron tickets con los par\u00e1metros dados."}), 404

    except Exception as e:
        return jsonify({"error": f"Error en la consulta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))