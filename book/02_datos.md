# Datos y contrato de entrada

El piloto usa exclusivamente train y validación de NuCLS. El contrato esperado contiene 14.539 recortes / 83 pacientes de entrenamiento y 2.049 / 21 de validación. Estos números no equivalen a una nueva auditoría de imágenes realizada en esta actualización.

La ejecución verifica el manifiesto, cada archivo, las clases y la separación por paciente, sitio y hash de píxeles. Se detiene ante incompatibilidad. Las clases técnicas son `tumor_nonMitotic`, `lymphocyte`, `nonTILnonMQ_stromal`. Los nombres cortos del dashboard son etiquetas de presentación.

El centro geométrico del recorte no se trata como segmentación del núcleo. El cotejo con anotaciones debe comprobar centrado y cobertura. Las anotaciones no deben incorporarse como señales de entrada si la tarea define inferencia con RGB limpio.

Los conjuntos PanNuke, Lizard y MoNuSAC son candidatos, no datos auditados. Hay posibles fuentes TCGA compartidas y solapamiento PanNuke–Lizard. Se mantienen taxonomías nativas; epitelial no equivale automáticamente a tumor. El control de duplicados y pacientes precede a cualquier confirmación externa.
