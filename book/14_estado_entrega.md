# Estado de entrega: evidencia y pendientes

**Fecha límite: sábado 21 de noviembre de 2026, 10:00 a. m. Bogotá.** Corte del 21 de noviembre: cinco semillas piloto recibidas y verificadas. Este estado es el mismo que muestra el dashboard, generado desde `data/estado_entrega.json`.

## Diagnóstico

Libro y dashboard reúnen la evidencia disponible de E1, E2 y E3. **No está acreditado el cumplimiento experimental total.** Publicar y documentar no resuelve PCam, el benchmark final, las ablaciones propias ni los conjuntos externos. Tampoco puede garantizarse completar esas brechas antes de la fecha límite con el tiempo de ejecución disponible.

La revisión usa la matriz de requisitos E3 y la trazabilidad E2 conservadas en el proyecto. Distingue evidencia integrada, avance comunicado y verificación pendiente; no convierte archivos antiguos de auditoría en nuevos experimentos.

## Matriz única de cierre

### E1 · Integración de evidencia

**Estado:** Integrado.

**Evidencia:** Tres bases × 11 semillas; confusión, calibración, selección de clases y flujo de literatura.

**Falta:** Conservar las diferencias entre el corte E1 y el manifiesto V2; no modificar originales.

### E2 · Benchmark histórico y correcciones

**Estado:** Integrado con límites.

**Evidencia:** 13 arquitecturas × 5 en reserva; 22 semillas de las bases, 15 ablaciones de preprocesamiento y ensambles.

**Falta:** Cerrar la auditoría de las 66 corridas base y sus predicciones/curvas; no confundirlas con 65 evaluaciones de reserva.

### E2 · PCam

**Estado:** Detenido; recuperación preparada.

**Evidencia:** 8301 completa verificada por hash; 8302 historia hasta época 16; integridad interna de cuatro checkpoints verificada.

**Falta:** Comprobar entorno aislado en RunPod, cargar optimizador y reanudar; descargar datos oficiales; completar semillas y evaluación. Esperar GPU libre de E3.

### E2 · Histología y análisis de errores

**Estado:** Parcial.

**Evidencia:** 36 núcleos, 21 pacientes, 18 aciertos y 18 discrepancias de tres modelos; huellas cotejadas.

**Falta:** Revisión de 100 errores por modelo principal, taxonomía y acuerdo/techo multi-rater con anotaciones independientes.

### E2 · Explicabilidad y fidelidad

**Estado:** Parcial.

**Evidencia:** 48/48 mapas Inception constantes en evidencia anterior; no se presentan como explicaciones válidas.

**Falta:** Corregir capa o método y repetir fidelidad/estabilidad; completar incertidumbre y cobertura no acreditadas.

### E3 A · Correcciones, fuga y congelación

**Estado:** Parcial.

**Evidencia:** Historial de exposición de reserva declarado y fuentes preservadas.

**Falta:** Auditar archivos primarios completos, pacientes/duplicados/versiones y congelar paquete final con hashes.

### E3 B/D · Exportación e inferencia CPU

**Estado:** CICO exportado; verificación local completada.

**Evidencia:** CICO 6101 exportado; 2.049/2.049 clases idénticas a RunPod usando las imágenes originales; hash ONNX y 7 pruebas de entradas/integridad.

**Falta:** Verificar inferencia en Render y medir memoria/latencia del servidor; calibración, fuera de dominio y exportación de comparadores pendientes.

### E3 C/E · Dashboard e integración visual

**Estado:** Publicado; verificación parcial.

**Evidencia:** Portal integrado, histología, filtros por página y libro; pruebas locales y escritorio.

**Falta:** Comprobar responsividad móvil, filtros globales exigidos y flujo de predicción cuando exista inferencia. No hay prueba móvil acreditada.

### E3 F · Originalidad y revisión externa

**Estado:** Parcial.

**Evidencia:** Antecedentes cercanos y alcance de lectura declarados.

**Falta:** Completar evidencia de 3 bases/5 cadenas/snowballing, textos pendientes, fuente/adaptación y evaluación por tercero; no declarar novedad probada.

### E3 G · Mecanismo y ablaciones propias

**Estado:** En ejecución reportada; parcial.

**Evidencia:** Tres variantes × cinco semillas: cuatro completas reportadas, una reanudada con época 3 guardada, diez pendientes.

**Falta:** Recibir y verificar las quince corridas; análisis emparejado y control sin D4 aún pendiente.

### E3 H · Tres conjuntos adicionales

**Estado:** Pendiente.

**Evidencia:** PanNuke, Lizard y MoNuSAC son candidatos, no datasets externos auditados.

**Falta:** Auditar solapamiento/etiquetas/licencia, diferencias en ≥2 ejes; evaluar toda la familia con presupuestos comparables, perturbaciones y escalabilidad.

### E3 I · Piloto de cinco semillas

**Estado:** Completo y verificado.

**Evidencia:** Cinco checkpoints y predicciones cotejados; 2.049 imágenes / 21 pacientes por semilla; macro-F1 recalculado.

**Falta:** No requiere repetir entrenamiento. Conservar archivos y separar piloto de evaluación final.

### E3 I · Benchmark final y potencia

**Estado:** Pendiente.

**Evidencia:** Cinco semillas piloto no cumplen la evaluación final.

**Falta:** Dimensionar por potencia al 90 % y mínimo ≥10; toda la familia, ≥3 pruebas por contraste, Holm, máximo p ajustado y potencia conjunta.

### E3 J · Libro y tabla maestra

**Estado:** Integrado; cierre pendiente.

**Evidencia:** Histología, tablas E1/E2 y cinco resultados CICO verificados integrados; misma fuente para libro/dashboard.

**Falta:** Completar evidencia del benchmark final, fichas de exportación, entorno/contenedor de inferencia, DOI y reproducción independiente.

### E3 K · Sustentación

**Estado:** Guion disponible; no ensayada.

**Evidencia:** Problema/datos, antecedentes, mecanismo, resultados y demostración.

**Falta:** Preparar diapositivas definitivas, ensayar demostración y explicación/modificación del mecanismo; respaldo local comprobado.

### Entrega · Congelación y envío final

**Estado:** Pendiente.

**Evidencia:** Portal accesible; paquete previo no equivale al paquete final de esta revisión.

**Falta:** Congelar versión, descargar respaldo independiente, generar hashes, revisar enlaces y adjuntos y enviar por el canal oficial.


## Orden operativo hasta las 10:00

1. Piloto recibido y respaldado: no relanzarlo.
2. Priorizar exportación y comprobación CPU; mantener publicada solo la funcionalidad verificada.
3. Consolidar resultados y limitaciones; el benchmark final, las ablaciones propias, los conjuntos externos y PCam siguen siendo brechas separadas.
4. Antes de las 09:00, congelar evidencia verificable; 09:00–09:30, prueba de enlaces, libro, descargas y respaldo; 09:30–10:00, envío académico y comprobante. Es una planificación propuesta, no garantía de completar experimentos.

[Resultados piloto verificados](14_resultados_piloto.md).

## Actualización de ablaciones y PCam

[Consultar el avance reportado, límites y transición preparada](15_ablaciones_y_transicion.md). PCam dispone ahora de respaldo local verificado y cuaderno de recuperación; todavía no se inició en RunPod. Las ablaciones registran cuatro corridas completas reportadas, no quince verificadas.
