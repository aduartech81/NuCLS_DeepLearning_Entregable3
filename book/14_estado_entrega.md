# Estado de entrega: evidencia y pendientes

21 noviembre 2026 · revisión directa de las guías E2 (65 páginas) y E3 (60 páginas); inferencia pública comprobada.

Auditoría documental contra las guías originales y evidencias recibidas. El avance de ablaciones sigue siendo el último comunicado, no monitoreo en vivo. No acredita cumplimiento experimental total ni envío académico.

[Auditoría detallada de las guías E2/E3](17_auditoria_cierre.md). La fecha prevista fue 21 noviembre, 10:00 Bogotá; esta revisión no acredita envío dentro de plazo.

## E1 · Integración de evidencia

**Estado:** Integrado.

**Evidencia:** Tres bases × 11 semillas; confusión, calibración, selección de clases y flujo de literatura.

**Falta:** Conservar las diferencias entre el corte E1 y el manifiesto V2; no modificar originales.

## E2 · Benchmark histórico y correcciones

**Estado:** Integrado con límites.

**Evidencia:** 13 arquitecturas × 5 en reserva; 22 semillas de las bases, 15 ablaciones de preprocesamiento y ensambles.

**Falta:** Cerrar la auditoría de las 66 corridas base y sus predicciones/curvas; no confundirlas con 65 evaluaciones de reserva.

## E2 · PCam

**Estado:** Detenido; recuperación preparada.

**Evidencia:** 8301 completa verificada por hash; 8302 historia hasta época 16; integridad interna de cuatro checkpoints verificada.

**Falta:** Comprobar entorno aislado en RunPod, cargar optimizador y reanudar; descargar datos oficiales; completar semillas y evaluación. Esperar GPU libre de E3.

## E2 · Histología y análisis de errores

**Estado:** Parcial.

**Evidencia:** 36 núcleos, 21 pacientes, 18 aciertos y 18 discrepancias de tres modelos; huellas cotejadas.

**Falta:** 100 errores por modelo principal con taxonomía/IC, errores compartidos y techo comparable (la guía admite acuerdo multi-rater u otra cota justificada); calcular distancia gamma.

## E2 · Explicabilidad y fidelidad

**Estado:** Parcial.

**Evidencia:** 48/48 mapas Inception constantes en evidencia anterior; no se presentan como explicaciones válidas.

**Falta:** Corregir capa o método y repetir fidelidad/estabilidad; completar incertidumbre y cobertura no acreditadas.

## E3 A · Correcciones, fuga y congelación

**Estado:** Parcial.

**Evidencia:** Historial de exposición de reserva declarado y fuentes preservadas.

**Falta:** Auditar archivos primarios completos, pacientes/duplicados/versiones y congelar paquete final con hashes.

## E3 B/D · Exportación e inferencia CPU

**Estado:** CICO publicado y probado en Render.

**Evidencia:** CICO 6101 exportado; 2.049/2.049 clases idénticas a RunPod usando las imágenes originales; hash ONNX y 7 pruebas de entradas/integridad. Prueba pública desde Safari: tumor 93,7%, linfocito 2,5%, estroma 3,8%; rechazo de dimensiones incorrectas y confirmación obligatoria verificados.

**Falta:** Exportar comparadores bajo política común, selector, probabilidades calibradas, incertidumbre con cobertura, explicación local, detección fuera de dominio y latencia/memoria del servidor.

## E3 C/E · Dashboard e integración visual

**Estado:** Publicado; verificación parcial.

**Evidencia:** Portal integrado, histología, filtros por página y libro; pruebas locales y escritorio.

**Falta:** Filtros globales para todos los gráficos de EDA, QA tablet/móvil, tabla completa con costos y diagnósticos del modelo elegido. La predicción CICO básica ya funciona.

## E3 F · Originalidad y revisión externa

**Estado:** Parcial.

**Evidencia:** Antecedentes cercanos y alcance de lectura declarados.

**Falta:** Completar evidencia de 3 bases/5 cadenas/snowballing, textos pendientes, fuente/adaptación y evaluación por tercero; no declarar novedad probada.

## E3 G · Mecanismo y ablaciones propias

**Estado:** En ejecución reportada; parcial.

**Evidencia:** Tres variantes × cinco semillas: cuatro completas reportadas, una reanudada con época 3 guardada, diez pendientes.

**Falta:** Recibir y verificar 15 corridas; completar base sin componentes y cada componente añadido solo (guía §7.4), control sin D4 y capacidad cuando corresponda; inferencia emparejada con Holm. No cambiar la cola en curso.

## E3 H · Tres conjuntos adicionales

**Estado:** Pendiente.

**Evidencia:** PanNuke, Lizard y MoNuSAC son candidatos, no datasets externos auditados.

**Falta:** Auditar solapamiento/etiquetas/licencia, diferencias en ≥2 ejes; evaluar toda la familia con presupuestos comparables, perturbaciones y escalabilidad.

## E3 I · Piloto de cinco semillas

**Estado:** Completo y verificado.

**Evidencia:** Cinco checkpoints y predicciones cotejados; 2.049 imágenes / 21 pacientes por semilla; macro-F1 recalculado.

**Falta:** No requiere repetir entrenamiento. Conservar archivos y separar piloto de evaluación final.

## E3 I · Benchmark final y potencia

**Estado:** Pendiente.

**Evidencia:** Cinco semillas piloto no cumplen la evaluación final.

**Falta:** Dimensionar por potencia al 90 % y mínimo ≥10; toda la familia, ≥3 pruebas por contraste, Holm, máximo p ajustado y potencia conjunta.

## E3 J · Libro y tabla maestra

**Estado:** Integrado; cierre pendiente.

**Evidencia:** Histología, tablas E1/E2 y cinco resultados CICO verificados integrados; misma fuente para libro/dashboard.

**Falta:** Benchmark final y tabla maestra completa; fichas MODEL_CARD/DATA_STATEMENT, CITATION/licencia, protocolo final con tag previo, DOI, autoría firmada y reproducción por tercero. Contenedor web existente no acredita reproducción independiente.

## E3 K · Sustentación

**Estado:** Guion disponible; no ensayada.

**Evidencia:** Problema/datos, antecedentes, mecanismo, resultados y demostración.

**Falta:** Preparar diapositivas definitivas, ensayar demostración y explicación/modificación del mecanismo; respaldo local comprobado.

## Entrega · Congelación y envío final

**Estado:** Pendiente.

**Evidencia:** Portal accesible; paquete previo no equivale al paquete final de esta revisión.

**Falta:** Congelar versión, descargar respaldo independiente, generar hashes, revisar enlaces y adjuntos y enviar por el canal oficial.

