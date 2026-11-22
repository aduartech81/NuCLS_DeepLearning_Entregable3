# Cierre documental y análisis sin GPU

Actualización del 21 de noviembre de 2026. Esta versión añade evidencia; conserva E1, el ZIP entregado y los resultados originales. No acredita cumplimiento total ni entrega dentro del plazo.

## Auditoría de resultados

Se cotejaron **66 corridas de desarrollo, 330 archivos, 2.049 predicciones por corrida y 21 pacientes**: hashes contra el índice, probabilidades, clases, macro-F1, curvas, historias, mejor época y métricas por paciente. No hay pesos en esa carpeta: no se certifica su integridad ni una reproducción independiente.

Se verificaron **390 huellas de las 65 evaluaciones de reserva**. Los diagnósticos siguientes corresponden a ensambles de cinco semillas de los tres modelos seleccionados por media de validación. No son resultados de un único checkpoint ni de CICO.

| Ensamble | Macro-F1 | IC95 descriptivo por paciente | Brier | ECE (10 bins fijos) |
|---|---:|---|---:|---:|
| inception_v3 | 0.7496 | [0.5610, 0.8052] | 0.1916 | 0.0689 |
| efficientnet_b0 | 0.7275 | [0.5216, 0.7990] | 0.2271 | 0.0842 |
| resnet18 | 0.5268 | [0.2589, 0.7014] | 0.4743 | 0.1114 |

Bootstrap agrupado por paciente, 2.000 remuestras, semilla 20261121; cada paciente aporta todos sus recortes. Reserva histórica expuesta, seis pacientes y 969 recortes. Los intervalos son descriptivos y condicionados a estos ensambles; no garantizan cobertura ni independencia confirmatoria. Los cálculos anteriores se conservan: este diagnóstico tiene su propio método y semilla.

La tabla histórica de métricas por semilla ya incluye pendiente e intercepto top-label. Se corrige su clasificación anterior como ausentes; sigue pendiente la calibración independiente y la evaluación por subgrupos.

## Revisión de errores preparada

Se seleccionaron 100 errores por ensamble (300 filas), con semilla fija y campos vacíos para adjudicación. Inception y EfficientNet comparten 91 errores; Inception y ResNet18, 89; EfficientNet y ResNet18, 98. Las filas con identificadores se mantienen en el paquete local, no en la web pública. No se ha realizado revisión humana. El muestreo de ensambles no reemplaza la exigencia de errores adjudicados por modelo principal.

## Dashboard y explicación

Los filtros de clase y partición actualizan tres gráficos EDA y sus totales. Los diagnósticos históricos agregados se identifican como otra población porque no permiten ese cruce. Se incorpora Bootstrap para la distribución adaptable; queda pendiente una revisión completa en tablet.

La predicción CICO informa latencia de la solicitud y entropía; ninguna es una garantía de exactitud. La explicación por oclusión sustituye cada bloque de 16×16 por el color medio de la imagen, en una malla 8×8. Representa la caída de probabilidad de la clase originalmente elegida. Valores negativos indican aumento. No es segmentación, causalidad ni Grad-CAM. Quedan pendientes estudios de fidelidad y estabilidad; no corrige por sí sola los mapas constantes de Inception en E2.

## Paquete de reproducibilidad

El repositorio incorpora `MODEL_CARD.md`, `DATA_STATEMENT.md`, `CITATION.cff`, `LICENSE_STATUS.md` y `CIERRE_Y_DEFENSA.md`. Las fichas documentan el alcance actual. La licencia y declaración de autoría requieren decisión del autor; no se les asigna una firma ni un DOI inexistente.

## Secuencia de cierre

1. Las 15 ablaciones ya fueron recibidas y verificadas; conservar su respaldo y completar los controles pendientes.
2. PCam continúa en Colab según el autor: 8301/8302 completas, 8303 en entrenamiento. Recibir y auditar el próximo respaldo; no intervenir el proceso.
3. Completar los experimentos pendientes del protocolo final, controles y datasets externos. Cinco semillas piloto y quince ablaciones no sustituyen el benchmark final.
4. Adjudicar errores, cerrar búsqueda bibliográfica, confirmar licencia/autoría y obtener reproducción externa.
5. Integrar resultados finales, revisar enlaces y crear una entrega nueva con manifiesto de huellas. No sobrescribir la entrega anterior.

[Auditoría completa de requisitos](17_auditoria_cierre.md) · [Histología y explicación de casos](09a_histologia.md)


## Tabla maestra de evidencia disponible

Consulte la [tabla maestra compartida con NuCLEA](21_tabla_maestra.md). Se genera automáticamente desde la misma fuente y contiene las tres variantes de ablación verificadas, sin mezclar las poblaciones de E1, E2 y E3.
