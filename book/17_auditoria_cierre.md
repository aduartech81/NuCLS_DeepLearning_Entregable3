# Auditoría contra las guías originales E2 y E3

22 noviembre 2026 · auditoría documental contra las guías originales E2/E3. No es calificación oficial ni certificado de cumplimiento.

15 ablaciones verificadas. Último reporte del autor (22 de noviembre): 8301 y 8302 completas; 8303 entrenando época 1, lote 1500/4096 en Colab; 8304–8305 pendientes. Test final no completado. Reporte operativo, no monitoreo en vivo ni respaldo nuevo auditado.

## Fuentes y alcance

- Entregable2DeepLearningProject.pdf (65 páginas), SHA-256 `93499dcfda6a36d9621524a81821470017ba114ca6b08241a35de5a54f74a654`.
- Entregable3DeepLearningProject.pdf (60 páginas), SHA-256 `d6048aebd7b3db85a59231a5a89b01bc3f8ad8cb581a96b462e341d21ff1f364`.

Las 15 ablaciones y el piloto están verificados. No sustituyen el benchmark final ni demuestran superioridad. Las 65 evaluaciones de reserva y las 66 corridas de desarrollo son cortes diferentes. No se repiten por esta revisión. E1 y el ZIP entregado se conservan.

## PCam: respaldo y continuación

Réplica PCam parcial. Último estado comunicado por el autor el 26 de noviembre: 8301 y 8302 completas; 8303 con época 5 guardada; 8304 y 8305 pendientes. Test final no realizado. No es monitoreo en vivo.

La presentación no espera la finalización de PCam. Se conserva el rescate en Drive reportado como verificado por el autor: PCAM_RESCATE_20261126T095034Z_ebc76149.zip (1.311.195.781 bytes). El contenido de ese ZIP no fue auditado nuevamente por el dashboard. No se publica como réplica completa.

## Matriz E2

| ID | Requisito | Guía | Estado y condición de cierre |
|---|---|---|---|
| 01 | Problema, RQ, hipótesis y utilidad | Sección 1 | Documentado; cierre parcial. Responder cada RQ con cifras y límites del benchmark final. |
| 02 | Contrato de datos, particiones y fuga | Sección 10 | Parcial. Completar auditoría de pacientes/duplicados/transformaciones; documentar reserva expuesta y hashes. |
| 03 | EDA orientado a decisiones | Sección 2 | Parcial. Integrado con histología; cotejar todas las decisiones, segmentos y controles con los datos finales. |
| 04 | Búsqueda sistemática y PRISMA | Sección 3.1 | Parcial. Conservar consultas exactas, fechas, filtros y conteos en ≥2 bases primarias; búsquedas de mecanismos en ≥3 modalidades. arXiv es complemento. |
| 05 | Cribado y sensibilidad del ranking | Sección 3.1–3.2 | Parcial. 166 fichas; completar 12 textos no recuperados, tabla de puntuación total, exclusiones y sensibilidad. |
| 06 | Top 10 diverso | Sección 3.2 | Documentado; verificación bibliográfica parcial. Diez candidatos adicionales y tres bases integrados; completar campos NR y comprobar fuentes de cada ficha. |
| 07 | Fichas completas, diagramas y análisis crítico | Sección 3.3 | Parcial. Completar campos no reportados con fuentes verificadas, motivación y diagrama por modelo. |
| 08 | Gap y limitación cuantificada | Sección 3.4 y 5 | Parcial. Justificar limitación medible, hipótesis falsable y probar su presencia en ≥3 Top10. |
| 09 | Preregistro y control de decisiones | Sección 9 | Parcial. Distinguir decisiones previas de posteriores; congelar correcciones sin fingir preregistro retrospectivo. |
| 10 | Equidad de ajuste y búsqueda condicional | Sección 4.1–4.4,11,14 | Parcial. Cotejar presupuestos, espacios, regularización, criterio común y costo de búsqueda; 1000 arquitecturas solo donde aplique §14. |
| 11 | Auditoría de corridas y predicciones | Sección 4 | Parcial. 66 corridas / 330 archivos cotejados: predicciones, curvas y métricas verificadas. Pesos y reproducción independiente pendientes. Distintos de las 65 evaluaciones de reserva. |
| 12 | Repeticiones y potencia | Sección 4.3 y 9.2 | Piloto disponible; cierre parcial. MDE y potencia históricos para tres bases ×22 semillas integrados en capítulo 23; no justifican automáticamente las 13 arquitecturas ×5 de reserva. Cotejar supuestos y justificar R por potencia ≥0,80 o MDE/limitaciones para cada comparación final. No repetir las 65 evaluaciones cerradas. |
| 13 | Baselines trivial y clásico | Sección 4.1 | Evaluados; ajuste por verificar. estado.json del cierre 65 confirma mayoritaria y logística guardada evaluadas. Falta acreditar suficiencia del ajuste del clásico. |
| 14 | Costos y eficiencia | Sección 11.4 | Parcial. Costos GPU, parámetros, FLOPs y Pareto históricos integrados. Completar costo total de búsqueda y condiciones comparables. |
| 15 | Inferencia y agregación estadística | Sección 6.3,7.3,13 | Calculado con límites. Cierre 65 contiene contrastes, Holm, Friedman/Nemenyi y CD; integrar adecuación, potencia y tres pruebas admisibles por contraste. Reserva expuesta y seis pacientes limitan inferencia. |
| 16 | Ajuste/sobreajuste y sanidad | Sección 4.5 | Parcial. Sanidad positiva Inception (33 recortes) y brechas disponibles; completar controles exigidos de ajuste/sobreajuste y respetar dependencia por paciente. |
| 17 | Calibración y segmentos | Sección 4.5 | Parcial. ECE fijo/adaptativo, Brier y brechas integrados; pendiente/intercepto ya presentes; faltan calibración independiente e IC por subgrupo. |
| 18 | Robustez y dominio | Sección 4.6 | Parcial; evidencia por consolidar. Separar robustez histórica de la nueva evaluación; verificar tres severidades, curva e índice, cambio de dominio y remuestreo por paciente. |
| 19 | Explicabilidad y fidelidad | Sección 4.6 | Parcial; falla identificada. 144 mapas examinados; 48/48 de Inception constantes. Corregir explicación del modelo principal y verificar fidelidad/estabilidad. |
| 20 | Ablaciones del mejor modelo | Sección 4.6 | Ejecutada para tres intervenciones. 15 corridas de preprocesamiento E2 integradas; inferencia sin significación. No confundir con ablaciones CICO ni inferir equivalencia. |
| 21 | Incertidumbre y cobertura | Sección 12.2 | Parcial. Ensambles, entropía y riesgo-retención disponibles; faltan cobertura nominal/empírica y condicional cuando aplique. |
| 22 | Techo y margen gamma | Sección 12.1 | Pendiente. Estimar techo comparable y gamma; multi-rater es una opción, no la única permitida. No convertir kappa directamente en macro-F1. |
| 23 | Análisis de 100 errores/modelo | Sección 12.3 | Pendiente. Galería 36 casos no equivale a 100 errores adjudicados por modelo; faltan taxonomía excluyente, IC, errores compartidos y segmentos. |
| 24 | Paper guía y réplica PCam | Sección 5 | Continuación comunicada en Colab; cierre pendiente. Último reporte del autor (22 de noviembre): 8301 y 8302 completas; 8303 entrenando época 1, lote 1500/4096 en Colab; 8304–8305 pendientes. Test final no completado. Reporte operativo, no monitoreo en vivo ni respaldo nuevo auditado. El respaldo local auditado conserva 8301 completa y 8302 en época 19. El reporte posterior informa la finalización de 8302 y el inicio de 8303. No se repite lo completado; falta recibir y verificar el próximo respaldo y los resultados finales. |
| 25 | Reproducción independiente y entorno | Sección 8 | Parcial. Entorno y checkpoints conservados; bases auditadas numéricamente; faltan pesos y reproducción independiente. |
| 26 | Libro, resultados y entrega | Entregables, pp. 58–59 | Publicado; cierre científico parcial. Libro/dashboard E3 integran E1/E2; no modificar el ZIP E2 entregado. Correcciones se documentan en nueva versión E3. |
| 27 | Sustentación y autoría | Sección requisitos finales | Pendiente de acreditación. Ensayo y defensa técnica por el autor; no se certifican por disponer de un guion. |
## Matriz E3

| ID | Requisito | Guía | Estado y condición de cierre |
|---|---|---|---|
| A | Correcciones E2 (7%) | §4, pp.4–5 | Parcial. Parcial: 16.588 imágenes verificadas por hash; cero cruces nominales de paciente/campo/píxeles entre particiones del paquete E3. Falta auditoría de decisiones históricas, duplicados aproximados, impacto de correcciones E2 y ranking antes/después. |
| B | Configuraciones y exportación (7%) | §5, pp.5–7 | Parcial. Parcial: exportación CICO ONNX y round-trip verificados, costo CPU medido. Faltan exportaciones de comparadores y política final común. |
| C | Dashboard: contexto y EDA (8%) | §9.4.1–2, p.32 | Parcial. Contexto, histología y tres gráficos EDA con filtros compartidos publicados. Pendiente QA tablet y accesibilidad. |
| D | Dashboard: modelos (9%) | §9.4.3, pp.33–34 | Parcial. Parcial: CICO con predicción CPU, oclusión y seis ejemplos precalculados; control descriptivo de eliminación/inserción frente a diez órdenes aleatorios y rotación 90°. Faltan comparadores, calibración/cobertura, detector OOD y fidelidad/estabilidad sobre muestra independiente de toda la familia. |
| E | Diseño, UX y despliegue (5%) | §9.5–10, pp.34–37 | Parcial. Parcial: prueba WSGI local de 180 predicciones sin errores, memoria RSS y latencias p50/p95, 72 rutas histológicas y recuperación tras entradas inválidas verificadas; CI remoto confirmado para 99db2bd. Falta QA real tablet/accesibilidad integral y medir memoria/carga del contenedor Render. |
| F | Original: revisión y diseño (8%) | §6.3–7, pp.11–20 | Parcial. 15 consultas ejecutadas: cinco cadenas en Europe PMC, Crossref y OpenAlex; 149 registros y 148 únicos. Recuperación truncada a diez por consulta. Pendientes cribado, textos completos, snowballing, contraste de antecedentes y tercero; no acredita novedad. |
| G | Original: implementación y demostración (10%) | §6.5 y 7.4, pp.13–20 | Parcial. Formulación y pruebas matemáticas documentadas; 15 ablaciones verificadas. Siete controles implementados con ocho pruebas de identidad, invariancia y gradientes; aún falta entrenar base/componentes/controles bajo protocolo común y evaluar capacidad activa y potencia. |
| H | Evaluación ampliada (10%) | §8.3 y 8.8, pp.23,28–29 | Parcial. Pendiente: 3 datasets adicionales auditados que difieran en ≥2 ejes, misma tarea, toda la familia; sensibilidad, perturbaciones, escalabilidad y cambio de dominio. |
| I | Hipótesis y adecuación (15%) | §8, pp.21–29 | Parcial. Piloto CICO y 15 ablaciones verificados. Escenarios de planificación aproximada disponibles, sin acreditar potencia conjunta. Final pendiente: familia completa ≥10 semillas o más según potencia ≥0,90, pruebas admisibles, Holm, IC/efectos y prueba independiente; sin superioridad acreditada. |
| J | Jupyter Book (14%) | §11–12 y tabla7, pp.38–40,58 | Parcial. Parcial: libro compilado e integrado; fichas y citación preparadas. Pendientes resultados confirmatorios, tabla maestra final, licencia, DOI, autoría firmada, protocolo/tag previo a nuevas corridas y reproducción independiente. |
| K | Sustentación (7%) | §13, pp.40–41 | Parcial. Pendiente: exposición 20 minutos, demostración y explicación/modificación en vivo por el autor; diapositivas y ensayo final. |

## Decisiones de cierre

1. Recibir el próximo respaldo PCam y verificarlo antes de actualizar resultados. El último inventario no es seguimiento en vivo.
2. Congelar protocolo, partición independiente y datos externos antes de nuevas evaluaciones confirmatorias. La reserva histórica expuesta no puede volver a sellarse.
3. Completar revisión humana de errores, literatura, licencia, autoría y reproducción por tercero. Estos pendientes no se solucionan con GPU.
4. Validar controles, estadísticas, exportaciones y demostración; generar una nueva entrega con hashes sin reemplazar el ZIP anterior.

[Resultados de ablaciones](15_ablaciones_y_transicion.md) · [Estado resumido](14_estado_entrega.md) · [Análisis CPU](18_cierre_cpu.md).
