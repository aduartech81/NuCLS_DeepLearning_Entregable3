# Estado de entrega: evidencia y pendientes

21 noviembre 2026 · revisión directa de las guías E2 (65 páginas) y E3 (60 páginas); inferencia pública comprobada

Respaldo de 15 ablaciones verificado y métricas recalculadas. PCam reanudado, último avance comunicado: época 17 lote 3500/4096. No es monitoreo en vivo ni cierre experimental total.

Meta de trabajo original: 21 noviembre 2026 a las 10:00; no representa la fecha oficial de la plataforma.

[Auditoría detallada E2/E3](17_auditoria_cierre.md).

## E1 · Integración de evidencia

**Estado:** Integrado.

**Evidencia:** Tres bases × 11 semillas; confusión, calibración, selección de clases y flujo de literatura.

**Pendiente:** Conservar las diferencias entre el corte E1 y el manifiesto V2; no modificar originales.

## E2 · Benchmark histórico y correcciones

**Estado:** Integrado con límites.

**Evidencia:** 13 arquitecturas × 5 en reserva; 22 semillas de las bases, 15 ablaciones de preprocesamiento y ensambles.

**Pendiente:** Verificación independiente de reproducibilidad y pesos; las 66 corridas base y 330 archivos ya se auditaron. No confundir con 65 evaluaciones de reserva.

## E2 · PCam

**Estado:** Reanudado desde checkpoint.

**Evidencia:** 8301 completa; 8302 época 17 lote 3500/4096, última época guardada 16. Proceso 8496 según salida comunicada.

**Pendiente:** Completar 8302–8305, evaluar test con política congelada y comparar la réplica con el artículo.

## E2 · Histología y análisis de errores

**Estado:** Parcial.

**Evidencia:** 36 núcleos, 21 pacientes, 18 aciertos y 18 discrepancias de tres modelos; huellas cotejadas.

**Pendiente:** 100 errores por modelo principal con taxonomía/IC, errores compartidos y techo comparable (la guía admite acuerdo multi-rater u otra cota justificada); calcular distancia gamma.

## E2 · Explicabilidad y fidelidad

**Estado:** Parcial.

**Evidencia:** 48/48 mapas Inception constantes en evidencia anterior; no se presentan como explicaciones válidas.

**Pendiente:** Corregir capa o método y repetir fidelidad/estabilidad; completar incertidumbre y cobertura no acreditadas.

## E3 A · Correcciones, fuga y congelación

**Estado:** Parcial.

**Evidencia:** Historial de exposición de reserva declarado y fuentes preservadas.

**Pendiente:** Auditar archivos primarios completos, pacientes/duplicados/versiones y congelar paquete final con hashes.

## E3 B/D · Exportación e inferencia CPU

**Estado:** CICO publicado y probado en Render.

**Evidencia:** CICO 6101 exportado; 2.049/2.049 clases idénticas a RunPod usando las imágenes originales; hash ONNX y 7 pruebas de entradas/integridad. Prueba pública desde Safari: tumor 93,7%, linfocito 2,5%, estroma 3,8%; rechazo de dimensiones incorrectas y confirmación obligatoria verificados.

**Pendiente:** Exportar comparadores bajo política común, selector, probabilidades calibradas, incertidumbre con cobertura, explicación local, detección fuera de dominio y latencia/memoria del servidor.

## E3 C/E · Dashboard e integración visual

**Estado:** Publicado; verificación parcial.

**Evidencia:** Portal integrado, histología, filtros por página y libro; pruebas locales y escritorio.

**Pendiente:** Filtros globales para todos los gráficos de EDA, QA tablet/móvil, tabla completa con costos y diagnósticos del modelo elegido. La predicción CICO básica ya funciona.

## E3 F · Originalidad y revisión externa

**Estado:** Parcial.

**Evidencia:** Antecedentes cercanos y alcance de lectura declarados.

**Pendiente:** Completar evidencia de 3 bases/5 cadenas/snowballing, textos pendientes, fuente/adaptación y evaluación por tercero; no declarar novedad probada.

## E3 G · Mecanismo y ablaciones propias

**Estado:** 15 ablaciones verificadas; controles adicionales pendientes.

**Evidencia:** 91 archivos verificados; 15 variantes y 5 CICO comparados sobre 2049 imágenes de 21 pacientes.

**Pendiente:** Base sin todos los componentes, cada componente solo, controles D4/capacidad y benchmark confirmatorio.

## E3 H · Tres conjuntos adicionales

**Estado:** Pendiente.

**Evidencia:** PanNuke, Lizard y MoNuSAC son candidatos, no datasets externos auditados.

**Pendiente:** Auditar solapamiento/etiquetas/licencia, diferencias en ≥2 ejes; evaluar toda la familia con presupuestos comparables, perturbaciones y escalabilidad.

## E3 I · Piloto de cinco semillas

**Estado:** Completo y verificado.

**Evidencia:** Cinco checkpoints y predicciones cotejados; 2.049 imágenes / 21 pacientes por semilla; macro-F1 recalculado.

**Pendiente:** No requiere repetir entrenamiento. Conservar archivos y separar piloto de evaluación final.

## E3 I · Benchmark final y potencia

**Estado:** Pendiente.

**Evidencia:** Cinco semillas piloto no cumplen la evaluación final.

**Pendiente:** Dimensionar por potencia al 90 % y mínimo ≥10; toda la familia, ≥3 pruebas por contraste, Holm, máximo p ajustado y potencia conjunta.

## E3 J · Libro y tabla maestra

**Estado:** Integrado; cierre pendiente.

**Evidencia:** Histología, tablas E1/E2 y cinco resultados CICO verificados integrados; misma fuente para libro/dashboard.

**Pendiente:** Benchmark final y tabla maestra completa; fichas MODEL_CARD/DATA_STATEMENT, CITATION/licencia, protocolo final con tag previo, DOI, autoría firmada y reproducción por tercero. Contenedor web existente no acredita reproducción independiente.

## E3 K · Sustentación

**Estado:** Guion disponible; no ensayada.

**Evidencia:** Problema/datos, antecedentes, mecanismo, resultados y demostración.

**Pendiente:** Preparar diapositivas definitivas, ensayar demostración y explicación/modificación del mecanismo; respaldo local comprobado.

## Entrega · Congelación y envío final

**Estado:** Pendiente.

**Evidencia:** Portal accesible; paquete previo no equivale al paquete final de esta revisión.

**Pendiente:** Congelar versión, descargar respaldo independiente, generar hashes, revisar enlaces y adjuntos y enviar por el canal oficial.
