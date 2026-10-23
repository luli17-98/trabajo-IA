import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)


def inicializar_db():
  conn = sqlite3.connect('comentarios_sonido.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios_audio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            likes INTEGER NOT NULL,
            dislikes INTEGER NOT NULL,
            cliente TEXT NOT NULL,
            sentimiento_audio TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
  conn.commit()
  conn.close()


inicializar_db()


@app.route('/')
def home():
  return render_template('sonido_panel.html')


@app.route('/api/guardar_comentario_audio', methods=['POST', 'OPTIONS'])
def guardar_comentario():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    data = request.json or {}
    producto = data.get('producto', 'Producto General')
    likes = int(data.get('likes', 1))
    dislikes = int(data.get('dislikes', 0))
    cliente = data.get('cliente', 'Anónimo')
    sentimiento = data.get('sentimiento_audio', 'Positivo')

    conn = sqlite3.connect('comentarios_sonido.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO comentarios_audio (producto, likes, dislikes, cliente, sentimiento_audio)
        VALUES (?, ?, ?, ?, ?)
    ''',
        (producto, likes, dislikes, cliente, sentimiento),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'mensaje': (
            f'¡Audio de {cliente} procesado y guardado en la base de datos!'
        ),
    })
  except Exception as e:
    return jsonify({'status': 'error', 'mensaje': str(e)}), 500


@app.route('/api/listar_comentarios_audio', methods=['GET'])
def listar_comentarios():
  try:
    conn = sqlite3.connect('comentarios_sonido.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, producto, likes, dislikes, cliente, sentimiento_audio, fecha'
        ' FROM comentarios_audio ORDER BY id DESC'
    )
    filas = cursor.fetchall()
    conn.close()

    registros = [
        {
            'id': f[0],
            'producto': f[1],
            'likes': f[2],
            'dislikes': f[3],
            'cliente': f[4],
            'sentimiento_audio': f[5],
            'fecha': f[6],
        }
        for f in filas
    ]

    return jsonify(registros)
  except Exception as e:
    return jsonify([]), 500


if __name__ == '__main__':
  print('Iniciando Servidor Punto 6 en http://127.0.0.1:5006')
  app.run(debug=True, port=5006)