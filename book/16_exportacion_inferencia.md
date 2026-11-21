# Exportación e inferencia de CICO

## Modelo para demostración

Se exportó la semilla 6101, elegida por el mayor macro-F1 de validación de las cinco semillas piloto (0,717443). Esto favorece el mejor resultado de selección y no establece superioridad ni rendimiento independiente. Las ablaciones siguen separadas y no modifican este modelo completo.

El checkpoint proviene del ZIP recibido y verificado. Se cargó en CPU con lectura restringida a pesos (`weights_only=True`) y arquitectura cotejada. No se ejecutó entrenamiento ni se intervino RunPod.

## Contrato de entrada

Un PNG o JPEG RGB, 128 × 128 píxeles, hasta 2 MB, centrado en un núcleo y preparado como NuCLS. Se rechazan transparencia, animación, dimensiones distintas y archivos corruptos. No se redimensiona, recorta ni estandariza la tinción automáticamente. Se convierte a [0,1], se aplica la media/desviación originales por canal y se ordena NCHW. No admite WSI ni detecta tejido o núcleo automáticamente.

Clases en orden: tumor_nonMitotic (tumor), lymphocyte (linfocito), nonTILnonMQ_stromal (estroma). Se aplica softmax a los logits. Las probabilidades no están calibradas. No existe detección validada fuera de dominio: una imagen ajena puede recibir una puntuación alta.

## Comprobaciones locales

| Comprobación | Resultado |
|---|---:|
| Error máximo de logits PyTorch CPU → ONNX CPU | 7.15255737e-07 |
| Error máximo de probabilidad CPU frente al registro RunPod | 1.1920929e-07 |
| Recortes reales de validación comprobados | 2 |
| Entradas sintéticas para equivalencia numérica, no desempeño | 16 |
| Tolerancia de aceptación | 0,0001 |
| Latencia mediana local, lote 1 | 3.825 ms |
| Percentil 95 de latencia local | 4.576 ms |

La medición usa 5 calentamientos, 30 repeticiones y 2 hilos en macOS ARM64. **No es latencia de Render.** Debe completarse medición en el servidor. El esquema ONNX fue validado y su hash se comprueba antes de crear la sesión CPU.

SHA256 ONNX: `da64160bc772eb3486107ff1f10ad97327ff0d61f7d8a642727003799ca6bcb5`.

## Manejo de imágenes y alcance

El visitante confirma que el recorte no contiene datos personales y acepta el uso experimental. Al analizar se envía a Render; la aplicación lo decodifica en memoria, no lo escribe en archivos ni lo incorpora a entrenamiento. Se limita el tamaño de la petición. No se prometen diagnóstico, certeza clínica ni interpretación de láminas completas.

La vista muestra imagen, clase con mayor puntuación y las tres probabilidades. Esta capacidad no completa exportación de toda la familia de comparadores, incertidumbre/calibración, robustez, evaluación externa o validación clínica.

Referencia técnica: [API de ONNX Runtime](https://onnxruntime.ai/docs/api/python/api_summary.html).

## Verificación completa del flujo de imágenes

Se cotejaron las 2.049 imágenes originales de validación (21 pacientes), sus huellas y el manifiesto, usando el mismo decodificador, normalización y modelo ONNX del formulario. Las 2.049 clases predichas coinciden con el registro de RunPod; el error máximo de probabilidad fue 3,7252903 × 10⁻⁷. Es una comprobación de equivalencia, no un conjunto de prueba independiente. Las siete pruebas de entradas e integridad pasaron.
