# Auditoría contra las guías originales E2 y E3

Revisión del 21 de noviembre de 2026, posterior al plazo indicado de las 10:00 (Bogotá). No acredita envío ni cumplimiento total. Fuentes: **Entregable2DeepLearningProject.pdf (65 páginas)** y **Entregable3DeepLearningProject.pdf (60 páginas)** suministrados por el autor. Las letras A–K de esta tabla corresponden a la rúbrica E3, no a los nombres de bloques de sus capítulos. Las huellas de las guías y la matriz completa están en `data/auditoria_cierre.json`.

## Conclusión de cierre

E2 y E3 siguen abiertos científicamente. El dashboard, la galería histológica, el libro integrado y la predicción CPU CICO están publicados; publicar no sustituye los experimentos exigidos. Las cinco semillas CICO piloto están verificadas. Las 65 evaluaciones de reserva E2 tienen cierre estadístico recibido y baselines evaluados: no deben repetirse por el antiguo error NaN. Esto es distinto de verificar las 66 corridas de desarrollo y de completar PCam.

**Las 15 ablaciones actuales no cubren por sí solas toda la sección 7.4 de E3:** faltan el modelo base sin componentes propios y cada componente añadido solo; además, control sin D4 y tamaño igualado cuando corresponda. No se modifica la cola en curso. El piloto completo tampoco satisface el benchmark final (mínimo diez semillas para cada integrante de la familia, o más según potencia).

## Secuencia de trabajo

1. Dejar terminar la cola actual; recibir las 15 corridas con checkpoints, predicciones, historias y configuración. Verificar hashes y comparar variantes emparejadas, sin sustituir faltantes por ceros.
2. Respaldar E3 fuera del Pod. Con cola completa y GPU libre, usar el cuaderno PCam revisado; no ejecutar todo ni compartir entorno de dependencias.
3. PCam: omitir 8301 ya completa; cargar pesos, optimizador y estados aleatorios de 8302 y continuar desde la época siguiente al checkpoint (historia recibida: 16). Completar 8303–8305. Quedan 64 épocas según el inventario, más descarga y test; medir la primera época en RunPod antes de estimar tiempo. Los tiempos de Colab no predicen el rendimiento de la L4.
4. Después de las cinco semillas, verificar test y resumen PCam y redactar discrepancia frente al paper. Es una réplica parcial con diferencias técnicas declaradas, no prueba automática de réplica exacta.
5. Diseñar y congelar la evaluación final E3 antes de correrla: familia completa, partición de confirmación no usada para diseño, potencia y tres conjuntos externos. La reserva histórica expuesta no puede volverse sellada retrospectivamente.
6. Completar análisis humanos, artefactos, fichas, reproducción externa y defensa. Congelar una nueva entrega con hashes y revisión de enlaces; conservar E1 y el ZIP entregado.

## Matriz de cumplimiento

### E2

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
| 11 | Auditoría de corridas y predicciones | Sección 4 | Parcial. 66 registros de desarrollo disponibles; falta cerrar cotejo de todas las predicciones y curvas. Distintos de las 65 evaluaciones de reserva. |
| 12 | Repeticiones y potencia | Sección 4.3 y 9.2 | Piloto disponible; cierre parcial. 13 arquitecturas × 5 en reserva; justificar R por potencia ≥0,80 o declarar MDE y límites. No repetir las 65 evaluaciones ya cerradas. |
| 13 | Baselines trivial y clásico | Sección 4.1 | Evaluados; ajuste por verificar. estado.json del cierre 65 confirma mayoritaria y logística guardada evaluadas. Falta acreditar suficiencia del ajuste del clásico. |
| 14 | Costos y eficiencia | Sección 11.4 | Parcial. Costos GPU, parámetros, FLOPs y Pareto históricos integrados. Completar costo total de búsqueda y condiciones comparables. |
| 15 | Inferencia y agregación estadística | Sección 6.3,7.3,13 | Calculado con límites. Cierre 65 contiene contrastes, Holm, Friedman/Nemenyi y CD; integrar adecuación, potencia y tres pruebas admisibles por contraste. Reserva expuesta y seis pacientes limitan inferencia. |
| 16 | Ajuste/sobreajuste y sanidad | Sección 4.5 | Parcial. Sanidad positiva Inception (33 recortes) y brechas disponibles; completar controles exigidos de ajuste/sobreajuste y respetar dependencia por paciente. |
| 17 | Calibración y segmentos | Sección 4.5 | Parcial. ECE fijo/adaptativo, Brier y brechas integrados; pendiente calibración independiente, pendiente/intercepto e IC por subgrupo. |
| 18 | Robustez y dominio | Sección 4.6 | Parcial; evidencia por consolidar. Separar robustez histórica de la nueva evaluación; verificar tres severidades, curva e índice, cambio de dominio y remuestreo por paciente. |
| 19 | Explicabilidad y fidelidad | Sección 4.6 | Parcial; falla identificada. 144 mapas examinados; 48/48 de Inception constantes. Corregir explicación del modelo principal y verificar fidelidad/estabilidad. |
| 20 | Ablaciones del mejor modelo | Sección 4.6 | Ejecutada para tres intervenciones. 15 corridas de preprocesamiento E2 integradas; inferencia sin significación. No confundir con ablaciones CICO ni inferir equivalencia. |
| 21 | Incertidumbre y cobertura | Sección 12.2 | Parcial. Ensambles, entropía y riesgo-retención disponibles; faltan cobertura nominal/empírica y condicional cuando aplique. |
| 22 | Techo y margen gamma | Sección 12.1 | Pendiente. Estimar techo comparable y gamma; multi-rater es una opción, no la única permitida. No convertir kappa directamente en macro-F1. |
| 23 | Análisis de 100 errores/modelo | Sección 12.3 | Pendiente. Galería 36 casos no equivale a 100 errores adjudicados por modelo; faltan taxonomía excluyente, IC, errores compartidos y segmentos. |
| 24 | Paper guía y réplica PCam | Sección 5 | PCam detenido; recuperación preparada. 8301 completa; 8302 guardada en 16; faltan 4 épocas de 8302 y 60 de 8303–8305, más evaluación. Reportar discrepancia/IC respecto del paper y limitación cuantificada en ≥3 modelos. |
| 25 | Reproducción independiente y entorno | Sección 8 | Parcial. Entorno y checkpoints conservados; faltan reproducción independiente, auditoría completa de bases y comparación numérica. |
| 26 | Libro, resultados y entrega | Entregables, pp. 58–59 | Publicado; cierre científico parcial. Libro/dashboard E3 integran E1/E2; no modificar el ZIP E2 entregado. Correcciones se documentan en nueva versión E3. |
| 27 | Sustentación y autoría | Sección requisitos finales | Pendiente de acreditación. Ensayo y defensa técnica por el autor; no se certifican por disponer de un guion. |

### E3

| ID | Requisito | Guía | Estado y condición de cierre |
|---|---|---|---|
| A | Correcciones E2 (7%) | §4, pp.4–5 | Parcial / pendiente. Parcial: completar observación–acción–evidencia–impacto, ranking antes/después y auditoría de fuga; congelar benchmarks sin reajuste con reserva. |
| B | Configuraciones y exportación (7%) | §5, pp.5–7 | Parcial / pendiente. Parcial: CICO 6101 ONNX verificado y publicado. Falta selección por configuración media, política común de reentrenamiento/exportación de comparadores, costos CPU y metadatos completos. |
| C | Dashboard: contexto y EDA (8%) | §9.4.1–2, p.32 | Parcial / pendiente. Parcial: contexto/EDA/histología publicados. EDA tiene selector de característica, pero no filtros globales que actualicen todos los gráficos; falta QA tablet. |
| D | Dashboard: modelos (9%) | §9.4.3, pp.33–34 | Parcial / pendiente. Parcial: subida y predicción CICO funcionan. Faltan selector de modelos, calibración, cobertura, explicación local, detección fuera de dominio, latencia y comparación final completa. |
| E | Diseño, UX y despliegue (5%) | §9.5–10, pp.34–37 | Parcial / pendiente. Parcial: Render probado y entrada validada; falta QA tablet/accesibilidad/memoria, consistencia automática y revisión CI. La guía pide dash-bootstrap-components, no instalado actualmente. |
| F | Original: revisión y diseño (8%) | §6.3–7, pp.11–20 | Parcial / pendiente. Parcial: matriz y antecedentes existentes; falta acreditar 3 bases/5 cadenas, snowballing, actualización de búsqueda y tercero. No declarar novedad demostrada. |
| G | Original: implementación y demostración (10%) | §6.5 y 7.4, pp.13–20 | Parcial / pendiente. Parcial: implementación y pruebas previas. Cola de 15 ablaciones en curso según último reporte; también faltan base sin componentes, componentes solos, controles de capacidad y explicación/fidelidad. |
| H | Evaluación ampliada (10%) | §8.3 y 8.8, pp.23,28–29 | Parcial / pendiente. Pendiente: 3 datasets adicionales auditados que difieran en ≥2 ejes, misma tarea, toda la familia; sensibilidad, perturbaciones, escalabilidad y cambio de dominio. |
| I | Hipótesis y adecuación (15%) | §8, pp.21–29 | Parcial / pendiente. Piloto CICO completo (5). Final pendiente: ≥10 semillas para toda la familia o más por potencia ≥0,90, ≥3 pruebas/contraste, Holm, máximo p ajustado, IC/efectos y potencia conjunta. No hay superioridad acreditada. |
| J | Jupyter Book (14%) | §11–12 y tabla7, pp.38–40,58 | Parcial / pendiente. Parcial: libro compilado/publicado e integrado. Faltan contenidos experimentales finales, tabla maestra completa, protocolo final/tag previo, fichas, DOI, autoría firmada y reproducción independiente. |
| K | Sustentación (7%) | §13, pp.40–41 | Pendiente. Pendiente: exposición 20 minutos, demostración y explicación/modificación en vivo por el autor; diapositivas y ensayo final. |

## Lo que no resuelven más horas de GPU

La adjudicación de 100 errores por modelo, una cota de techo comparable, las búsquedas y concepto independiente de novedad, la firma de autoría, el DOI, el ensayo y la reproducción por un tercero requieren trabajo adicional. No se declaran realizados por disponer de scripts. La búsqueda de 1.000 arquitecturas en E2 es condicional a no tener diseño predefinido (§14); no es una corrida nueva obligatoria para toda arquitectura publicada.

## Estado de la función predictiva

[Analizar imagen en Render](https://nucls-entregable3.onrender.com/prediccion): PNG/JPEG RGB 128×128 hasta 2 MB. CICO 6101 exportado y cotejado en 2.049 imágenes; prueba de carga pública desde Safari, probabilidades conocidas, rechazo de tamaño y confirmación verificados. No hay aún calibración validada, explicación local ni detector de dominio: el aviso de uso experimental no reemplaza estos requisitos.

[Exportación y pruebas](16_exportacion_inferencia.md) · [Estado resumido](14_estado_entrega.md).
