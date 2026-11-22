# Planificación: sensibilidad a efecto y variabilidad

Sensibilidad de planificación basada en cinco diferencias pareadas del piloto y aproximación normal bilateral con Bonferroni m=3. No es potencia conjunta, análisis de potencia del test exacto, preregistro ni garantía del tamaño final. La varianza es inestable con n=5. La familia final puede tener más contrastes: debe recalcularse antes de congelar el protocolo. Los deltas son escenarios, no márgenes elegidos tras ver resultados.

## Fórmula y supuestos

`n ≈ ((z(1−α/(2m)) + z(0,90)) × s_d / Δ)^2`. Se usa desviación de diferencias entre semillas, no dispersión de recortes como si fueran pacientes independientes. Alfa familiar 0,05; tres contrastes; objetivo individual 0,90. No demuestra potencia conjunta 0,90 ni satisface por sí solo la sección 8 de E3.

| Variante | DE de diferencias | MDE aproximado con n=10 | Δ=0,01: n | Δ=0,02: n | Δ=0,03: n | Δ=0,05: n |
|---|---:|---:|---:|---:|---:|---:|
| sin_contraste | 0.01193 | 0.01386 | 20 | 10 | 10 | 10 |
| sin_amortiguacion | 0.01794 | 0.02085 | 44 | 11 | 10 | 10 |
| sin_contexto | 0.02111 | 0.02454 | 61 | 16 | 10 | 10 |

El número mostrado incorpora el piso de diez semillas de la guía. No es una orden de ejecutar esas corridas: falta fijar el efecto mínimo relevante con justificación externa, la familia completa, la unidad independiente y simular las pruebas finales con corrección múltiple. El mínimo de diez semillas no asegura potencia suficiente.

## Condiciones antes de correr el benchmark final

1. Definir las preguntas, efectos mínimos relevantes, comparadores y controles sin elegirlos por el resultado favorable.
2. Auditar particiones y tres datasets externos; no reutilizar la reserva histórica como prueba nueva.
3. Justificar pruebas admisibles y su dependencia; no contar tres pruebas correlacionadas como tres replicaciones independientes.
4. Estimar potencia individual y conjunta con el diseño y corrección finales; congelar protocolo y hashes antes de nuevas corridas.
5. Conservar los análisis exploratorios actuales como tales, sin declararlos preregistrados retrospectivamente.

Código: `tools/planificar_potencia.py`. Datos compartidos con NuCLEA: `data/diagnosticos/planificacion_potencia.json`.

## E2: potencia y MDE históricos ya disponibles

El archivo histórico `data/proyecto/contrastes22.csv` contiene contrastes de las tres bases sobre 22 semillas. Se integra aquí sin recalcular ni modificar sus resultados. No corresponde a las 65 evaluaciones de reserva ni a PCam.

| Contraste histórico | n | Δ medio | MDE80 familia 3 | MDE80 familia 10 | Potencia histórica Δ=0,02 / familia 10 | R histórico propuesto |
|---|---:|---:|---:|---:|---:|---:|
| resnet50 - densenet121 | 22 | 0.00765 | 0.01893 | 0.02196 | 0.698 | 26 |
| resnet50 - softmaxcnn_bn | 22 | 0.03221 | 0.02521 | 0.02924 | 0.380 | 43 |
| densenet121 - softmaxcnn_bn | 22 | 0.02456 | 0.02087 | 0.02420 | 0.584 | 31 |

Estos valores son cálculos históricos bajo sus supuestos y no justifican automáticamente las cinco semillas del benchmark de reserva. Falta cotejar el método original y justificar la familia y el efecto mínimo relevante; no se ordena repetir ni ampliar experimentos por esta tabla.
