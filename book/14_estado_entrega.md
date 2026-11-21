# Estado de entrega: evidencia y pendientes

**Fecha límite: sábado 21 de noviembre de 2026, 10:00 a. m. Bogotá.** Corte del 21 de noviembre: cinco semillas piloto recibidas y verificadas. Este estado es el mismo que muestra el dashboard, generado desde `data/estado_entrega.json`.

## Diagnóstico

Libro y dashboard reúnen la evidencia disponible de E1, E2 y E3. **No está acreditado el cumplimiento experimental total.** Publicar y documentar no resuelve PCam, el benchmark final, las ablaciones propias ni los conjuntos externos. Tampoco puede garantizarse completar esas brechas antes de la fecha límite con el tiempo de ejecución disponible.

La revisión usa la matriz de requisitos E3 y la trazabilidad E2 conservadas en el proyecto. Distingue evidencia integrada, avance comunicado y verificación pendiente; no convierte archivos antiguos de auditoría en nuevos experimentos.

## Matriz única de cierre

### E1 · Integración de evidencia

**Estado:** Integrado. **Ubicación:** Libro y dashboard.

**Evidencia disponible:** Tres bases × 11 semillas; confusión, calibración, selección de clases y flujo de literatura.

**Falta exactamente:** Conservar las diferencias entre el corte E1 y el manifiesto V2; no modificar originales.

**Depende de:** Documentación.

### E2 · Benchmark histórico y correcciones

**Estado:** Integrado con límites. **Ubicación:** Libro y dashboard.

**Evidencia disponible:** 13 arquitecturas × 5 en reserva; 22 semillas de las bases, 15 ablaciones de preprocesamiento y ensambles.

**Falta exactamente:** Cerrar la auditoría de las 66 corridas base y sus predicciones/curvas; no confundirlas con 65 evaluaciones de reserva.

**Depende de:** Archivos E2.

### E2 · PCam

**Estado:** Detenido. **Ubicación:** Último inventario comunicado.

**Evidencia disponible:** 8301 completa, época 20; 8302 checkpoint época 16; 8303–8305 sin checkpoint.

**Falta exactamente:** Revisar checkpoint y optimizador, reanudar 8302 y ejecutar 8303–8305; consolidar métricas de réplica. No usar la GPU ocupada por E3.

**Depende de:** GPU y checkpoints E2.

### E2 · Histología y análisis de errores

**Estado:** Parcial. **Ubicación:** Libro y dashboard.

**Evidencia disponible:** 36 núcleos, 21 pacientes, 18 aciertos y 18 discrepancias de tres modelos; huellas cotejadas.

**Falta exactamente:** Revisión de 100 errores por modelo principal, taxonomía y acuerdo/techo multi-rater con anotaciones independientes.

**Depende de:** Revisión humana y anotaciones.

### E2 · Explicabilidad y fidelidad

**Estado:** Parcial. **Ubicación:** Correcciones E2.

**Evidencia disponible:** 48/48 mapas Inception constantes en evidencia anterior; no se presentan como explicaciones válidas.

**Falta exactamente:** Corregir capa o método y repetir fidelidad/estabilidad; completar incertidumbre y cobertura no acreditadas.

**Depende de:** Modelos entrenados y evaluación.

### E3 A · Correcciones, fuga y congelación

**Estado:** Parcial. **Ubicación:** Trazabilidad de correcciones.

**Evidencia disponible:** Historial de exposición de reserva declarado y fuentes preservadas.

**Falta exactamente:** Auditar archivos primarios completos, pacientes/duplicados/versiones y congelar paquete final con hashes.

**Depende de:** Archivos y auditoría.

### E3 B/D · Exportación e inferencia CPU

**Estado:** Pendiente. **Ubicación:** Código preparado; función web no habilitada.

**Evidencia disponible:** Cinco checkpoints CICO recibidos y verificados por hash; no ejecutados en esta auditoría.

**Falta exactamente:** Definir selección por validación, exportar pesos y metadata, verificar ida/vuelta numérica, latencia/memoria CPU, entradas inválidas/fuera de dominio e incertidumbre. Verificar comparadores exigidos (Top10, bases y original).

**Depende de:** Artefactos entrenados.

### E3 C/E · Dashboard e integración visual

**Estado:** Publicado; verificación parcial. **Ubicación:** Render.

**Evidencia disponible:** Portal integrado, histología, filtros por página y libro; pruebas locales y escritorio.

**Falta exactamente:** Comprobar responsividad móvil, filtros globales exigidos y flujo de predicción cuando exista inferencia. No hay prueba móvil acreditada.

**Depende de:** QA web y modelo.

### E3 F · Originalidad y revisión externa

**Estado:** Parcial. **Ubicación:** Capítulo de literatura y matriz de novedad.

**Evidencia disponible:** Antecedentes cercanos y alcance de lectura declarados.

**Falta exactamente:** Completar evidencia de 3 bases/5 cadenas/snowballing, textos pendientes, fuente/adaptación y evaluación por tercero; no declarar novedad probada.

**Depende de:** Búsqueda y revisión humana.

### E3 G · Mecanismo y ablaciones propias

**Estado:** Parcial. **Ubicación:** Implementación y propiedades sintéticas.

**Evidencia disponible:** CICO formulado; pruebas previas de D4, cota y gradientes.

**Falta exactamente:** Entrenar y analizar ≥3 componentes aislados del mecanismo, más control D4 definido; las ablaciones de preprocesamiento E2 no sustituyen estas.

**Depende de:** Entrenamiento adicional.

### E3 H · Tres conjuntos adicionales

**Estado:** Pendiente. **Ubicación:** Candidatos documentados.

**Evidencia disponible:** PanNuke, Lizard y MoNuSAC son candidatos, no datasets externos auditados.

**Falta exactamente:** Auditar solapamiento/etiquetas/licencia, diferencias en ≥2 ejes; evaluar toda la familia con presupuestos comparables, perturbaciones y escalabilidad.

**Depende de:** Datos y GPU.

### E3 I · Piloto de cinco semillas

**Estado:** Completo y verificado. **Ubicación:** Libro y dashboard; ZIP respaldado.

**Evidencia disponible:** Cinco checkpoints y predicciones cotejados; 2.049 imágenes / 21 pacientes por semilla; macro-F1 recalculado.

**Falta exactamente:** No requiere repetir entrenamiento. Conservar archivos y separar piloto de evaluación final.

**Depende de:** Ninguna para cerrar recepción del piloto.

### E3 I · Benchmark final y potencia

**Estado:** Pendiente. **Ubicación:** No acreditado.

**Evidencia disponible:** Cinco semillas piloto no cumplen la evaluación final.

**Falta exactamente:** Dimensionar por potencia al 90 % y mínimo ≥10; toda la familia, ≥3 pruebas por contraste, Holm, máximo p ajustado y potencia conjunta.

**Depende de:** Diseño, entrenamiento y estadística.

### E3 J · Libro y tabla maestra

**Estado:** Integrado; cierre pendiente. **Ubicación:** Libro publicado.

**Evidencia disponible:** Histología, tablas E1/E2 y cinco resultados CICO verificados integrados; misma fuente para libro/dashboard.

**Falta exactamente:** Completar evidencia del benchmark final, fichas de exportación, entorno/contenedor de inferencia, DOI y reproducción independiente.

**Depende de:** Resultados finales y tercero.

### E3 K · Sustentación

**Estado:** Guion disponible; no ensayada. **Ubicación:** 20 minutos propuestos.

**Evidencia disponible:** Problema/datos, antecedentes, mecanismo, resultados y demostración.

**Falta exactamente:** Preparar diapositivas definitivas, ensayar demostración y explicación/modificación del mecanismo; respaldo local comprobado.

**Depende de:** Autor.

### Entrega · Congelación y envío final

**Estado:** Pendiente. **Ubicación:** 21 noviembre, 10:00 Bogotá.

**Evidencia disponible:** Portal accesible; paquete previo no equivale al paquete final de esta revisión.

**Falta exactamente:** Congelar versión, descargar respaldo independiente, generar hashes, revisar enlaces y adjuntos y enviar por el canal oficial.

**Depende de:** Autor y paquete final.

## Orden operativo hasta las 10:00

1. Piloto recibido y respaldado: no relanzarlo.
2. Priorizar exportación y comprobación CPU; mantener publicada solo la funcionalidad verificada.
3. Consolidar resultados y limitaciones; el benchmark final, las ablaciones propias, los conjuntos externos y PCam siguen siendo brechas separadas.
4. Antes de las 09:00, congelar evidencia verificable; 09:00–09:30, prueba de enlaces, libro, descargas y respaldo; 09:30–10:00, envío académico y comprobante. Es una planificación propuesta, no garantía de completar experimentos.

[Resultados piloto verificados](14_resultados_piloto.md).
