# Ficha del modelo CICO 6101

Estado: piloto exploratorio, no producto clínico. Tres clases: tumor, linfocito y estroma. Entrada PNG/JPEG RGB 128×128, sin redimensionamiento automático; normalización exacta en models/cico_6101.json. ONNX con proveedor CPU y verificación SHA-256 al cargar.

Seleccionado por el mejor macro-F1 de validación entre cinco semillas: 0,7174428, época 22. Esta selección introduce optimismo; no constituye rendimiento en test independiente. Entrenamiento: 14.539 recortes de 83 pacientes; validación: 2.049 de 21 pacientes. Las cinco semillas tienen media 0,668243 y desviación entre semillas 0,037204.

La exportación conserva las clases en 2.049/2.049 imágenes de validación y máxima diferencia de probabilidad 3,72529e-7 frente a PyTorch. Esta prueba demuestra concordancia numérica, no generalización clínica.

No hay calibración independiente, detector fuera de dominio, cobertura certificada ni validación externa. La entropía es descriptiva. La oclusión representa sensibilidad local y necesita evaluación de fidelidad/estabilidad. Una fotografía no histológica también puede recibir una predicción: no usar para diagnóstico.

Las cargas se procesan en memoria y el código no escribe imágenes a disco. Requiere confirmar autorización antes de cargar. No aportar identificadores personales. Conservación y acceso de la infraestructura se rigen además por el proveedor.

Pesos ONNX SHA-256: da64160bc772eb3486107ff1f10ad97327ff0d61f7d8a642727003799ca6bcb5.
Procedencia, contrato y verificación detallados: models/cico_6101.json y libro, capítulo 16.

Actualización de interfaz 21 noviembre: se rechazan imágenes uniformes mediante un filtro de calidad, sin detector de dominio validado. Se admite RGBA totalmente opaco convirtiendo a RGB. Diagnósticos sin recalibración y comparación exploratoria están en /diagnosticos; CICO no demuestra superioridad.
