import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*"}})


def inicializar_db():
  conn = sqlite3.connect('animales_ia.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS caracteristicas_animales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_animal TEXT NOT NULL,
            especie TEXT NOT NULL,
            confianza REAL NOT NULL,
            habitat TEXT NOT NULL,
            fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
  conn.commit()
  conn.close()


inicializar_db()


@app.route('/')
def home():
  return render_template('db_panel.html')


@app.route('/api/guardar_animal', methods=['POST', 'OPTIONS'])
def guardar_animal():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    data = request.json or {}
    animal = data.get('nombre_animal', 'Desconocido')
    especie = data.get('especie', 'General')
    confianza = float(data.get('confianza', 98.5))
    habitat = data.get('habitat', 'Terrestre')

    conn = sqlite3.connect('animales_ia.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO caracteristicas_animales (nombre_animal, especie, confianza, habitat)
        VALUES (?, ?, ?, ?)
    ''',
        (animal, especie, confianza, habitat),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'mensaje': f'¡{animal} guardado correctamente en la base de datos!',
    })
  except Exception as e:
    return jsonify({'status': 'error', 'mensaje': str(e)}), 500


@app.route('/api/listar_animales', methods=['GET'])
def listar_animales():
  try:
    conn = sqlite3.connect('animales_ia.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, nombre_animal, especie, confianza, habitat, fecha_analisis'
        ' FROM caracteristicas_animales ORDER BY id DESC'
    )
    filas = cursor.fetchall()
    conn.close()

    registros = [
        {
            'id': f[0],
            'nombre_animal': f[1],
            'especie': f[2],
            'confianza': f[3],
            'habitat': f[4],
            'fecha': f[5],
        }
        for f in filas
    ]

    return jsonify(registros)
  except Exception as e:
    return jsonify([]), 500


if __name__ == '__main__':
  print('Servidor Punto 5 iniciado en http://127.0.0.1:5005')
  app.run(debug=True, port=5005)