# Datos y contrato de entrada

El piloto usa exclusivamente train y validación de NuCLS. El contrato esperado contiene 14.539 recortes / 83 pacientes de entrenamiento y 2.049 / 21 de validación. Estos números no equivalen a una nueva auditoría de imágenes realizada en esta actualización.

La ejecución verifica el manifiesto, cada archivo, las clases y la separación por paciente, sitio y hash de píxeles. Se detiene ante incompatibilidad. Las clases técnicas son `tumor_nonMitotic`, `lymphocyte`, `nonTILnonMQ_stromal`. Los nombres cortos del dashboard son etiquetas de presentación.

El centro geométrico del recorte no se trata como segmentación del núcleo. El cotejo con anotaciones debe comprobar centrado y cobertura. Las anotaciones no deben incorporarse como señales de entrada si la tarea define inferencia con RGB limpio.

Los conjuntos PanNuke, Lizard y MoNuSAC son candidatos, no datos auditados. Hay posibles fuentes TCGA compartidas y solapamiento PanNuke–Lizard. Se mantienen taxonomías nativas; epitelial no equivale automáticamente a tumor. El control de duplicados y pacientes precede a cualquier confirmación externa.

## EDA heredado de E1: selección de clases

| particion | clase | origen | incluidas | retencion | porcentaje |
|---|---|---|---|---|---|
| entrenamiento | tumor_nonMitotic | 13826 | 7089 | 0.5127 | 49.1336 |
| entrenamiento | lymphocyte | 9036 | 4162 | 0.4606 | 28.8467 |
| entrenamiento | nonTILnonMQ_stromal | 6607 | 3177 | 0.4809 | 22.0197 |
| validacion | tumor_nonMitotic | 3485 | 1646 | 0.4723 | 46.0935 |
| validacion | lymphocyte | 2629 | 1196 | 0.4549 | 33.4920 |
| validacion | nonTILnonMQ_stromal | 1582 | 729 | 0.4608 | 20.4144 |

Esta tabla histórica contiene 14.428 ejemplos de entrenamiento y 3.571 de validación. **No coincide con el contrato V2 del piloto E3 (14.539 / 2.049)** y no se presenta como si fuera el mismo manifiesto. Se conserva como antecedente del proceso de selección; cualquier comparación experimental requiere verificar la versión usada.

Las imágenes y sus anotaciones se examinan en el [capítulo histológico](09a_histologia.md). Los histogramas de calidad y el cambio de dominio están en el [EDA interactivo](https://nucls-entregable3.onrender.com/datos). La etiqueta del núcleo no convierte el campo completo en una máscara de segmentación.
