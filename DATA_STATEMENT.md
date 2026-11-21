# Declaración de datos

La tarea es clasificación de recortes histológicos, con separación y remuestreo por paciente. Los recortes del mismo paciente no son unidades independientes.

- EDA histórico E1: 14.428 recortes de entrenamiento y 3.571 de validación.
- Piloto E3 y evidencia de desarrollo auditada: 2.049 recortes de validación, 21 pacientes; entrenamiento E3 14.539 recortes, 83 pacientes.
- Reserva histórica E2: 969 recortes, seis pacientes. Ya expuesta; no puede presentarse como reserva sellada después del análisis.

No combinar estas poblaciones en un único ranking sin controlar partición, preprocesamiento y unidad experimental. Los manifiestos y huellas del repositorio documentan los cortes recibidos, pero falta acreditar toda la auditoría de duplicados/fuga.

La galería contiene campos histológicos reales y anotaciones originales. El campo ilustrado no equivale automáticamente al tensor 128×128 de entrada ni la anotación es una explicación generada por el modelo. Los pies de figura distinguen origen, etiqueta y predicción.

Los permisos de redistribución del dataset y de cada recurso requieren cotejo de sus licencias originales. Esta ficha no concede derechos nuevos. El CSV de errores con identificadores se conserva localmente para revisión autorizada.
