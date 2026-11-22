# CICO: formulación, propiedad y límites

CICO combina una cabeza central con una corrección contextual acotada y amortiguada por dispersión de orientaciones. Existen cinco semillas piloto y quince ablaciones verificadas. La novedad y la superioridad predictiva **no están acreditadas**. La formulación siguiente documenta la implementación existente; no cambia los pesos ni constituye un preregistro retrospectivo.

## Descriptores y contraste

Sea $G=D_4$ el conjunto de ocho rotaciones/reflexiones exactas de una cuadrícula cuadrada. El mismo encoder $E_\theta$ procesa cada vista $gx$. Sobre su mapa de características se promedian una ventana central cuadrada y su complemento disjunto, produciendo $c_g,s_g\in\mathbb{R}^d$. La máscara central es geométrica; no es una segmentación nuclear. La implementación usa convoluciones y SiLU, sin dropout ni estadísticas de batch.

```{math}
:label: cico-descriptores
\bar c=\frac1{|G|}\sum_{g\in G}c_g,\qquad
\bar s=\frac1{|G|}\sum_{g\in G}s_g,\qquad
r_g=s_g-c_g,\qquad \bar r=\frac1{|G|}\sum_{g\in G}r_g.
```

La dispersión se calcula sobre orientaciones y dimensiones del descriptor:

```{math}
:label: cico-dispersion
V=\frac1{|G|d}\sum_{g\in G}\|r_g-\bar r\|_2^2\geq0.
```

## Compuerta, presupuesto y salida

Para $K=3$ clases, las cabezas $W_c,W_r$ son aplicaciones afines. La compuerta usa la concatenación de los descriptores promediados. En el piloto, $\beta=0.5$ y $\lambda=1$ son constantes del protocolo.

```{math}
:label: cico-presupuesto
q=\sigma(w_q^\top[\bar c;\bar s]+b_q),\qquad
B=\frac{\beta q}{1+\lambda V},\qquad
\delta=B\frac{\tanh(W_r\bar r+b_r)}{\sqrt K}.
```

```{math}
:label: cico-logits
z(x)=W_c\bar c+b_c+\delta,\qquad p(y\mid x)=\operatorname{softmax}(z(x)).
```

Las salidas softmax son puntuaciones no calibradas. $V$ mide dispersión entre vistas del encoder, no incertidumbre clínica ni variabilidad entre pacientes. La descripción corresponde a `src/original_model.py`, clase `ContextoAcotado`.

## Propiedad 1: invariancia D4

Para cualquier $h\in G$, la aplicación $g\mapsto gh$ permuta $G$. Por tanto, las vistas de $hx$ recorren exactamente las vistas de $x$, posiblemente en otro orden. El encoder compartido y la extracción determinista producen el mismo multiconjunto de pares $(c_g,s_g)$. Los promedios y la dispersión de las ecuaciones {eq}`cico-descriptores` y {eq}`cico-dispersion` no dependen del orden. La compuerta, el presupuesto y la cabeza final también coinciden: $z(hx)=z(x)$ en aritmética exacta.

La comparación computacional admite error de redondeo. La propiedad no cubre rotaciones arbitrarias con interpolación, deformaciones, ruido o cambios de tinción. No exige que el encoder sea equivariante: la invariancia proviene de agregar toda la órbita.

## Propiedad 2: corrección contextual acotada

Como cada coordenada de $\tanh(u)$ tiene valor absoluto menor o igual a uno, $\|\tanh(u)/\sqrt K\|_2\leq1$. Además $0\leq q\leq1$, $V\geq0$ y $\lambda\geq0$. De {eq}`cico-presupuesto`:

```{math}
:label: cico-cota
\|\delta\|_2\leq B=\frac{\beta q}{1+\lambda V}\leq\beta.
```

Para una cabeza central fija, dos correcciones válidas difieren a lo sumo $2\beta$ por desigualdad triangular. Esto **no acota el cambio total de logits ante cualquier cambio de imagen**: la cabeza central también puede cambiar y su campo receptivo incluye entorno. La propiedad no garantiza exactitud, calibración, robustez global ni superioridad.

## Intervenciones y pruebas

| Intervención | Modificación exacta | Evidencia |
|---|---|---|
| Sin contraste | $r_g=s_g$ | Cinco semillas verificadas |
| Sin amortiguación | Factor $1/(1+\lambda V)$ sustituido por uno | Cinco semillas verificadas |
| Sin contexto | $\delta=0$ | Cinco semillas verificadas |
| Sin órbita D4 | Una sola vista | Implementable; evaluación entrenada pendiente |
| Base sin componentes / cada componente solo | Requiere definir la familia y controlar capacidad | Evaluación confirmatoria pendiente |

`tests/test_original_model.py` comprueba las ocho isometrías, la cota, gradientes, entradas inválidas, serialización y aprendizaje sintético. Son pruebas de implementación; el aprendizaje sintético no mide utilidad histológica. La prueba de exportación usa una fixture sintética que no se publica como modelo entrenado. La equivalencia del modelo entrenado se documenta por separado en el capítulo 16.

## Costos, precedentes y pregunta abierta

La órbita requiere ocho evaluaciones del encoder por imagen; no son ocho pacientes ni ocho observaciones independientes. El presupuesto limita la corrección y puede impedir aprovechar contexto útil. El backbone pequeño y la máscara geométrica pueden limitar el desempeño. Las ablaciones no muestran superioridad consistente del modelo completo; se mantienen sus resultados sin cambiar retrospectivamente la selección del modelo desplegado.

La invariancia de grupo y las compuertas tienen precedentes explícitos en `experiments/procedencia.md`. La combinación se propone como candidato de ingeniería, no como prioridad científica demostrada. Véanse [literatura](04_literatura.md), [ablaciones](15_ablaciones_y_transicion.md), [diagnósticos](19_contexto_y_diagnosticos.md) y [planificación](23_planificacion_potencia.md).
