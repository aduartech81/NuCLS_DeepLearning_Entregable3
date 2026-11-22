# Tabla maestra de resultados disponibles

La misma tabla alimenta NuCLEA. Media y desviación estándar entre semillas; no son intervalos por paciente. Las poblaciones de cada corte son diferentes: no se ordenan conjuntamente como prueba de superioridad. PCam y el benchmark confirmatorio no se incorporan sin artefactos verificados.

| Corte | Modelo | Semillas | Macro-F1 medio | DE entre semillas |
|---|---|---:|---:|---:|
| E1 validación histórica | softmaxcnn_bn | 11 | 0.756766 | 0.025475 |
| E1 validación histórica | densenet121 | 11 | 0.778256 | 0.025384 |
| E1 validación histórica | resnet50 | 11 | 0.793404 | 0.017341 |
| E2 desarrollo auditado | softmaxcnn_bn | 22 | 0.760030 | 0.021915 |
| E2 desarrollo auditado | densenet121 | 22 | 0.784588 | 0.021721 |
| E2 desarrollo auditado | resnet50 | 22 | 0.792242 | 0.022710 |
| E2 reserva expuesta | softmaxcnn_bn | 5 | 0.474160 | 0.061858 |
| E2 reserva expuesta | densenet121 | 5 | 0.637879 | 0.060033 |
| E2 reserva expuesta | resnet50 | 5 | 0.666943 | 0.034907 |
| E2 reserva expuesta | resnet18 | 5 | 0.525980 | 0.065373 |
| E2 reserva expuesta | mobilenetv3_small_100 | 5 | 0.650388 | 0.029760 |
| E2 reserva expuesta | efficientnet_b0 | 5 | 0.675828 | 0.031199 |
| E2 reserva expuesta | deit_tiny_patch16_224 | 5 | 0.611740 | 0.028208 |
| E2 reserva expuesta | swin_tiny_patch4_window7_224 | 5 | 0.494165 | 0.049901 |
| E2 reserva expuesta | mobilevit_xxs | 5 | 0.605316 | 0.072218 |
| E2 reserva expuesta | mixer_s16_224 | 5 | 0.600694 | 0.026864 |
| E2 reserva expuesta | convnext_tiny | 5 | 0.516177 | 0.026880 |
| E2 reserva expuesta | inception_v3 | 5 | 0.720419 | 0.033279 |
| E2 reserva expuesta | sequencer2d_s | 5 | 0.433229 | 0.049193 |
| E3 validación piloto | CICO | 5 | 0.668243 | 0.037204 |
| E3 ablaciones validación | sin_contraste | 5 | 0.679140 | 0.030867 |
| E3 ablaciones validación | sin_amortiguacion | 5 | 0.661048 | 0.028140 |
| E3 ablaciones validación | sin_contexto | 5 | 0.662546 | 0.020912 |
