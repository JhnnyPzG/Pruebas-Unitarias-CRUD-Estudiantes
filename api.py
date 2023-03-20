from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'estudiantes.db'

# Función para conectarse a la base de datos SQLite
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conn = get_db()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    conn.close()
    return jsonify([dict(estudiante) for estudiante in estudiantes])


# Ruta para obtener un estudiante por su ID
@app.route('/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    conn = get_db()
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id,)).fetchone()
    conn.close()
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    return jsonify(dict(estudiante))

# Ruta para crear un nuevo estudiante
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    nuevo_estudiante = request.get_json()
    nombre = nuevo_estudiante['nombre']
    edad = nuevo_estudiante['edad']
    celular = nuevo_estudiante['celular']
    nota = nuevo_estudiante['nota']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estudiantes (nombre, edad, celular, nota) VALUES (?, ?, ?, ?)', (nombre, edad, celular, nota))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': nuevo_id}), 201

# Ruta para actualizar un estudiante existente
@app.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    estudiante_actualizado = request.get_json()
    nombre = estudiante_actualizado['nombre']
    edad = estudiante_actualizado['edad']
    celular = estudiante_actualizado['celular']
    nota = estudiante_actualizado['nota']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE estudiantes SET Nombre = ?, Edad = ?, Celular = ?, Nota = ? WHERE id = ?', (nombre, edad, celular, nota, id))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Estudiante actualizado con éxito'})

# Ruta para eliminar un estudiante existente
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Estudiante eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True)