# Control descriptivo de explicaciones CICO

Seis ejemplos públicos de validación, seleccionados para demostración. Diagnóstico descriptivo, no muestra independiente ni validación clínica. La referencia aleatoria es un control del orden; no prueba causalidad. La rotación prueba una simetría de diseño de CICO, no robustez general. No corrige Inception E2 ni cierra fidelidad/estabilidad de la familia.

## Método y procedencia

Oclusión 8×8, bloques 16px, relleno media RGB de la imagen, orden descendente de caída de probabilidad. Curvas acumuladas cada 8 bloques; diez órdenes aleatorios fijos. Rotación 90 grados y alineación inversa del mapa.

Modelo ONNX SHA-256: `da64160bc772eb3486107ff1f10ad97327ff0d61f7d8a642727003799ca6bcb5`. Se conserva sin cambios. Seis recortes públicos con hashes en el archivo de resultados. Código reproducible: `tools/evaluar_explicaciones_cpu.py`; salida `data/diagnosticos/explicaciones_cpu.json`. Solo CPU.

## Resultados por caso

AUC es el área trapezoidal bajo la puntuación de la clase originalmente elegida frente a la fracción de bloques modificados; no es ROC-AUC. En eliminación, menor AUC es favorable; en inserción, mayor AUC es favorable. El control es la media de diez órdenes aleatorios fijos.

| Caso | Δ AUC eliminación (mapa − azar) | Δ AUC inserción (mapa − azar) | Correlación del mapa tras rotación y alineación |
|---|---:|---:|---:|
| 01 | -0.114431 | 0.086678 | 1.00000000 |
| 07 | -0.242846 | 0.057976 | 1.00000000 |
| 13 | -0.141072 | 0.554294 | 1.00000000 |
| 19 | -0.337773 | 0.090153 | 1.00000000 |
| 25 | -0.191373 | 0.186794 | 0.99999982 |
| 31 | -0.186219 | 0.499415 | 1.00000000 |

## Interpretación y límite

En estos seis ejemplos, el orden del mapa reduce más rápidamente la puntuación al eliminar regiones y la recupera más rápidamente al insertarlas que el control aleatorio medio. La estabilidad ante una rotación de 90° es coherente con la simetría D4 del diseño. No se evaluó estabilidad frente a tinción, ruido o cambio de dominio.

Las imágenes se seleccionaron para demostración y pertenecen a validación. La intervención y el mapa utilizan el mismo relleno, por lo que existe afinidad metodológica entre explicación y evaluación. No hay intervalos poblacionales ni prueba confirmatoria. El análisis no valida explicaciones clínicas y no corrige los 48 mapas constantes de Inception en E2. Falta un conjunto independiente y representativo, otros rellenos/perturbaciones y evaluar cada modelo principal.

[Explorar las curvas en NuCLEA](https://nucls-entregable3.onrender.com/calidad-explicaciones).
