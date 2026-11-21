# Ablaciones E3 y transición a PCam

## Evidencia y fecha

Corte: 21 noviembre 2026, último registro compartido por el autor. Este es un estado reportado de ejecución, no una recepción de pesos ni monitoreo en vivo. El piloto CICO de cinco semillas sí fue recibido y verificado por separado.

## Diseño de ablaciones

Tres intervenciones: desactivar contraste centro–entorno (`use_contrast=False`), amortiguación por dispersión (`use_dispersion=False`) o corrección contextual (`use_context=False`). Cada una conserva el resto de la arquitectura y la receta. Se usan semillas 6101–6105, máximo 25 épocas, paciencia 5 y el mismo manifiesto train/validation. El control sin D4 no forma parte de esta cola y continúa pendiente.

| Variante | 6101 | 6102 | 6103 | 6104 | 6105 |
|---|---|---|---|---|---|
| Sin contraste | Completa reportada | Completa reportada | Pendiente | Pendiente | Pendiente |
| Sin amortiguación | Completa reportada | Reanudada; época 3 guardada | Pendiente | Pendiente | Pendiente |
| Sin contexto | Completa reportada | Pendiente | Pendiente | Pendiente | Pendiente |

La cola pausó entre épocas al alcanzar su presupuesto y luego reportó reanudación con un presupuesto de 8 horas. Cuatro de quince corridas se reportan completas. No se extrapola actividad posterior ni se atribuyen los fragmentos del log a una variante sin su encabezado.

## Análisis al recibir los resultados

1. Verificar configuración, identidad, historias, checkpoints y predicciones por variante/semilla.
2. Recalcular las métricas y comparar diferencias emparejadas con el piloto completo usando idénticas imágenes y etiquetas.
3. Mostrar curvas completas, distribución entre semillas y tamaños de muestra efectivos; no tratar pendientes como ceros ni imputar resultados.
4. Declarar la selección por validación y el carácter exploratorio; cinco semillas no sustituyen prueba independiente, potencia final ni revisión de multiplicidad.

## PCam: recuperación preparada, no iniciada

Se recibió la carpeta original sin modificarla. El respaldo de transferencia contiene 874.153.429 bytes; todos sus archivos coinciden con las huellas de los originales y los cuatro checkpoints pasaron integridad interna. La marca de fin de 8301 coincide con el hash de su mejor checkpoint. 8302 tiene historia hasta época 16; el estado interno del optimizador debe comprobarse al cargarlo en el entorno compatible.

El cuaderno restaura una copia independiente bajo `/workspace/PCAM_CONTINUACION`. Conserva el código original verificado y exige torch 2.14.1+cu130, torchvision 0.29.1+cu130 y NumPy 2.4.6 en un entorno aislado. La instalación y ejecución en RunPod aún no están verificadas. No se rebajan estas comprobaciones si fallan.

Los datos oficiales PCam no están incluidos: deben descargarse y cotejarse con sus huellas. Las últimas épocas históricas duraron aproximadamente 90 minutos en Colab; no se promete la misma velocidad ni completar todas las semillas en RunPod.

## Cambio seguro de tarea

1. Confirmar fin o pausa controlada de E3; no basta una marca antigua. Comprobar que no haya proceso GPU activo.
2. Respaldar resultados y código de las ablaciones antes de cambiar de tarea.
3. Ejecutar preparación del entorno PCam; si falla una versión, conservar todo y revisar el diagnóstico.
4. Iniciar PCam una sola vez. Debe omitir 8301 y recuperar 8302, sin cambiar la receta.
5. Consultar la primera época nueva y medir duración antes de comprometer las horas restantes. Descargar resultados antes de apagar/eliminar el Pod.

La cola PCam tiene un límite inicial de cinco horas revisado tras guardar una época; puede excederlo por una época completa. No apaga el Pod ni detiene su cobro. E1 y el ZIP entregado permanecen preservados.
