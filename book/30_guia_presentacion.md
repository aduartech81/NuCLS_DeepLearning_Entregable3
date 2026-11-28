# Guía rápida de presentación de NuCLEA

**Andrés Duarte Chaves · 28 de noviembre de 2026.** Estado reportado de PCam: 26 de noviembre; no es monitoreo en vivo.

## 1. Guion rápido para presentar

### Apertura · 1 minuto

Soy Andrés Duarte Chaves. NuCLEA estudia la clasificación de núcleos tumorales, linfocitarios y estromales en imágenes histológicas. Integra datos, modelos, resultados y una demostración de inferencia. Es un prototipo de investigación, no una herramienta diagnóstica.

### Datos y bases · 2 minutos

Mostrar Explorar tejido y Comparar resultados. Explicar que la referencia corresponde al núcleo objetivo, no a toda la imagen. Se separan pacientes entre particiones. E1 incluyó CNN-BN, DenseNet121 y ResNet50; las métricas de poblaciones distintas no se mezclan en un ranking único.

### Propuesta CICO · 2 minutos

CICO procesa ocho orientaciones y combina descriptores del centro y del entorno. Añade una corrección limitada a los logits centrales, amortiguada por dispersión. La cota limita la corrección; no demuestra robustez clínica ni que el modelo sea mejor. D4, contexto y compuertas tienen antecedentes.

### Resultados y ablaciones · 2 minutos

Cinco semillas CICO y quince ablaciones completadas. Macro-F1 medio CICO: 0,66824. Bases en la comparación de validación: 0,7509; 0,7692; 0,7843. Sin contraste: 0,67914. No se demuestra superioridad; el beneficio del contraste no recibe apoyo en este piloto.

### Demostración · 3 minutos

Abrir Probar una imagen. Mostrar un acierto y después un error conocido; comparar referencia, predicción y puntuaciones. Explicar que el mapa de oclusión mide sensibilidad local, no segmentación ni causalidad.

### Cierre · 1 minuto

La contribución comprobada es la implementación trazable, el piloto, las ablaciones y la integración funcional. Quedan controles de capacidad, evaluación externa y confirmatoria. PCam es parcial. No presentar el proyecto como cierre experimental completo.

## 2. Demostración de imágenes, paso a paso

### Antes de presentar

Abrir el dashboard y comprobar /healthz. Descargar y descomprimir Imagenes_NuCLEA_para_prueba.zip en el computador. Mantener los PNG originales: RGB, 128 × 128, sin ampliar, capturar ni añadir anotaciones. Este guion dura unos 11 minutos; ampliar preguntas y explicación de código si se dispone de 20.

### Ruta A · ejemplo incorporado

En Probar una imagen, elegir Caso 01. Marcar la confirmación de uso experimental. Esperar la vista previa y pulsar Analizar recorte. La referencia es tumor no mitótico y la predicción registrada es tumor (91,3 %). Son puntuaciones no calibradas.

### Ruta B · comprobar la subida real

Con la confirmación marcada, pulsar Seleccionar imagen PNG o JPG. Elegir caso_13_linfocito.png del paquete. Esperar el nombre y la vista previa; pulsar Analizar recorte. La referencia y la predicción registrada son linfocito (91,7 %).

### Mostrar una limitación real

Subir caso_31_estroma.png: referencia estroma; predicción registrada linfocito (91,8 %). Decir: una puntuación alta no garantiza acierto. No ocultar esta discrepancia ni cambiar la etiqueta de referencia.

### Qué hacer si una imagen no se acepta

El formulario exige PNG/JPEG RGB 128 × 128, máximo 2 MB. Una lámina completa, una captura o un recorte anotado no sustituye la entrada original. El filtro de apariencia es experimental y puede rechazar histología válida. No quitarlo durante la demostración para forzar un resultado.

### Si falla la conexión

Reintentar cuando Render responda. Usar el catálogo de referencia para explicar resultados ya calculados, diciendo explícitamente que son precalculados. No presentarlos como una nueva inferencia en vivo. No tocar Colab ni PCam para reparar el dashboard.

## 3. Respuestas a los comentarios del profesor

### ¿CICO supera a los modelos base?

No. Quedó por debajo de las tres bases en las cinco semillas emparejadas. La hipótesis de mejora no recibió apoyo. El p conjunto ajustado de 0,1875 no demuestra equivalencia, ni convierte el resultado en favorable.

### ¿Por qué cinco semillas no son suficientes?

Con cinco diferencias no nulas, el Wilcoxon bilateral exacto tiene p mínimo 0,0625 antes de ajustes. Más semillas permiten estimar mejor; no garantizan superioridad. El número de réplicas y la potencia deben definirse antes de una evaluación confirmatoria.

### ¿Falta el control de capacidad?

Sí. CICO tiene una capacidad y un presupuesto distintos de las bases. Sin un control entrenado comparable no puedo atribuir la diferencia al mecanismo contextual. Un control implementado pero no entrenado no cierra esta exigencia.

### ¿Qué enseñan las ablaciones?

Quitar el contraste elevó la media observada de 0,66824 a 0,67914. No encontramos evidencia suficiente de que ese componente mejore el resultado bajo el protocolo del piloto. Las ablaciones no demuestran utilidad universal ni equivalencia.

### ¿Qué pasó con PCam y los externos?

PCam se declara réplica parcial: 8301 y 8302 completas, 8303 con época 5 guardada, 8304/8305 pendientes y sin test final, según reporte del 26 de noviembre. No se acredita la evaluación final de tres datasets externos con toda la familia. Un protocolo escrito no equivale a resultados ejecutados.

### ¿Qué es original y qué significa el mapa?

La combinación concreta de corrección acotada y dispersión es una propuesta candidata; no reivindico como nuevos D4 o atención. NuClass es un antecedente de integración local/contextual. El mapa de oclusión muestra cambios de puntuación al ocultar regiones: no es una máscara nuclear ni una explicación causal validada.

## Catálogo de ejemplos originales

Ejemplos seleccionados de validación; no estiman exactitud global y no constituyen test independiente.

| Archivo | Referencia | Predicción registrada | Coincide |
|---|---|---|---|
| caso_01_tumor.png | Tumor no mitótico | tumor | Sí |
| caso_07_tumor.png | Tumor no mitótico | tumor | Sí |
| caso_13_linfocito.png | Linfocito | linfocito | Sí |
| caso_19_linfocito.png | Linfocito | tumor | No |
| caso_25_estroma.png | Estroma no TIL / no macrófago | estroma | Sí |
| caso_31_estroma.png | Estroma no TIL / no macrófago | linfocito | No |

[Probar imágenes](https://nucls-entregable3.onrender.com/prediccion) · [Sustentación](https://nucls-entregable3.onrender.com/defensa) · [Libro](https://nucls-entregable3.onrender.com/libro/)
