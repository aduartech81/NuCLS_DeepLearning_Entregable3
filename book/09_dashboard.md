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
