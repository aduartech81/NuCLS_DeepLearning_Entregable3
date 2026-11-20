# Selección provisional — 17 noviembre 2026

Candidato de ingeniería: **CICO**, corrección contextual acotada por dispersión de orientaciones. No se acredita novedad científica ni ventaja predictiva.

Se descartó como propuesta suficiente la invariancia D4 aislada: Cohen y Welling (2016), https://proceedings.mlr.press/v48/cohenc16.html, y Veeling et al. (2018), https://arxiv.org/abs/1806.03962, documentan antecedentes directos. Las compuertas adaptativas también son conocidas (Selective Kernel Networks, https://openaccess.thecvf.com/content_CVPR_2019/papers/Li_Selective_Kernel_Networks_CVPR_2019_paper.pdf). La diferencia a investigar es el acoplamiento de contraste centro-entorno, dispersión de orientaciones y presupuesto explícito sobre logits. Una combinación no constituye por sí misma novedad.

Búsqueda preliminar web en inglés y español: “nuclei classification rotation invariant group pooling uncertainty context gating”, “histopathology dispersion gating context”, “clasificación nuclear invariancia contexto redes”. Esto NO reemplaza la revisión en tres bases, las cinco consultas reproducibles ni la comprobación independiente exigidas por la guía. No se registran estudios como incluidos sin cribado y lectura.

Alternativas: invariancia D4 simple (antecedente establecido); normalización/adversarial de tinción (antecedentes extensos y mayor complejidad); mecanismo contextual acotado (seleccionado para prototipo por verificabilidad algebraica, con novedad abierta).

## Propiedad y límites
Para cualquier h en D4, {gh:g∈D4}=D4. El promedio de descriptores y su dispersión son funciones simétricas del conjunto de vistas. Por tanto z(hx)=z(x) en aritmética exacta. La comparación numérica admite tolerancia de redondeo. No cubre rotaciones arbitrarias ni cambios de tinción.

Con K clases, |tanh(u_i)|≤1 implica ||tanh(u)/√K||₂≤1. Como 0≤σ(a)≤1 y V≥0, ||δ||₂≤β. Para un descriptor central fijo, dos correcciones difieren como máximo 2β. Esto NO es una cota sobre cambios arbitrarios de la imagen: el campo receptivo central ve entorno, y el término central también cambia.

La ventana central es geométrica, no una segmentación. Hay que comprobar el centrado nuclear. El promedio de ocho vistas aumenta el costo y puede diluir señales relevantes. El backbone pequeño puede limitar rendimiento.

Ablaciones previstas: sin contraste centro-entorno, sin amortiguación por dispersión, sin contribución contextual; además sin agregación D4. Presupuesto y protocolo aún no congelados. No ajustar usando reserva histórica.

Código desarrollado con asistencia de IA; el autor debe comprenderlo, verificar su procedencia y defender formalización y decisiones. Las pruebas sintéticas verifican implementación, no utilidad clínica.
