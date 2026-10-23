import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)


def inicializar_db():
  conn = sqlite3.connect('comentarios_texto.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios_texto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            likes INTEGER NOT NULL,
            dislikes INTEGER NOT NULL,
            cliente TEXT NOT NULL,
            analisis_texto TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
  conn.commit()
  conn.close()


inicializar_db()


@app.route('/')
def home():
  return render_template('texto_panel.html')


@app.route('/api/guardar_comentario_texto', methods=['POST', 'OPTIONS'])
def guardar_comentario():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    data = request.json or {}
    producto = data.get('producto', 'Producto General')
    likes = int(data.get('likes', 1))
    dislikes = int(data.get('dislikes', 0))
    cliente = data.get('cliente', 'Anónimo')
    analisis = data.get('analisis_texto', 'Comentario favorable')

    conn = sqlite3.connect('comentarios_texto.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO comentarios_texto (producto, likes, dislikes, cliente, analisis_texto)
        VALUES (?, ?, ?, ?, ?)
    ''',
        (producto, likes, dislikes, cliente, analisis),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'mensaje': '¡Texto procesado y guardado en la base de datos!',
    })
  except Exception as e:
    return jsonify({'status': 'error', 'mensaje': str(e)}), 500


@app.route('/api/listar_comentarios_texto', methods=['GET'])
def listar_comentarios():
  try:
    conn = sqlite3.connect('comentarios_texto.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, producto, likes, dislikes, cliente, analisis_texto, fecha'
        ' FROM comentarios_texto ORDER BY id DESC'
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
            'analisis_texto': f[5],
            'fecha': f[6],
        }
        for f in filas
    ]

    return jsonify(registros)
  except Exception as e:
    return jsonify([]), 500


if __name__ == '__main__':
  print('Iniciando Servidor Punto 7 en http://127.0.0.1:5007')
  app.run(debug=True, port=5007)