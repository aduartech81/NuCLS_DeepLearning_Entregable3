# Cierre operativo y recepción de evidencia

Actualización: 20 noviembre 2026, America/Bogota. Entrega: sábado 21, 10:00 a. m.

## Estado del piloto E3

RunPod ejecuta el candidato CICO con la receta congelada: cinco semillas, máximo de 25 épocas y parada temprana. El registro recibido contiene cuatro épocas de 6101; el mejor macro-F1 de validación observado es 0,6265 (época 2). Es una instantánea comunicada, no evidencia final auditada. El tiempo medio observado es 182,8 segundos por época. No se garantiza una hora de finalización.

## Integración sin repetir entrenamiento

1. Esperar el cierre de las cinco semillas. Consultar únicamente la celda 3 del cuaderno RunPod.
2. Ejecutar su celda 4 y descargar `NuCLS_E3_RUNPOD_RESULTADOS.zip`. Descargar también el notebook con sus salidas.
3. Ejecutar localmente `python tools/importar_piloto.py RUTA_AL_ZIP`. El receptor valida las cinco semillas, huellas de pesos y predicciones, identidad común y coherencia de las métricas. No carga Torch ni entrena.
4. Revisar el resumen agregado y las curvas. La tabla y el capítulo generado provienen del mismo archivo de resultados.
5. Exportar el checkpoint seleccionado por validación con su preprocesamiento; comprobar equivalencia numérica e inferencia CPU antes de habilitar predicción web. Conservar GPU, versiones y hashes del entorno original.
6. Compilar el libro y comprobar rutas del dashboard. Publicar únicamente en un servicio E3 independiente y verificar sus enlaces.

## Qué todavía exige evidencia adicional

| Requisito | Situación y siguiente paso |
|---|---|
| Piloto ≥5 semillas | En ejecución; recibir y verificar resultados. |
| Benchmark final ≥10 o tamaño mayor por potencia al 90 % | El piloto actual no lo completa. Calcular tamaño y fijar familia antes de nuevas corridas. |
| Ablaciones de ≥3 componentes propios | Las de preprocesamiento E2 no las sustituyen; requieren variantes y corridas específicas. |
| Tres conjuntos adicionales | Requieren auditoría, protocolo y evaluación de toda la familia. PCam observado no equivale automáticamente a prueba independiente. |
| Inferencia CPU y exportación | Código previo disponible; falta validar artefactos entrenados, equivalencia, latencia y entradas fuera de dominio. |
| Revisión de novedad y tercero | Conservar fuentes, cadenas y nivel de lectura. La implementación por sí sola no demuestra novedad. |
| Publicación | Paquete preparado localmente; acreditar despliegue, enlaces, responsividad y prueba de humo. |
| Defensa | Preparar explicación de formulación, cotas, diferencias con antecedentes y límites experimentales. |

No se equipara una entrega documental a completar los experimentos de la guía. Los resultados que no se hayan ejecutado no se presentan como cumplidos.

## Continuidad de E2

El cierre de reserva, las 15 ablaciones de preprocesamiento y los ensambles constan en la trazabilidad heredada. Antes de modificar la web E2 se cotejan contra sus archivos fuente; no se reentrena ni se vuelve a seleccionar sobre reserva.

PCam está detenido (confirmación del autor, 20 de noviembre). El último inventario comunicado acredita la semilla 8301 completa y la 8302 hasta época 16; 8303–8305 no tienen checkpoints en ese inventario. No se afirma que PCam haya concluido. La reanudación requiere comprobar versiones y estado del optimizador, sin competir con el piloto E3 por la misma GPU.

Inception presenta mapas Grad-CAM constantes en la evidencia revisada: requieren cambiar la capa o método y verificar fidelidad antes de mostrarlos como explicaciones válidas. El techo multi-rater requiere anotaciones independientes enlazadas; una máscara QC no lo sustituye. Sigue siendo necesaria la revisión de las 66 corridas base y la reproducción externa.

E1 y el ZIP E2 entregado son inmutables. Los cambios posteriores pertenecen a las versiones online, con su fecha e historial.
