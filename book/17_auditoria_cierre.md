# Auditoría contra las guías originales E2 y E3

22 noviembre 2026 · auditoría documental contra las guías originales E2/E3. No es calificación oficial ni certificado de cumplimiento.

15 ablaciones verificadas. Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado.

## Fuentes y alcance

- Entregable2DeepLearningProject.pdf (65 páginas), SHA-256 `93499dcfda6a36d9621524a81821470017ba114ca6b08241a35de5a54f74a654`.
- Entregable3DeepLearningProject.pdf (60 páginas), SHA-256 `d6048aebd7b3db85a59231a5a89b01bc3f8ad8cb581a96b462e341d21ff1f364`.

Las 15 ablaciones y el piloto están verificados. No sustituyen el benchmark final ni demuestran superioridad. Las 65 evaluaciones de reserva y las 66 corridas de desarrollo son cortes diferentes. No se repiten por esta revisión. E1 y el ZIP entregado se conservan.

## PCam: respaldo y continuación

Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado.

Desde ese respaldo quedan 61 épocas (1 de 8302 y 60 de 8303–8305), más test y resumen. Se omiten semillas completas y se recuperan pesos, optimizador y estados aleatorios; no se repite lo guardado.

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
| 12 | Repeticiones y potencia | Sección 4.3 y 9.2 | Piloto disponible; cierre parcial. 13 arquitecturas × 5 en reserva; justificar R por potencia ≥0,80 o declarar MDE y límites. No repetir las 65 evaluaciones ya cerradas. |
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
| 24 | Paper guía y réplica PCam | Sección 5 | Continuación comunicada en Colab; cierre pendiente. Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado. Desde ese respaldo quedan 61 épocas (1 de 8302 y 60 de 8303–8305), más test y resumen. Se omiten semillas completas y se recuperan pesos, optimizador y estados aleatorios; no se repite lo guardado. Test final, discrepancia e IC respecto del artículo pendientes. |
| 25 | Reproducción independiente y entorno | Sección 8 | Parcial. Entorno y checkpoints conservados; bases auditadas numéricamente; faltan pesos y reproducción independiente. |
| 26 | Libro, resultados y entrega | Entregables, pp. 58–59 | Publicado; cierre científico parcial. Libro/dashboard E3 integran E1/E2; no modificar el ZIP E2 entregado. Correcciones se documentan en nueva versión E3. |
| 27 | Sustentación y autoría | Sección requisitos finales | Pendiente de acreditación. Ensayo y defensa técnica por el autor; no se certifican por disponer de un guion. |
## Matriz E3

| ID | Requisito | Guía | Estado y condición de cierre |
|---|---|---|---|
| A | Correcciones E2 (7%) | §4, pp.4–5 | Parcial / pendiente. Parcial: completar observación–acción–evidencia–impacto, ranking antes/después y auditoría de fuga; congelar benchmarks sin reajuste con reserva. |
| B | Configuraciones y exportación (7%) | §5, pp.5–7 | Parcial / pendiente. Parcial: exportación CICO ONNX y round-trip verificados, costo CPU medido. Faltan exportaciones de comparadores y política final común. |
| C | Dashboard: contexto y EDA (8%) | §9.4.1–2, p.32 | Parcial / pendiente. Contexto, histología y tres gráficos EDA con filtros compartidos publicados. Pendiente QA tablet y accesibilidad. |
| D | Dashboard: modelos (9%) | §9.4.3, pp.33–34 | Parcial / pendiente. Subida y predicción CICO, explicación por oclusión y latencia publicadas. Faltan selector de comparadores, calibración/cobertura y detector OOD validado; aviso de dominio no equivale a detector. |
| E | Diseño, UX y despliegue (5%) | §9.5–10, pp.34–37 | Parcial / pendiente. Parcial: NuCLEA publicado, dash-bootstrap-components instalado, entradas e imágenes verificadas. Se añade consistencia automática libro/dashboard y CI con pruebas del modelo/exportación. Falta QA real tablet/accesibilidad integral y memoria/carga. |
| F | Original: revisión y diseño (8%) | §6.3–7, pp.11–20 | Parcial / pendiente. Parcial: matriz y antecedentes existentes; falta acreditar 3 bases/5 cadenas, snowballing, actualización de búsqueda y tercero. No declarar novedad demostrada. |
| G | Original: implementación y demostración (10%) | §6.5 y 7.4, pp.13–20 | Parcial / pendiente. 15 ablaciones verificadas, cinco semillas por variante. Faltan base sin componentes, componentes individuales, controles D4/capacidad y protocolo confirmatorio con potencia requerida. |
| H | Evaluación ampliada (10%) | §8.3 y 8.8, pp.23,28–29 | Parcial / pendiente. Pendiente: 3 datasets adicionales auditados que difieran en ≥2 ejes, misma tarea, toda la familia; sensibilidad, perturbaciones, escalabilidad y cambio de dominio. |
| I | Hipótesis y adecuación (15%) | §8, pp.21–29 | Parcial / pendiente. Piloto CICO completo (5). Final pendiente: ≥10 semillas para toda la familia o más por potencia ≥0,90, ≥3 pruebas/contraste, Holm, máximo p ajustado, IC/efectos y potencia conjunta. No hay superioridad acreditada. |
| J | Jupyter Book (14%) | §11–12 y tabla7, pp.38–40,58 | Parcial / pendiente. Parcial: libro compilado e integrado; fichas y citación preparadas. Pendientes resultados confirmatorios, tabla maestra final, licencia, DOI, autoría firmada, protocolo/tag previo a nuevas corridas y reproducción independiente. |
| K | Sustentación (7%) | §13, pp.40–41 | Pendiente. Pendiente: exposición 20 minutos, demostración y explicación/modificación en vivo por el autor; diapositivas y ensayo final. |

## Decisiones de cierre

1. Recibir el próximo respaldo PCam y verificarlo antes de actualizar resultados. El último inventario no es seguimiento en vivo.
2. Congelar protocolo, partición independiente y datos externos antes de nuevas evaluaciones confirmatorias. La reserva histórica expuesta no puede volver a sellarse.
3. Completar revisión humana de errores, literatura, licencia, autoría y reproducción por tercero. Estos pendientes no se solucionan con GPU.
4. Validar controles, estadísticas, exportaciones y demostración; generar una nueva entrega con hashes sin reemplazar el ZIP anterior.

[Resultados de ablaciones](15_ablaciones_y_transicion.md) · [Estado resumido](14_estado_entrega.md) · [Análisis CPU](18_cierre_cpu.md).
