# Dashboard integrado del proyecto final

La publicación reúne E1, E2 y E3 en [el portal del proyecto](https://nucls-entregable3.onrender.com/). Los originales y el ZIP entregado se preservan.

## Recorrido de lectura

- **Proyecto:** mapa conceptual y estado experimental.
- **Datos y EDA:** clases, pacientes, dominio e histogramas de calidad agregados.
- **Resultados E1–E2:** selector de etapa y arquitecturas; baselines E1 con 11 semillas; ampliación E2 de 22 semillas; reserva histórica E2 con 13 modelos y cinco semillas.
- **CICO y literatura:** formulación, mecanismos, antecedentes y diagramas de arquitectura.
- **Piloto:** curvas parciales reportadas, con procedencia y corte.
- **Evidencia:** requisitos, límites y reproducción.

## Comparabilidad y privacidad

No se mezclan las corridas de distintas etapas. Las barras de error de la reserva representan desviación entre semillas; los intervalos por paciente se muestran por separado. Las tablas permiten ordenar, filtrar y exportar CSV. Los histogramas de calidad se publican agregados, sin identificadores de pacientes. El ancho del diagrama de flujo conceptual no cuantifica datos.

La inferencia CPU de CICO requiere recibir y validar pesos, preprocesamiento y exportación. La web no presenta predicciones aleatorias ni convierte el piloto en un benchmark final. PCam E2 continúa detenido según el último inventario recibido.


## Histología integrada

La [galería histológica](/histologia) reúne 36 núcleos diferentes de 21 pacientes de validación: 18 aciertos y 18 discrepancias seleccionados de tres modelos históricos, semilla 6113. Permite filtrar por clase, modelo y resultado; comparar el campo limpio con la anotación original, ampliar las imágenes y consultar probabilidades registradas.

El campo de contexto no se presenta como la entrada exacta de 128 × 128. El contorno amarillo proviene de las coordenadas originales y no representa Grad-CAM. La selección ilustrativa no estima tasas. Las predicciones de CICO todavía no se han incorporado.
