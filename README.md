# NuCLS: E1, E2 y E3 integrados

Dashboard y libro: https://nucls-entregable3.onrender.com/

Versión de cierre CPU del 21 de noviembre de 2026. Integra evidencia histórica, histología real, cinco semillas piloto CICO verificadas, predicción ONNX CPU, sensibilidad por oclusión y auditoría de 66 corridas de desarrollo / 65 evaluaciones de reserva. No acredita cierre científico completo.

## Ejecución web
Instalar requirements.txt y ejecutar `python app.py`. El modelo y sus metadatos deben estar en models; se comprueba su huella al cargar. No se requiere GPU para la web. Construir libro con requirements-book.txt y `jupyter-book build book --warningiserror --keep-going`.

## Evidencia
Consultar libro capítulos 17 y 18, MODEL_CARD.md, DATA_STATEMENT.md, LICENSE_STATUS.md y CIERRE_Y_DEFENSA.md. Ejecutar `python -m pytest tests/test_dashboard.py tests/test_inference.py tests/test_cierre_cpu.py` para verificar la aplicación y los nuevos cálculos/controles. tools/cierre_cpu.py audita las fuentes recibidas y exige un directorio de salida nuevo; no modifica fuentes.

## Pendiente
Recibir ablaciones, finalizar PCam y evaluación final E3, controles/datasets externos, calibración/cobertura, fidelidad/estabilidad, adjudicación humana, literatura y reproducción independiente. Mantener E1 y el ZIP entregado intactos. No lanzar entrenamiento desde el dashboard.
