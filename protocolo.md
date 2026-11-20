# Protocolo E3 — piloto de desarrollo v1

Fecha: 18 noviembre 2026. Límite de entrega: sábado 21 noviembre, 10:00 America/Bogota. **Este documento define el piloto exploratorio; NO es el preregistro final congelado de E3.** No se ha lanzado entrenamiento ni intervenido Colab. El hash del protocolo piloto se guarda con cada corrida.

## Pregunta y mecanismo
¿La corrección contextual acotada por dispersión D4 aporta señal útil, sin degradar validación frente al clasificador central? CICO v1 conserva la formulación del 17 noviembre. La dispersión es un diagnóstico de representación, no incertidumbre calibrada ni prueba de desplazamiento. Registrar distribución de V, compuerta efectiva y norma de corrección. La demostración de invariancia/cota no implica mejor generalización. Novedad no acreditada; revisar matriz del 18 noviembre.

## Datos y particiones
Piloto exclusivamente sobre train/validation NuCLS heredados: 14.539/2.049 recortes, 83/21 pacientes según contrato previo. Clases tumor, linfocito, estroma; RGB128; medias/SD obtenidas de train, rotaciones90/reflexión horizontal solo train. Verificar manifiesto por SHA, disjunción de paciente/TSS/hash de píxeles, clases, formato e integridad de cada imagen. No leer imágenes de reserva. Esta sesión no dispone del manifiesto local: los conteos son contrato esperado, no auditoría real recién ejecutada.

No usar reserva E1/E2 para escoger beta, lambda, ancho, épocas, umbrales ni variantes. La confirmación nueva sigue sin resolver. La preselección externa PanNuke/Lizard/MoNuSAC conserva etiquetas nativas; no iguala epitelial a tumor ni inflamatorio a linfocito. Antes del congelamiento: licencia, versión, hashes, pacientes/fuentes y duplicados; Lizard debe excluir fuentes compartidas. Ver datos_candidatos.json. No se consideran tres datasets independientes ya disponibles.

## Piloto ejecutable y control de cómputo
Cinco semillas6101–6105, sin preentrenamiento, AdamW lr0.001 wd0, batch32, máximo25épocas, mínimo5, paciencia5. Una receta fija de factibilidad; NO búsqueda HPO equiparable al benchmark. Un modelo/semilla a la vez; cero workers y carga por imagen para limitar RAM. Mejor checkpoint por macro-F1 de validación; empate conserva primero. Guardar mejor y último checkpoint, optimizador/RNG y época; reanudar desde última época completa. No entrenar de nuevo corridas completas con identidad verificada. Una época parcial puede repetirse tras desconexión. No borrar bloqueos automáticamente.

Diagnóstico previo: tiempo/época, memoria, finitud de gradientes, métricas y señales del mecanismo. No prometer duración hasta medir GPU. Cinco semillas×25épocas=125épocas como techo de este candidato; no incluye HPO, rivales ni ablaciones. El plazo no convierte un piloto en resultado confirmatorio.

## Comparación y tamaño final
Primaria macro-F1; delta práctico0.02 heredado. Familia final: Top10 completo más baselines fuertes E2, sin excluir rivales por resultados. Congelar IDs y hashes; no confundir las13 arquitecturas del cierre histórico con una familia final ya auditada. La selección descriptiva del mejor rival no reduce la familia. Corridas históricas solo se reutilizan si coinciden datos/preprocesamiento/configuración/semilla/entorno y evidencias; de lo contrario se presentan aparte.

Final: al menos10semillas o más por potencia≥0.90 por contraste, según diferencias pareadas del piloto contra TODOS los rivales. Planificación conservadora alpha0.05/m y sensibilidad a SD; no estimar potencia suficiente desde medias agregadas ni adoptar el R de E2. Reportar potencia conjunta sin asumir independencia de contrastes. Pruebas previstas: t pareado, Wilcoxon y permutación pareada, Holm por prueba sobre familia completa; interpretación conservadora si discrepan. IC por paciente con≥2.000 remuestreos, efectos e IC; semillas no son pacientes. Para afirmar R3: dirección favorable frente a todos, delta, pruebas ajustadas y condiciones completas de guía. Nadeau–Bengio solo con diseño de particiones repetidas que lo justifique; no agregarlo mecánicamente a semillas en un split fijo.

## Ablaciones y decisiones
Familia secundaria: sin contraste, sin amortiguación, sin contexto; control adicional sinD4. Mismas semillas/configuración para cada contraste, Holm dentro de familia. Son intervenciones del mecanismo, no garantía de tres contribuciones inéditas. Si el modelo falla o cambia, registrar nuevo diseño, presupuesto consumido y clasificación exploratoria. No seleccionar variante usando reserva. Cinco semillas de desarrollo no permiten proclamar equivalencia.

## Criterios de paso
El piloto requiere datos verificados y entorno GPU compatible; código probado sintéticamente. La fase confirmatoria además requiere revisión de novedad, tercero que repita búsquedas, datasets externos auditados, confirmación no expuesta, familia/configuraciones congeladas, potencia y tagGit. No se presenta este borrador como si cumpliera esas condiciones. Declarar asistencia IA y defensa del código por el autor.

Con cinco pares no nulos, el mínimo p bilateral exacto de Wilcoxon es 0,0625: el piloto no puede satisfacer ese requisito confirmatorio ni siquiera antes de Holm. No convertir “sin significancia” en equivalencia. La planificación final debe contemplar también la discreción de las pruebas, no solo potencia del t pareado.
