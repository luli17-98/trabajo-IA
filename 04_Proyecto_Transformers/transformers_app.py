from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/')
def home():
    return render_template('transformers.html')

@app.route('/api/transformers', methods=['POST'])
def procesar_transformer():
    data = request.json or {}
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "No se ingresó ningún prompt"}), 400

    # Lógica de simulación autoregresiva / Multi-Head Attention
    respuesta = "La arquitectura Transformer procesa secuencias utilizando mecanismos de Self-Attention (Query, Key, Value) para calcular dependencias globales en paralelo."
    
    if "código" in prompt.lower() or "python" in prompt.lower():
        respuesta = "import torch\nimport transformers\n\n# Carga de modelo Transformer preentrenado\nmodel = transformers.AutoModel.from_pretrained('gpt2')"

    return jsonify({
        "status": "success",
        "prompt_recibido": prompt,
        "tokens": len(prompt.split()) + 24,
        "respuesta": respuesta,
        "mecanismo": "Multi-Head Self-Attention (12 Heads)"
    })

if __name__ == '__main__':
    print("Iniciando Módulo 4: Transformers en http://127.0.0.1:5004")
    app.run(debug=True, port=5004)