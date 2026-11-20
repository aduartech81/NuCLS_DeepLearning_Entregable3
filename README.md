# NuCLS · Entregable 3

Actualización: 20 noviembre 2026. Entrega: sábado 21 noviembre, 10:00 Bogotá.

Aplicación Dash y Jupyter Book independientes para el candidato CICO. Incluye seis páginas interactivas, trece capítulos numerados y la introducción, referencias con nivel de lectura y tablas históricas E2 identificadas como tales. El piloto está en ejecución; se muestra una instantánea de sus primeras cuatro épocas, identificada como registro comunicado. No hay inferencia pública habilitada. Novedad y superioridad no acreditadas.

## Ejecución web

Instalar `requirements.txt` y `requirements-book.txt`; compilar con `jupyter-book build book --warningiserror --keep-going`; iniciar con `python app.py`. El libro se sirve bajo `/libro/` y la comprobación de salud en `/healthz`. El servicio web no importa Torch ni inicia experimentos.

## Piloto

La ejecución vigente en RunPod utiliza `../RUNPOD/NuCLS_E3_RunPod.ipynb`; el cuaderno Colab se conserva como antecedente y no debe lanzarse en paralelo. Protocolo y receta permanecen sin cambios. No ejecutar en paralelo con PCam en la misma GPU. Cinco semillas no equivalen al benchmark final requerido.

## Publicación

Crear un repositorio E3 y un servicio Render nuevos usando `render.yaml`. No vincular el servicio de E2. `Dockerfile` compila el libro en una etapa separada y arranca Gunicorn; el plan free se prepara para una vista previa; su capacidad y disponibilidad deben comprobarse al desplegar. Ninguna URL E3 se anuncia como publicada antes de verificar el despliegue.

## Evidencia y límites

`revision/` conserva las verificaciones, búsquedas y requisitos. `data/heredado_e2/procedencia.json` identifica tablas históricas. Las pruebas de modelo/exportación anteriores fueron sintéticas en CPU; no representan entrenamientos reales ni equivalencia entre entornos GPU. El paquete web no contiene imágenes de pacientes, checkpoints ni credenciales.

E1 y el ZIP E2 entregado no se modifican. El trabajo y publicación E3 tienen alcance separado. Se declara asistencia de IA y responsabilidad del autor en verificar y defender el contenido.
