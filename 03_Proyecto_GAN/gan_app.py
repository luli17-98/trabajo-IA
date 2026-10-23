import numpy as np
import matplotlib.pyplot as plt
import gradio as gr

print("Iniciando servicio GAN para la interfaz web...")

def generar_imagen_gan(semilla):
    try:
        np.random.seed(int(semilla))
        # Ruido latente sintético
        matriz = np.random.normal(0, 1, (28, 28))
        
        ruta_salida = "imagen_generada_gan.png"
        plt.figure(figsize=(4, 4))
        plt.imshow(matriz, cmap='inferno')
        plt.axis('off')
        plt.title(f"Muestra Sintética (Seed {semilla})", fontsize=10)
        plt.savefig(ruta_salida, bbox_inches='tight')
        plt.close()
        
        return ruta_salida, f"¡Patrón sintético generado con éxito! Semilla: {semilla}"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Interfaz Gradio
interfaz_gan = gr.Interface(
    fn=generar_imagen_gan,
    inputs=gr.Slider(minimum=1, maximum=1000, step=1, value=42, label="Espacio Latente (Semilla)"),
    outputs=[
        gr.Image(type="filepath", label="Resultado Sintético GAN"),
        gr.Textbox(label="Estado")
    ],
    title="Generador GAN",
    description="Modulo de Redes Generativas Antagónicas"
)

if __name__ == "__main__":
    # Permite embeber la app dentro del panel HTML
    interfaz_gan.launch(server_port=7861, inline=True)