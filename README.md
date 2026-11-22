# NuCLEA · Proyecto NuCLS: E1, E2 y E3 integrados

Dashboard y libro: https://nucls-entregable3.onrender.com/

Versión para nueva revisión del 22 de noviembre de 2026. Integra evidencia histórica, histología real, cinco semillas piloto CICO verificadas, predicción ONNX CPU, sensibilidad por oclusión y auditoría de 66 corridas de desarrollo / 65 evaluaciones de reserva. No acredita cierre científico completo.

## Ejecución web
Instalar requirements.txt y ejecutar `python app.py`. El modelo y sus metadatos deben estar en models; se comprueba su huella al cargar. No se requiere GPU para la web. Construir libro con requirements-book.txt y `jupyter-book build book --warningiserror --keep-going`.

## Evidencia
Consultar libro capítulos 17 y 18, MODEL_CARD.md, DATA_STATEMENT.md, LICENSE_STATUS.md y CIERRE_Y_DEFENSA.md. Ejecutar `python -m pytest tests/test_dashboard.py tests/test_inference.py tests/test_cierre_cpu.py` para verificar la aplicación y los nuevos cálculos/controles. tools/cierre_cpu.py audita las fuentes recibidas y exige un directorio de salida nuevo; no modifica fuentes.

## Pendiente
Quince ablaciones ya verificadas. Finalizar PCam y evaluación final E3, controles/datasets externos, calibración/cobertura, fidelidad/estabilidad, adjudicación humana, literatura y reproducción independiente. Mantener E1 y el ZIP entregado intactos. No lanzar entrenamiento desde el dashboard.

## Revisión y comprobación
Leer el capítulo 24 del libro. Ejecutar las pruebas del workflow `.github/workflows/web.yml`; sus verificaciones locales no sustituyen la reproducción por un tercero. Los capítulos 14, 17 y 21 se generan con `tools/sincronizar_auditoria.py`; los capítulos 22 y 23, con `tools/documentar_analisis_cpu.py`. No editar tablas generadas sin actualizar su fuente compartida.
