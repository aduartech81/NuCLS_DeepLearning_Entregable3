# Comprobaciones ejecutadas sin GPU

Estas comprobaciones completan evidencias de ingeniería y de integridad que antes estaban pendientes. No son entrenamiento ni una validación confirmatoria del modelo.

## Integridad y separación de datos

Se leyeron **16.588 PNG** de entrenamiento y validación directamente del ZIP: hash de archivo, hash de píxeles RGB y tamaño 128 × 128 coinciden con el manifiesto en todos los casos. No se modificó ninguna partición.

| Partición | Recortes | Pacientes | Campos |
|---|---:|---:|---:|
| train | 14539 | 83 | 1192 |
| reserva_candidata | 969 | 6 | 24 |
| validation | 2049 | 21 | 229 |

Los tres cruces entre particiones tienen **cero coincidencias** de identificador de paciente, campo, hash de imagen fuente, píxeles y archivo. Tampoco se encontraron duplicados exactos internos según el manifiesto. De la reserva candidata solo se leyeron metadatos, no sus imágenes ni sus resultados.

Esto cierra la comprobación nominal y exacta sobre este paquete; no descarta duplicados aproximados, errores de identidad ni fuga por decisiones anteriores. La reserva histórica no se convierte por ello en test nuevo.

## Carga y memoria de la aplicación

Se ejecutó la aplicación real con Gunicorn, un worker y dos threads, ONNX en CPU y los seis ejemplos públicos. Las solicitudes recorren el callback de predicción y se comprueba que devuelvan una predicción válida. Son mediciones locales HTTP loopback, no de Render.

| Clientes simultáneos | Solicitudes | Errores | Mediana ms | p95 ms | Solicitudes/s |
|---:|---:|---:|---:|---:|---:|
| 1 | 60 | 0 | 17.54 | 21.67 | 55.13 |
| 2 | 60 | 0 | 30.36 | 38.09 | 63.52 |
| 4 | 60 | 0 | 62.77 | 84.18 | 60.33 |

Primera predicción: **203.81 ms**. Memoria RSS máxima del worker: **174.55 MiB**, obtenida mediante `getrusage` durante las respuestas HTTP. Incluye librerías y aplicación, no el proceso maestro. Plataforma: macOS-26.4-arm64-arm-64bit, Python 3.11.16. Estos valores no garantizan memoria ni latencia equivalentes en el plan de Render.

Se comprobaron las **72 rutas histológicas**, rechazo de caso inexistente (404), cuerpo HTTP mayor de 3 MiB (413) y base64 inválido con mensaje controlado. Una predicción posterior válida confirma recuperación sin detener el servicio. No se hizo una prueba de carga sobre el servicio público ni sobre PCam.

## Controles implementados y comprobados

Se añadieron constructores separados para base central, solo órbita, solo contexto, contexto con contraste, órbita con contexto, órbita con contexto y contraste, y CICO completo. Conservan el mismo conjunto de parámetros almacenados y admiten copiar la inicialización sin modificar la referencia. Igual número de parámetros almacenados **no implica igual cómputo ni parámetros activos**.

Ocho pruebas verifican eliminación exacta del contexto, identidad inicial de pesos, efecto y gradientes del contexto, invariancia de las variantes con órbita y dispersión nula con una sola vista. Esta última propiedad impide interpretar “amortiguación sola” sin órbita como un control informativo. Los controles están implementados; sus resultados predictivos requieren entrenarlos bajo un protocolo común.

## Integración continua verificada

El flujo remoto de GitHub Actions del commit `99db2bd9ebd2c477d6ad14cf824aebdc418c2b31` finalizó correctamente el 22/11/2026. Comprueba la versión anterior a estas nuevas adiciones; estas se validan en su propio commit. [Ejecución remota verificada](https://github.com/aduartech81/NuCLS_DeepLearning_Entregable3/actions/runs/45063575096).

## Reproducción

Desde una copia del repositorio, con las dependencias de la aplicación y `requests` instaladas:

```bash
python tools/benchmark_servicio_cpu.py
python tools/auditar_particiones.py /ruta/NuCLS_E3_DATOS_TRAIN_VALIDATION.zip
python -m pytest tests/test_control_variants.py tests/test_auditoria_particiones.py -q
```

Los resultados se escriben en `data/diagnosticos/` de esa copia. El benchmark inicia y termina únicamente su propio proceso local. La auditoría lee el ZIP sin extraer ni sobrescribir sus contenidos. Los hashes de entrada permiten comprobar que se usó la misma evidencia.
