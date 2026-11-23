# Autoría, lectura metodológica y accesibilidad

**Autor del proyecto: Andrés Duarte Chaves.** Actualización para revisión docente: 22 de noviembre de 2026. La autoría se muestra en la portada de NuCLEA, en su pie común y en la apertura de este libro. Esta versión no modifica E1 ni el ZIP entregado.

## Lectura metodológica de tres antecedentes

Esta ampliación revisa secciones de método de tres fuentes primarias. Es una revisión asistida, no una segunda revisión independiente ni un cribado completo de los 148 registros recuperados. Se conserva el registro original de búsqueda.

| Fuente y pasaje consultado | Mecanismo y relación con CICO | Consecuencia para evaluar la propuesta |
|---|---|---|
| [Cohen y Welling, 2016](https://proceedings.mlr.press/v48/cohenc16.pdf), §§5–6, ecuaciones 10–12 | La convolución de grupo transforma filtros y representaciones con una regla de equivarianza. CICO enumera ocho vistas con un encoder compartido y agrega descriptores; no implementa esas capas de convolución de grupo. | La simetría no constituye novedad propia. Comparar parámetros y costo efectivo, sin equiparar ocho pases con una sola convolución. |
| [Veeling et al., 2018](https://arxiv.org/pdf/1806.03962), trabajo relacionado y §2, figura 1 | Aplica grupos de rotación/reflexión a patología y describe pooling sobre orientaciones. Distingue la arquitectura equivariante de promediar predicciones transformadas. CICO comparte la motivación de simetría, pero añade contexto y una corrección limitada de logits. | PCam y clasificación nuclear NuCLS son tareas distintas. La réplica PCam no demuestra por sí misma superioridad de CICO en NuCLS. |
| [Li et al., 2019](https://arxiv.org/pdf/1903.06586), §3.1, ecuaciones 2–6 | Selective Kernel combina ramas de diferentes escalas mediante atención softmax por canal. CICO usa contraste centro–entorno y limita una corrección de logits con dispersión entre vistas; no es esa mezcla de mapas por canal. | La selección adaptativa de contexto ya tiene antecedentes. El control de contexto sin amortiguación ayuda a separar aportes, pero estas diferencias no prueban originalidad. |

**Seguimiento de citas ejecutado:** el apartado de métodos de Veeling remite a G-CNN; se contrastaron las definiciones de Cohen y Welling. Esto es un enlace de seguimiento hacia atrás, no una búsqueda exhaustiva de citas. No se declara seguimiento hacia adelante completado ni auditoría de los repositorios de estos artículos.

**Conclusión crítica:** la hipótesis defendible es evaluar la combinación concreta de contraste contextual y corrección acotada. No corresponde presentar D4, contexto o atención como inventos de este proyecto. La evidencia disponible sigue siendo exploratoria y no acredita superioridad.

## Accesibilidad: comprobaciones de esta revisión

En la portada pública, a 768 × 1024, se comprobó que las siete imágenes visibles tienen texto alternativo y cargan. El enlace «Saltar al contenido» se activó con Enter y trasladó el foco al contenido principal. El ancho del documento no excedió el ancho de la ventana en esa comprobación. La portada conserva títulos, navegación principal y pies identificables en el árbol de accesibilidad.

Se amplió el estilo de foco visible a todos los controles y se añadió foco blanco sobre los paneles oscuros. La autoría tiene un estilo legible en la portada y el pie. Estas comprobaciones son parciales: no constituyen una certificación WCAG ni sustituyen pruebas con lectores de pantalla y usuarios.

## Para la revisión docente

- [Dashboard NuCLEA](https://nucls-entregable3.onrender.com/).
- [Resultados y pendientes verificables](24_nueva_revision.md).
- [Comprobaciones ejecutadas sin GPU](25_comprobaciones_sin_gpu.md).
- [Registro de búsqueda bibliográfica](26_busqueda_ejecutada.md).

PCam permanece fuera de esta actualización: no se inicia, detiene ni modifica su entrenamiento. Su finalización y los controles confirmatorios de E3 requieren evidencia experimental adicional; esta edición no los presenta como terminados.
