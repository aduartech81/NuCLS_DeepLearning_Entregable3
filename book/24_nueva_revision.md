# E3: versión para nueva revisión

**Corte documental: 22 de noviembre de 2026. Estado: revisión de avance, no cierre confirmatorio.**

## Qué se solicita revisar

Se presenta la integración de NuCLEA y el libro, la trazabilidad de resultados y las correcciones implementadas. No se solicita dar por cumplidos los experimentos faltantes ni se atribuye una calificación al docente.

## Evidencia disponible

- Cinco semillas piloto CICO y quince ablaciones verificadas (tres variantes por cinco semillas).
- Tabla maestra común, análisis pareado y ajuste de Holm; evidencia exploratoria en validación compartida.
- Formulación y demostración de invariancia por promedio de la órbita D4 y cota de corrección contextual en el capítulo 5. La cota no demuestra robustez global ni mejor generalización.
- Inferencia CPU con exportación ONNX y concordancia de clases en 2049/2049 imágenes. Histología real, anotaciones y seis ejemplos con referencia y explicación.
- Controles descriptivos de eliminación/inserción frente a diez órdenes aleatorios y rotación de 90 grados, sobre seis ejemplos; no sustituyen una evaluación independiente de explicaciones.
- Separación explícita entre predicción, referencia, probabilidad no calibrada y limitaciones de uso.

## Resultado que sí puede afirmarse

El piloto CICO obtuvo macro-F1 medio **0,66824**, desviación entre semillas **0,03720**. Sin contraste obtuvo **0,67914**, sin amortiguación **0,66105** y sin contexto **0,66255**. Los p ajustados de los contrastes exploratorios fueron **0,375; 1; 1**, respectivamente. No se demuestra superioridad de CICO; tampoco equivalencia. No son resultados de test confirmatorio independiente.

## Estado frente a los bloques de la guía

| Bloque | Componente | Peso de la guía | Estado y condición de cierre |
|---|---|---:|---|
| A | Correcciones E2 | 7 | Parcial: 16.588 imágenes verificadas por hash; cero cruces nominales de paciente/campo/píxeles entre particiones del paquete E3. Falta auditoría de decisiones históricas, duplicados aproximados, impacto de correcciones E2 y ranking antes/después. |
| B | Configuraciones y exportación | 7 | Parcial: exportación CICO ONNX y round-trip verificados, costo CPU medido. Faltan exportaciones de comparadores y política final común. |
| C | Dashboard: contexto y EDA | 8 | Contexto, histología y tres gráficos EDA con filtros compartidos publicados. Pendiente QA tablet y accesibilidad. |
| D | Dashboard: modelos | 9 | Parcial: CICO con predicción CPU, oclusión y seis ejemplos precalculados; control descriptivo de eliminación/inserción frente a diez órdenes aleatorios y rotación 90°. Faltan comparadores, calibración/cobertura, detector OOD y fidelidad/estabilidad sobre muestra independiente de toda la familia. |
| E | Diseño, UX y despliegue | 5 | Parcial: prueba WSGI local de 180 predicciones sin errores, memoria RSS y latencias p50/p95, 72 rutas histológicas y recuperación tras entradas inválidas verificadas; CI remoto confirmado para 99db2bd. Falta QA real tablet/accesibilidad integral y medir memoria/carga del contenedor Render. |
| F | Original: revisión y diseño | 8 | 15 consultas ejecutadas: cinco cadenas en Europe PMC, Crossref y OpenAlex; 149 registros y 148 únicos. Recuperación truncada a diez por consulta. Pendientes cribado, textos completos, snowballing, contraste de antecedentes y tercero; no acredita novedad. |
| G | Original: implementación y demostración | 10 | Formulación y pruebas matemáticas documentadas; 15 ablaciones verificadas. Siete controles implementados con ocho pruebas de identidad, invariancia y gradientes; aún falta entrenar base/componentes/controles bajo protocolo común y evaluar capacidad activa y potencia. |
| H | Evaluación ampliada | 10 | Pendiente: 3 datasets adicionales auditados que difieran en ≥2 ejes, misma tarea, toda la familia; sensibilidad, perturbaciones, escalabilidad y cambio de dominio. |
| I | Hipótesis y adecuación | 15 | Piloto CICO y 15 ablaciones verificados. Escenarios de planificación aproximada disponibles, sin acreditar potencia conjunta. Final pendiente: familia completa ≥10 semillas o más según potencia ≥0,90, pruebas admisibles, Holm, IC/efectos y prueba independiente; sin superioridad acreditada. |
| J | Jupyter Book | 14 | Parcial: libro compilado e integrado; fichas y citación preparadas. Pendientes resultados confirmatorios, tabla maestra final, licencia, DOI, autoría firmada, protocolo/tag previo a nuevas corridas y reproducción independiente. |
| K | Sustentación | 7 | Pendiente: exposición 20 minutos, demostración y explicación/modificación en vivo por el autor; diapositivas y ensayo final. |

Los pesos no son notas obtenidas. La matriz detallada y los localizadores de la guía están en el capítulo 17; no se suman como una calificación.

## Orden para cerrar las brechas

1. **Congelar un protocolo prospectivo**: familia de modelos, partición independiente, hipótesis, presupuestos, semillas, métricas y política de selección. Revisar primero la disponibilidad de los tres conjuntos externos; no llamar “nuevo test” a una reserva ya usada para decisiones.
2. **Completar la evidencia experimental**: base sin componentes, componentes aislados y controles D4/capacidad; familia completa y número de semillas justificado; evaluación externa, incertidumbre y contrastes con potencia requerida. Esto requiere datos y cómputo adicional.
3. **PCam se presenta como réplica parcial**: según el reporte del autor del 26 de noviembre, 8301 y 8302 están completas, 8303 tiene época 5 guardada y 8304/8305 siguen pendientes. Test final no realizado. La entrega no espera a PCam y conserva su respaldo. Esta información operativa no equivale a una auditoría nueva de checkpoints.
4. **Completar documentación y validación humana**: búsquedas/fichas y revisión por tercero, análisis de errores, permisos/licencia, DOI, autoría firmada, reproducción independiente y sustentación de 20 minutos. No se pueden sustituir con declaraciones automáticas.
5. **Cerrar producto**: incorporar comparadores, calibración/cobertura y OOD validados; comprobar tablet, accesibilidad y carga. La inferencia CICO disponible es una demostración de investigación.

## Ubicación de evidencias

- [Formulación y límites](05_modelo_diseno.md).
- [Ablaciones verificadas](15_ablaciones_y_transicion.md).
- [Exportación e inferencia](16_exportacion_inferencia.md).
- [Auditoría de requisitos](17_auditoria_cierre.md).
- [Tabla maestra](21_tabla_maestra.md).
- [Explicaciones: controles CPU](22_calidad_explicaciones.md).
- [Planificación de potencia](23_planificacion_potencia.md).

La versión mantiene los resultados históricos de E1 y E2 como evidencia de sus propias poblaciones. No mezcla sus métricas con las de CICO ni modifica el ZIP entregado. Las nuevas correcciones documentales no cambian los pesos del modelo.

[Comprobaciones ejecutadas sin GPU](25_comprobaciones_sin_gpu.md).

[Búsqueda ejecutada](26_busqueda_ejecutada.md).
