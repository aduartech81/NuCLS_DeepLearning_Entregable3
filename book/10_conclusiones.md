# Conclusiones: resultado negativo y alcance

**CICO obtuvo menor Macro-F1 que las tres bases en las cinco semillas emparejadas de esta validación.** Su media fue 0,6682, frente a 0,7509 de SoftmaxCNN-BN, 0,7692 de DenseNet121 y 0,7843 de ResNet50: diferencias de −8,27, −10,10 y −11,60 puntos porcentuales. La hipótesis de mejora no recibe apoyo en este corte; el sentido observado es contrario al esperado.

El contraste contextual tampoco muestra un beneficio consistente: eliminarlo eleva la media de 0,6682 a 0,6791. Sin amortiguación se obtiene 0,6610 y sin contexto 0,6625. Estos resultados no prueban equivalencia ni ausencia universal de utilidad del mecanismo. El diseño carece de un control entrenado de capacidad comparable que separe tamaño de arquitectura.

La inferencia tiene límites concretos: cinco semillas, validación utilizada para seleccionar checkpoints, presupuestos de ajuste históricos distintos y pacientes fijos. El Wilcoxon bilateral exacto no puede alcanzar 0,05 con cinco diferencias no nulas. Repetir análisis sobre estos datos no añade réplicas ni crea una prueba independiente.

La contribución demostrada consiste en una implementación trazable de corrección contextual acotada, su propiedad D4, los resultados del piloto y quince ablaciones conservadas. La originalidad de la combinación requiere contrastar antecedentes; D4, contexto y atención no son contribuciones originales por sí solos.

Tres semillas seleccionaron la época 1 porque las cinco épocas siguientes no superaron su Macro-F1; la pérdida de entrenamiento sí descendió. Esta observación explica el funcionamiento de la parada temprana, pero no identifica causalmente sobreajuste, capacidad o falta de entrenamiento.

[Resumen de entrega, análisis adicional y defensa](28_cierre_revision.md). PCam y los controles pendientes se mantienen separados de los resultados completos. Esta edición posterior no acredita envío dentro del plazo ni cierre experimental de E3.
