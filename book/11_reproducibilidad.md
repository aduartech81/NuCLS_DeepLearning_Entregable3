# Reproducibilidad y defensa

## Ruta única

Usar el cuaderno RunPod `NuCLS_E3_RunPod.ipynb`. La celda 1 audita datos, la 2 inicia un proceso independiente, la 3 consulta el avance y la 4 empaqueta al finalizar. La salida se conserva en `/workspace/NuCLS_E3_PILOTO_CICO_V1`; debe descargarse antes de eliminar el Pod. El cuaderno Colab es un antecedente y no es la ruta activa. No se debe iniciar mientras otro trabajo use la misma GPU.

El ejecutor guarda checkpoints por época, estado del optimizador y generadores aleatorios. Verifica identidad y evidencias antes de omitir corridas. Una época incompleta puede repetirse. Los cambios de entorno y bloqueos provocan una detención conservadora; no se borran automáticamente.

## Paquete web

`requirements.txt` define dependencias del servidor; `requirements-book.txt`, las del libro. Docker incluye la compilación HTML verificada del libro y arranca Gunicorn. El libro se recompila antes de empaquetar cambios documentales. No se incluyen imágenes de pacientes ni pesos de modelos en el paquete web.

El manifiesto de publicación registra hashes de los archivos distribuidos. Esto verifica identidad de archivos, no validez científica de las conclusiones. La exportación ONNX futura debe comprobar equivalencia sobre imágenes de verificación; la fixture sintética previa no constituye un modelo clínico.

## Autoría y defensa

Se declara asistencia de IA para preparación de código, documentación y revisión. El autor debe comprender y defender las decisiones, verificar referencias y asumir responsabilidad por el informe. La revisión por un tercero y la réplica independiente no se declaran realizadas.

Guion de 20 minutos: problema/datos (3), antecedentes e hipótesis (4), mecanismo y propiedad (4), diseño y resultados disponibles (5), demostración y límites (4). Explicar por qué ocho vistas no son ocho pacientes y por qué la reserva E2 no es una confirmación nueva.
