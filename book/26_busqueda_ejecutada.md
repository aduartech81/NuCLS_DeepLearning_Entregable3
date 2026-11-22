# Búsqueda ejecutada en tres fuentes bibliográficas

Se ejecutaron cinco cadenas en Europe PMC, Crossref y OpenAlex: **15 consultas con respuesta HTTP 200**, el 22/11/2026. Se recuperaron **149 registros** y quedaron **148 registros únicos** según DOI normalizado o título. No son 148 artículos leídos ni incluidos.

## Protocolo de recuperación

Objetivo: localizar antecedentes del mecanismo CICO. Búsqueda exploratoria posterior al piloto, no preregistro. Se conserva fecha UTC, URL exacta, cadena, HTTP de intentos, total declarado, metadatos y hash de respuesta por consulta. Límite: diez primeros registros por consulta, orden predeterminado de relevancia. Los resultados no prueban exhaustividad ni ausencia de antecedentes.

| Cadena | Texto ejecutado |
|---|---|
| 1 | histopathology rotation invariant group equivariant convolution |
| 2 | histopathology nuclei center surround context classification |
| 3 | neural network bounded residual context gating |
| 4 | orientation disagreement uncertainty neural networks |
| 5 | selective kernel attention context histology |

## Registro de ejecución

| Fuente | Cadena | Total declarado | Recuperados | HTTP |
|---|---:|---:|---:|---:|
| Europe PMC | 1 | 9 | 9 | 200 |
| Europe PMC | 2 | 285 | 10 | 200 |
| Europe PMC | 3 | 444 | 10 | 200 |
| Europe PMC | 4 | 749 | 10 | 200 |
| Europe PMC | 5 | 600 | 10 | 200 |
| Crossref | 1 | 1220965 | 10 | 200 |
| Crossref | 2 | 1892148 | 10 | 200 |
| Crossref | 3 | 2607276 | 10 | 200 |
| Crossref | 4 | 2313349 | 10 | 200 |
| Crossref | 5 | 1264807 | 10 | 200 |
| OpenAlex | 1 | 190 | 10 | 200 |
| OpenAlex | 2 | 1818 | 10 | 200 |
| OpenAlex | 3 | 44721 | 10 | 200 |
| OpenAlex | 4 | 10598 | 10 | 200 |
| OpenAlex | 5 | 4100 | 10 | 200 |

Los totales declarados no se suman como publicaciones únicas. Crossref interpreta consultas bibliográficas de manera distinta a los otros servicios; los resultados no son intercambiables. Se respetaron respuestas de limitación de frecuencia y se conservaron los intentos.

## Qué se completó y qué falta

**Completado:** ejecución reproducible de cinco cadenas en tres fuentes, registro de resultados y deduplicación explícita. Se entrega `revision/busqueda_20261122/registros_para_cribado.csv` con DOI, enlace y fuentes de cada registro.

**Aún no completado:** cribado justificado, lectura de textos completos, búsqueda de citas hacia atrás y adelante, contraste detallado con CICO y revisión por un tercero. Todos los registros conservan el estado pendiente; no se inventaron decisiones de inclusión ni firmas de revisor. Un cribado limitado a títulos no acreditaría novedad.

## Reproducción y documentación de los servicios

```bash
python tools/busqueda_bibliografica.py
```

La reproducción genera una nueva fecha y puede recuperar resultados distintos. Se debe conservar la evidencia anterior si se compara la búsqueda.

- [Europe PMC: servicio de búsqueda](https://dev.europepmc.org/RestfulWebService).
- [Crossref: API de metadatos](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).
- [OpenAlex: búsqueda](https://help.openalex.org/api/searching/).

No se enviaron imágenes, checkpoints ni información personal a estos servicios; únicamente las cadenas bibliográficas mostradas.
