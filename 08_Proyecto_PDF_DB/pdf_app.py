import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)


def inicializar_db():
  conn = sqlite3.connect('analisis_pdf.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos_pdf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            resumen TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
  conn.commit()
  conn.close()


inicializar_db()


@app.route('/')
def home():
  return render_template('pdf_panel.html')


@app.route('/api/guardar_pdf', methods=['POST', 'OPTIONS'])
def guardar_pdf():
  if request.method == 'OPTIONS':
    return jsonify({'status': 'ok'}), 200

  try:
    data = request.json or {}
    nombre = data.get('nombre_archivo', 'Documento.pdf')
    resumen = data.get(
        'resumen', 'Resumen generado automáticamente por IA del documento PDF.'
    )

    conn = sqlite3.connect('analisis_pdf.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO documentos_pdf (nombre_archivo, resumen)
        VALUES (?, ?)
    ''',
        (nombre, resumen),
    )
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'mensaje': (
            '¡PDF procesado y resumen almacenado en la base de datos!'
        ),
    })
  except Exception as e:
    return jsonify({'status': 'error', 'mensaje': str(e)}), 500


@app.route('/api/listar_pdfs', methods=['GET'])
def listar_pdfs():
  try:
    conn = sqlite3.connect('analisis_pdf.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, nombre_archivo, resumen, fecha FROM documentos_pdf ORDER BY'
        ' id DESC'
    )
    filas = cursor.fetchall()
    conn.close()

    registros = [
        {'id': f[0], 'nombre_archivo': f[1], 'resumen': f[2], 'fecha': f[3]}
        for f in filas
    ]

    return jsonify(registros)
  except Exception as e:
    return jsonify([]), 500


if __name__ == '__main__':
  print('Iniciando Servidor Punto 8 en http://127.0.0.1:5008')
  app.run(debug=True, port=5008)