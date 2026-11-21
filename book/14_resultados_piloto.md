# Resultados del piloto E3

Actualización: 2026-11-21T08:41:55.802388+00:00

ZIP RunPod verificado por huellas, código, conteos y F1 recalculado; no constituye reproducción independiente.

SHA256 del ZIP: `fe2ac1e3abcfbdca81f8f86b85f03a28c5c5cb037160057fb71192c8895dd2ba`.

| Semilla | Mejor época | Macro-F1 validación |
|---|---:|---:|
| 6101 | 22 | 0.717443 |
| 6102 | 18 | 0.699306 |
| 6103 | 1 | 0.642112 |
| 6104 | 1 | 0.639904 |
| 6105 | 1 | 0.642451 |

Media ± DE entre cinco semillas: 0.668243 ± 0.037204. La DE no es un intervalo de confianza.

Selección realizada por validación; no se acredita evaluación en reserva, superioridad ni benchmark final. Las curvas del dashboard usan la misma fuente validada.

## Duración y parada temprana

| Semilla | Épocas ejecutadas | Mejor época | Suma de segundos por época |
|---|---:|---:|---:|
| 6101 | 25 | 22 | 4611.7 |
| 6102 | 23 | 18 | 4262.2 |
| 6103 | 6 | 1 | 1110.6 |
| 6104 | 6 | 1 | 1124.6 |
| 6105 | 6 | 1 | 1118.4 |

Las semillas 6103, 6104 y 6105 conservaron su mejor checkpoint en la época 1 y pararon en la 6: cinco épocas posteriores sin mejora, coherentes con paciencia 5 y mínimo 5. La semilla 6102 paró en la 23 tras su mejor época 18; 6101 alcanzó el máximo de 25. Una parada temprana válida no equivale a buen desempeño ni a superioridad. Este patrón requiere discusión de estabilidad y optimización antes de ampliar el benchmark.

Los tiempos sumados son los registrados por época; no representan todo el tiempo facturado del Pod ni incluyen necesariamente auditoría inicial, exportación y empaquetado.

## Alcance estadístico y selección

Las cinco métricas corresponden al mejor checkpoint de cada semilla **seleccionado con esta misma validación**. Su media describe este piloto con selección; no es una estimación independiente en prueba. La semilla 6101 tiene la mayor métrica, pero escogerla como representante puede favorecer la selección del mejor caso: debe declararse cualquier regla de exportación. No se decide aquí el modelo final ni se declara equivalencia con los baselines.

La variación entre semillas no sustituye incertidumbre por paciente. Cinco semillas no satisfacen el benchmark final exigido ni la potencia conjunta. Las curvas completas ahora proceden del ZIP auditado; ya no faltan las épocas 5–7 de 6101.

## Qué se verificó

Código y configuración frente al piloto local; integridad del ZIP; hashes de pesos y predicciones; cinco semillas con una misma identidad; historias continuas; coherencia de mejor época; 2.049 predicciones de 21 pacientes por semilla, mismo orden y clases; probabilidades válidas y macro-F1 recalculado. No se ejecutaron los checkpoints para esta auditoría. Actualización posterior: CICO 6101 se exportó y verificó sobre 2.049 imágenes; su inferencia CPU se publicó y comprobó en Render. Ver capítulo 16.

Se conservó también el notebook con sus salidas. Contiene un error histórico de lanzamiento duplicado; no se borró ese historial. La presencia de resultados finales coherentes se verificó con los archivos, no solo con la consola.

