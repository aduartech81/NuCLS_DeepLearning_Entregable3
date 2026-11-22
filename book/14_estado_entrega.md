# Estado de entrega: evidencia y pendientes

22 noviembre 2026 · auditoría documental contra las guías originales E2/E3

15 ablaciones verificadas. Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado.

El corte documental no acredita envío ni cumplimiento total; la meta interna anterior no es una fecha oficial.

[Auditoría detallada E2/E3](17_auditoria_cierre.md).

## E1 · Integración de evidencia

**Estado:** Integrado.

**Evidencia:** Tres bases × 11 semillas; confusión, calibración, selección de clases y flujo de literatura.

**Pendiente:** Conservar las diferencias entre el corte E1 y el manifiesto V2; no modificar originales.

**Dependencia:** Documentación

## E2 · Benchmark histórico y correcciones

**Estado:** Integrado con límites.

**Evidencia:** 13 arquitecturas × 5 en reserva; 22 semillas de las bases, 15 ablaciones de preprocesamiento y ensambles.

**Pendiente:** Verificación independiente de reproducibilidad y pesos; las 66 corridas base y 330 archivos ya se auditaron. No confundir con 65 evaluaciones de reserva.

**Dependencia:** Archivos E2

## E2 · PCam

**Estado:** Continuación en Colab comunicada por el autor.

**Evidencia:** Respaldo verificado del 22 de noviembre: 8301 completa; 8302 con época 19 guardada; 8303–8305 pendientes en ese corte. El autor comunica continuación en Colab; no es monitoreo en vivo ni un resultado nuevo verificado.

**Pendiente:** Desde ese respaldo quedan 61 épocas (1 de 8302 y 60 de 8303–8305), más test y resumen. Se omiten semillas completas y se recuperan pesos, optimizador y estados aleatorios; no se repite lo guardado. Evaluar test con política congelada y contrastar con el artículo.

**Dependencia:** GPU y checkpoints E2

## E2 · Histología y análisis de errores

**Estado:** Parcial.

**Evidencia:** 36 núcleos, 21 pacientes, 18 aciertos y 18 discrepancias de tres modelos; huellas cotejadas.

**Pendiente:** 100 errores por modelo principal con taxonomía/IC, errores compartidos y techo comparable (la guía admite acuerdo multi-rater u otra cota justificada); calcular distancia gamma.

**Dependencia:** Revisión humana y anotaciones

## E2 · Explicabilidad y fidelidad

**Estado:** Parcial.

**Evidencia:** 48/48 mapas Inception constantes en evidencia anterior; no se presentan como explicaciones válidas.

**Pendiente:** Corregir capa o método y repetir fidelidad/estabilidad; completar incertidumbre y cobertura no acreditadas.

**Dependencia:** Modelos entrenados y evaluación

## E3 A · Correcciones, fuga y congelación

**Estado:** Parcial.

**Evidencia:** Historial de exposición de reserva declarado y fuentes preservadas.

**Pendiente:** Auditar archivos primarios completos, pacientes/duplicados/versiones y congelar paquete final con hashes.

**Dependencia:** Archivos y auditoría

## E3 B/D · Exportación e inferencia CPU

**Estado:** CICO publicado y probado en Render.

**Evidencia:** CICO 6101 exportado; 2.049/2.049 clases idénticas a RunPod usando las imágenes originales; hash ONNX y 7 pruebas de entradas/integridad. Prueba pública desde Safari: tumor 93,7%, linfocito 2,5%, estroma 3,8%; rechazo de dimensiones incorrectas y confirmación obligatoria verificados.

**Pendiente:** Exportar comparadores bajo política común y selector; calibración independiente, cobertura, detector OOD y fidelidad/estabilidad. Oclusión local y latencia CPU ya disponibles; falta prueba de memoria/carga.

**Dependencia:** Artefactos entrenados

## E3 C/E · Dashboard e integración visual

**Estado:** Publicado; verificación parcial.

**Evidencia:** NuCLEA publicado: histología, ejemplos reales, carga y predicción, curvas y comparación de 15 ablaciones. 72 vistas histológicas verificadas.

**Pendiente:** QA real tablet/móvil y accesibilidad integral; costos/diagnósticos para cada modelo seleccionable. Tres gráficos EDA ya comparten filtros.

**Dependencia:** QA web y modelo

## E3 F · Originalidad y revisión externa

**Estado:** Parcial.

**Evidencia:** Antecedentes cercanos y alcance de lectura declarados.

**Pendiente:** Completar evidencia de 3 bases/5 cadenas/snowballing, textos pendientes, fuente/adaptación y evaluación por tercero; no declarar novedad probada.

**Dependencia:** Búsqueda y revisión humana

## E3 G · Mecanismo y ablaciones propias

**Estado:** 15 ablaciones verificadas; controles adicionales pendientes.

**Evidencia:** 91 archivos verificados; 15 variantes y 5 CICO comparados sobre 2049 imágenes de 21 pacientes.

**Pendiente:** Base sin todos los componentes, cada componente solo, controles D4/capacidad y benchmark confirmatorio.

**Dependencia:** Entrenamiento adicional

## E3 H · Tres conjuntos adicionales

**Estado:** Pendiente.

**Evidencia:** PanNuke, Lizard y MoNuSAC son candidatos, no datasets externos auditados.

**Pendiente:** Auditar solapamiento/etiquetas/licencia, diferencias en ≥2 ejes; evaluar toda la familia con presupuestos comparables, perturbaciones y escalabilidad.

**Dependencia:** Datos y GPU

## E3 I · Piloto de cinco semillas

**Estado:** Completo y verificado.

**Evidencia:** Cinco checkpoints y predicciones cotejados; 2.049 imágenes / 21 pacientes por semilla; macro-F1 recalculado.

**Pendiente:** No requiere repetir entrenamiento. Conservar archivos y separar piloto de evaluación final.

**Dependencia:** Ninguna para cerrar recepción del piloto

## E3 I · Benchmark final y potencia

**Estado:** Pendiente.

**Evidencia:** Cinco semillas piloto no cumplen la evaluación final.

**Pendiente:** Dimensionar por potencia al 90 % y mínimo ≥10; toda la familia, ≥3 pruebas por contraste, Holm, máximo p ajustado y potencia conjunta.

**Dependencia:** Diseño, entrenamiento y estadística

## E3 J · Libro y tabla maestra

**Estado:** Integrado; cierre pendiente.

**Evidencia:** Histología, tablas E1/E2 y cinco resultados CICO verificados integrados; misma fuente para libro/dashboard.

**Pendiente:** Resultados confirmatorios y tabla completa; fichas MODEL_CARD/DATA_STATEMENT y CITATION ya preparadas, falta validación final, licencia, protocolo/tag previo a nuevas corridas, DOI, autoría firmada y reproducción por tercero.

**Dependencia:** Resultados finales y tercero

## E3 K · Sustentación

**Estado:** Guion disponible; no ensayada.

**Evidencia:** Problema/datos, antecedentes, mecanismo, resultados y demostración.

**Pendiente:** Preparar diapositivas definitivas, ensayar demostración y explicación/modificación del mecanismo; respaldo local comprobado.

**Dependencia:** Autor

## Entrega · Congelación y envío final

**Estado:** Pendiente.

**Evidencia:** Portal accesible; paquete previo no equivale al paquete final de esta revisión.

**Pendiente:** Congelar versión, descargar respaldo independiente, generar hashes, revisar enlaces y adjuntos y enviar por el canal oficial.

**Dependencia:** Autor y paquete final
