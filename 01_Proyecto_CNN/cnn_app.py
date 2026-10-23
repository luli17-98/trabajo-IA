import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import gradio as gr

# 1. Cargamos el modelo CNN pre-entrenado (MobileNetV2)
print("Cargando la Red Neuronal Convolucional (CNN)...")
modelo = MobileNetV2(weights='imagenet')

# Diccionario básico de traducción para mostrar resultados en español
traducciones = {
    "Irish_setter": "Setter irlandés (Perro)",
    "bloodhound": "Sabueso / Perro de San Huberto",
    "golden_retriever": "Golden Retriever (Perro)",
    "labrador_retriever": "Labrador Retriever (Perro)",
    "German_shepherd": "Pastor alemán (Perro)",
    "cat": "Gato",
    "persian_cat": "Gato persa",
    "car": "Automóvil",
    "laptop": "Computadora portátil",
    "cell_phone": "Teléfono celular"
}

# 2. Función que procesa la imagen y devuelve las predicciones
def clasificar_imagen(imagen_ingresada):
    if imagen_ingresada is None:
        return "Por favor, sube una imagen."
    
    # Adaptamos el tamaño de la imagen a 224x224 (lo que requiere la CNN)
    img = imagen_ingresada.resize((224, 224))
    
    # Convertimos la imagen a una matriz numérica (array)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # Realizamos la predicción con la red CNN
    preds = modelo.predict(x)
    resultados = decode_predictions(preds, top=3)[0]
    
    # Formateamos las respuestas traducidas
    etiquetas_espanol = {}
    for res in resultados:
        nombre_ingles = res[1]
        probabilidad = float(res[2])
        nombre_traducido = traducciones.get(nombre_ingles, nombre_ingles.replace("_", " "))
        etiquetas_espanol[nombre_traducido] = probabilidad
        
    return etiquetas_espanol

# 3. Interfaz de usuario con Gradio (Vibe Coding)
interfaz = gr.Interface(
    fn=clasificar_imagen,
    inputs=gr.Image(type="pil", label="Sube o arrastra una imagen aquí"),
    outputs=gr.Label(num_top_classes=3, label="Predicciones de la Red Neuronal CNN"),
    title="Punto 1: Clasificador de Imágenes con CNN (Vibe Coding)",
    description="Subí cualquier fotografía para que la Red Neuronal Convolucional (CNN) analice sus patrones visuales y prediga qué es."
)

# 4. Iniciar la aplicación en tu máquina local
if __name__ == "__main__":
    interfaz.launch()