# Cierre operativo y recepción de evidencia

Actualización: 21 noviembre 2026, America/Bogota. Entrega: sábado 21, 10:00 a. m.

## Estado del piloto E3

Cinco semillas piloto completas y verificadas desde el ZIP recibido el 21 de noviembre. Macro-F1 de validación: media 0.6682 ± DE 0.0372. No es un resultado de prueba ni una demostración de superioridad.

[Resultados por semilla y auditoría](14_resultados_piloto.md). El ZIP y el notebook se copiaron a una carpeta independiente y se registraron sus hashes. El paquete pasó integridad y verificación de las predicciones. No hace falta repetir el piloto.

## Siguiente paso sin repetir entrenamiento

1. Conservar el ZIP original recibido y el notebook con salidas.
2. Seleccionar y documentar la política de exportación usando validación; comprobar preprocesamiento e ida/vuelta numérica.
3. Medir latencia y memoria CPU y validar entradas antes de habilitar predicción web.
4. Mantener separados los resultados piloto y la evaluación final pendiente.

## Qué todavía exige evidencia adicional

| Requisito | Situación y siguiente paso |
|---|---|
| Piloto ≥5 semillas | Cinco completas, recibidas y verificadas; piloto cerrado. |
| Benchmark final ≥10 o tamaño mayor por potencia al 90 % | El piloto actual no lo completa. Calcular tamaño y fijar familia antes de nuevas corridas. |
| Ablaciones de ≥3 componentes propios | Las de preprocesamiento E2 no las sustituyen; requieren variantes y corridas específicas. |
| Tres conjuntos adicionales | Requieren auditoría, protocolo y evaluación de toda la familia. PCam observado no equivale automáticamente a prueba independiente. |
| Inferencia CPU y exportación | Código previo disponible; falta validar artefactos entrenados, equivalencia, latencia y entradas fuera de dominio. |
| Revisión de novedad y tercero | Conservar fuentes, cadenas y nivel de lectura. La implementación por sí sola no demuestra novedad. |
| Publicación | Render publicado y verificado en escritorio; falta comprobar móvil y el flujo de inferencia cuando exista el modelo. |
| Defensa | Preparar explicación de formulación, cotas, diferencias con antecedentes y límites experimentales. |

No se equipara una entrega documental a completar los experimentos de la guía. Los resultados que no se hayan ejecutado no se presentan como cumplidos.

## Continuidad de E2

El cierre de reserva, las 15 ablaciones de preprocesamiento y los ensambles constan en la trazabilidad heredada. Antes de modificar la web E2 se cotejan contra sus archivos fuente; no se reentrena ni se vuelve a seleccionar sobre reserva.

Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado. Desde ese respaldo quedan 61 épocas (1 de 8302 y 60 de 8303–8305), más test y resumen. Se omiten semillas completas y se recuperan pesos, optimizador y estados aleatorios; no se repite lo guardado.

Inception presenta mapas Grad-CAM constantes en la evidencia revisada: requieren cambiar la capa o método y verificar fidelidad antes de mostrarlos como explicaciones válidas. El techo multi-rater requiere anotaciones independientes enlazadas; una máscara QC no lo sustituye. Sigue siendo necesaria la revisión de las 66 corridas base y la reproducción externa.

E1 y el ZIP E2 entregado son inmutables. Los cambios posteriores pertenecen a las versiones online, con su fecha e historial.
