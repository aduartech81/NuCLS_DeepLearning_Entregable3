# CICO frente a NuClass: diferencia metodológica y evidencia necesaria

**Revisión asistida del 25 de noviembre de 2026.** Se contrastaron las secciones 3.1–3.3 del artículo con `src/original_model.py`. Esta lectura amplía el análisis de antecedentes; no constituye una réplica de NuClass, una revisión independiente ni una demostración de novedad.

## Antecedente contrastado

Xu et al., *Adaptive Multi-Scale Integration Unlocks Robust Cell Annotation in Histopathology Images*, arXiv:2511.13586v1, 17 de noviembre de 2025. Se fija esta versión para hacer trazable la lectura. [Texto primario y ecuaciones](https://arxiv.org/html/2511.13586v1).

| Eje | NuClass, según el artículo | CICO, según la implementación |
|---|---|---|
| Entrada | Recorte local 224 × 224 y campo contextual 1024 × 1024 (§3). | Un recorte cuadrado; centro y entorno se separan con una máscara geométrica en el mapa de características. No hay segmentación nuclear. |
| Representación | UNI2-h y DINOv3, adaptación condicionada por tejido (§§3.1–3.2). | Encoder convolucional compartido para ocho transformaciones D4; promedio de descriptores centrales y periféricos. |
| Fusión | Mezcla convexa de probabilidades de dos ramas, ecuación 15. | Suma de una corrección acotada a los logits centrales; softmax posterior para obtener probabilidades. |
| Compuerta | Características y estadísticas de confianza, entropía y margen, ecuaciones 16–18. | Sigmoide de descriptores centro–entorno concatenados; amortiguación adicional por dispersión entre orientaciones. |
| Supervisión de la compuerta | Preferencia entre expertos y objetivos auxiliares, ecuaciones 19–23. | `components()` no define esa supervisión específica. La dispersión no equivale a incertidumbre calibrada. |

## Qué diferencia puede defenderse

En el código de CICO, con K clases, la corrección es `delta = B * tanh(context_head(r)) / sqrt(K)`, y `B = beta * gate / (1 + penalty * dispersion)`. Con parámetros no negativos, cada componente de `tanh` está acotado por uno y por ello la norma euclídea de la corrección es como máximo B, que a su vez no supera beta.

Esta es una propiedad de la intervención contextual sobre los logits. No garantiza acierto, calibración, resistencia a cambios de tinción ni superioridad. Tampoco convierte la dispersión de orientaciones en una probabilidad de error. El promedio D4 proporciona una invariancia a ese grupo finito bajo las hipótesis expuestas en el [capítulo de diseño](05_modelo_diseno.md); no implica invariancia a cualquier rotación.

La distinción concreta para estudiar es **corregir logits con presupuesto limitado frente a mezclar predicciones de expertos**. La existencia de esa distinción no demuestra prioridad científica. No deben presentarse contexto, compuertas o simetría como invenciones de NuCLEA.

## Comparación que aún debe ejecutarse

1. Mantener idénticos datos, particiones por paciente, selección de checkpoint y presupuesto de entrenamiento.
2. Contrastar CICO con una base central y controles de capacidad activa comparable; contabilizar los ocho pases del encoder además de los parámetros.
3. Incluir una fusión de probabilidades con capacidad comparable como control de mecanismo. Si no reproduce modelos, datos y entrenamiento del artículo, denominarla **control inspirado en fusión**, no réplica NuClass.
4. Estimar efectos e intervalos sobre semillas pareadas bajo un protocolo prospectivo y test independiente. No reutilizar la validación histórica como confirmación nueva.

Los resultados del piloto y las ablaciones ya disponibles no se modifican con esta lectura. No se añade ninguna comparación numérica contra NuClass: sus condiciones no son las de este experimento. El [resultado exploratorio y sus límites](24_nueva_revision.md) continúa vigente.

## Alcance del avance sin GPU

Queda realizada la comparación de mecanismos y localizados sus pasajes primarios. Continúan abiertos el cribado completo de literatura, el seguimiento sistemático de citas, la revisión por tercero y las comparaciones experimentales. PCam pertenece a la réplica E2 y su finalización no resuelve automáticamente estas exigencias de E3.
