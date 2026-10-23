import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)


def inicializar_db():
  conn = sqlite3.connect('analisis_video.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_video TEXT NOT NULL,
            duracion TEXT NOT NULL,
            analisis TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
  conn.commit()
  conn.close()


inicializar_db()


@app.route('/')
def home():
  return render_template('video_panel.html')


@app.route('/api/guardar_video', methods=['POST', 'OPTIONS'])
def guardar_video():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    data = request.json or {}
    nombre = data.get('nombre_video', 'video_demostrasion.mp4')
    duracion = data.get('duracion', '02:45 min')
    analisis = data.get(
        'analisis', 'Análisis de frames y detección de patrones completado.'
    )

    conn = sqlite3.connect('analisis_video.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO videos_ia (nombre_video, duracion, analisis)
        VALUES (?, ?, ?)
    ''',
        (nombre, duracion, analisis),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'mensaje': '¡Video procesado y almacenado en la base de datos!',
    })
  except Exception as e:
    return jsonify({'status': 'error', 'mensaje': str(e)}), 500


@app.route('/api/listar_videos', methods=['GET'])
def listar_videos():
  try:
    conn = sqlite3.connect('analisis_video.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, nombre_video, duracion, analisis, fecha FROM videos_ia ORDER'
        ' BY id DESC'
    )
    filas = cursor.fetchall()
    conn.close()

    registros = [
        {
            'id': f[0],
            'nombre_video': f[1],
            'duracion': f[2],
            'analisis': f[3],
            'fecha': f[4],
        }
        for f in filas
    ]

    return jsonify(registros)
  except Exception as e:
    return jsonify([]), 500


if __name__ == '__main__':
  print('Iniciando Servidor Vídeos en http://127.0.0.1:5009')
  app.run(debug=True, port=5009)