# Dashboard, privacidad y publicación

La aplicación Dash de E3 tiene páginas de contexto, datos, modelos, investigación, reproducibilidad y piloto. El servicio se prepara con un nombre independiente en Render. No reemplaza E2 ni publica archivos de Colab.

La aplicación de presentación no importa Torch ni ejecuta entrenamiento. No incluye un formulario de carga de imágenes mientras no exista un modelo entrenado y exportado que haya superado controles. Así se evita ofrecer predicciones con pesos aleatorios.

El panel de modelos distingue claramente la reserva histórica y el candidato con piloto en curso, cuya evidencia final aún no ha sido recibida. Los enlaces bibliográficos abren fuentes originales. El libro compilado se sirve bajo `/libro/` y la comprobación de salud bajo `/healthz`.

La publicación requiere un repositorio remoto E3 y un servicio Render separado. El archivo de despliegue no demuestra que el servicio ya esté publicado. El contenedor debe verificarse en el entorno de destino antes de anunciar una URL pública.
