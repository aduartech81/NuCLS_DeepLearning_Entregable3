# Síntesis de entrega y sustentación

**Autor: Andrés Duarte Chaves. Edición de entrega: 22 de noviembre de 2026.**

Esta edición incorpora las correcciones posteriores a la revisión. El paquete es una copia fija; el sitio público puede mostrar una versión anterior o una actualización posterior. La versión pública verificada al preparar este paquete corresponde al commit `441ad5f95d3b6b7356b378c45aff659e4604e123`. Las nuevas correcciones de esta edición se incluyen en el ZIP; su presencia aquí no acredita despliegue en Render.

## Resultado principal

CICO obtuvo Macro-F1 0,6682. En la comparación emparejada sobre la misma validación fue inferior a las tres bases en las cinco semillas. La hipótesis de mejora no recibe apoyo en este corte. Sin contraste alcanzó 0,6791; sin amortiguación, 0,6610; sin contexto, 0,6625. No hay beneficio consistente de los componentes en estos resultados.

## Tres análisis sobre las diferencias disponibles

Las pruebas se agregaron después del piloto: no son preregistro ni nuevos experimentos. Diferencia: CICO menos base. Holm se aplica a tres comparadores dentro de cada método. El criterio conjunto usa el máximo de las tres p antes de Holm; no se selecciona el método favorable.

| Base | Diferencia | d_z | t: p Holm | Wilcoxon: p Holm | Permutación: p Holm | Conjunta: p Holm |
|---|---:|---:|---:|---:|---:|---:|
| softmaxcnn_bn | -0.08269 | -1.875 | 0.02740 | 0.18750 | 0.18750 | 0.18750 |
| densenet121 | -0.10097 | -1.878 | 0.02740 | 0.18750 | 0.18750 | 0.18750 |
| resnet50 | -0.11602 | -2.984 | 0.00787 | 0.18750 | 0.18750 | 0.18750 |

t pareada: diferencias independientes entre entrenamientos y aproximadamente normales. Wilcoxon: diferencias simétricas. Permutación de signos: intercambiabilidad de signos bajo H0. Shapiro con n=5 tiene poca potencia y no demuestra normalidad; independencia entre pacientes no se obtiene repitiendo semillas. Ninguna prueba convierte validación usada para seleccionar modelos en test final.

Con cinco diferencias no nulas, el mínimo p bilateral exacto de Wilcoxon es 0,0625. Agregar la t pareada no corrige la falta de repeticiones del diseño. Los efectos observados son negativos; la inferencia conjunta sigue limitada.

## Checkpoints de la primera época

| Semilla | Épocas ejecutadas | Mejor época | Pérdida inicial | Pérdida final | F1 final |
|---|---:|---:|---:|---:|---:|
| 6101 | 25 | 22 | 0.7672 | 0.5175 | 0.7050 |
| 6102 | 23 | 18 | 0.7698 | 0.5312 | 0.6926 |
| 6103 | 6 | 1 | 0.7524 | 0.6511 | 0.6402 |
| 6104 | 6 | 1 | 0.7618 | 0.6516 | 0.6286 |
| 6105 | 6 | 1 | 0.7601 | 0.6533 | 0.6148 |

6103, 6104 y 6105 acumularon cinco épocas sin superar el resultado inicial y terminaron en la época 6. La pérdida de entrenamiento descendió. Esto explica la parada, pero no identifica causalmente capacidad, sobreajuste o insuficiente entrenamiento. No se cambian retrospectivamente checkpoints ni se descartan semillas.

## Hallazgos concretos del EDA

La proporción tumoral cambia de 47,99 % en train a 54,08 % en validación; estroma baja de 21,34 % a 16,79 %. El canal rojo medio aproximado de linfocitos baja de 159,99 a 135,25 sobre 255. Las medias provienen de centros de 16 intervalos, no del promedio exacto de píxeles. Describen diferencias de composición y apariencia; no identifican por sí solas la causa. Los gráficos del dashboard recalculan estas cifras con los filtros.

## Control de apariencia

Filtro experimental nuevo, ajustado con 14.539 imágenes train. Combina histogramas RGB, medias, desviaciones y diferencias locales; usa una distancia con covarianza regularizada. El umbral se fijó en el percentil 95 de 952 recortes de los primeros diez pacientes de validación ordenados por identificador, antes de comprobar los once restantes y cinco patrones sintéticos. No modifica los pesos ni las predicciones históricas.

En los 1.097 recortes restantes aceptó 877 (79,95 %). Rechazó tejido válido: 44,48 % de linfocitos, 19,66 % de estroma y 5,57 % de tumor. Rechazó los cinco patrones sintéticos (ruido RGB, degradado con ruido, tablero gris, degradado de colores y ruido rosado). Los seis ejemplos públicos superan el filtro.

**Limitación material:** el rechazo es desigual por clase. No hay prueba externa representativa de imágenes no histológicas; superar el filtro no certifica tejido ni diagnóstico. Las entradas rechazadas no reciben clase en la nueva interfaz. Es una protección experimental conservadora, no un detector OOD validado ni cobertura garantizada.

## Respuestas para la sustentación

1. **¿Cómo separar capacidad y mecanismo?** Hoy no podemos atribuir la diferencia exclusivamente al mecanismo: CICO tiene 7.671 parámetros y las bases son mayores. El control de CNN de capacidad comparable está implementado, pero aún requiere entrenamiento. No afirmar que ya resolvió la confusión.
2. **¿Qué queda de la hipótesis si quitar contraste mejora?** La hipótesis no recibe apoyo en este corte. Se conserva la propiedad matemática de acotación, pero esta no implica mejor clasificación.
3. **¿Qué diferencia hay con Veeling y NuClass?** D4 y fusión contextual tienen antecedentes. La diferencia candidata es una corrección de logits limitada por un presupuesto dependiente de dispersión. Su novedad requiere comparación metodológica completa, no solo una fórmula distinta.
4. **¿Por qué cinco semillas?** Fue un piloto exploratorio insuficiente para el contraste exacto exigido. No podía producir p bilateral menor que 0,05. Se reconoce el error de adecuación entre diseño y objetivo; la ampliación debe fijar potencia y presupuesto antes de ejecutar.
5. **¿Por qué tres mejores épocas son la primera?** Por cinco validaciones consecutivas sin mejora antes de parar. La disminución de pérdida no asegura mejor Macro-F1; las curvas muestran ambas cosas. No se ha aislado la causa.

## Ruta de demostración de 20 minutos

- 0–3: pregunta, clases y pacientes; separar recorte de paciente independiente.
- 3–6: EDA con cifras y comparadores.
- 6–10: CICO, acotación y antecedentes.
- 10–14: diferencias negativas, ablaciones y parada temprana.
- 14–17: un ejemplo histológico, puntuaciones y límites del filtro.
- 17–20: conclusión, controles necesarios y preguntas.

## Estado de cierre

Completos y disponibles: cinco semillas piloto, quince ablaciones, exportación ONNX verificada, auditoría de datos, análisis descriptivos y libro integrado. PCam continúa según el último reporte del autor; no hay en este paquete un test final nuevo verificado. Faltan controles entrenados de capacidad y sin D4, ampliación de repeticiones justificada, benchmark confirmatorio y conjuntos externos. La novedad, calibración, cobertura y reproducción por tercero no se acreditan mediante esta edición.

El cuaderno anterior de cinco semillas sigue siendo exploratorio: no debe interpretarse como cumplimiento del mínimo confirmatorio ni ejecutarse mientras PCam trabaja. Esta entrega no inicia entrenamientos.

## Enlaces

- [NuCLEA en Render](https://nucls-entregable3.onrender.com/).
- [Libro público](https://nucls-entregable3.onrender.com/libro/).
- [Repositorio](https://github.com/aduartech81/NuCLS_DeepLearning_Entregable3).
