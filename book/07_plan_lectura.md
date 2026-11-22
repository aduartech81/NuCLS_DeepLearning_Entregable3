# Plan de lectura del piloto y decisiones

> Documento histórico: fechas y estados siguientes corresponden a su elaboración, no al avance actual. Consulte la [auditoría vigente](17_auditoria_cierre.md).

Complemento documental del 18 noviembre 2026. No cambia el protocolo, el código ni la receta incorporados en el cuaderno vigente. Fecha de entrega: sábado 21 noviembre, 10:00 (Bogotá).

## Qué puede resolver el piloto

Cinco semillas sirven para medir factibilidad, estabilidad y costo. Se conservan beta=0,5, lambda=1, ancho=16 y la receta fija. No se decide un nuevo diseño con la reserva E2. Cinco pares no nulos dan un mínimo p bilateral exacto de Wilcoxon de 0,0625: no permiten una afirmación confirmatoria de superioridad.

## Evidencia que se debe cotejar

| Pregunta | Evidencia | Interpretación |
|---|---|---|
| ¿Corresponden los datos al contrato? | SHA del manifiesto e imágenes; paciente y TSS disjuntos | No aceptar métricas si falla la auditoría |
| ¿Aporta la corrección? | Macro-F1 del modelo completo y de su cabeza central sobre las mismas imágenes | Diagnóstico interno; no reemplaza entrenar la ablación sin contexto |
| ¿Opera la amortiguación? | Cuantiles de V, presupuesto y norma de corrección por clase/paciente | Una compuerta constante o casi nula cuestiona el mecanismo; no demuestra calibración |
| ¿Se cumple la propiedad? | Diferencia de logits entre las ocho transformaciones y norma de corrección | Verificar tolerancia numérica; D4 no equivale a rotación arbitraria |
| ¿Es viable el costo? | Tiempo por época, memoria máxima y latencia a batch 1 | Medir los ocho pases; no comparar solo parámetros |
| ¿Es reproducible? | Semilla, configuración, entorno, checkpoints y predicciones enlazados por hash | Omitir solo corridas completas verificadas |

## Límites del mecanismo

La región central es geométrica, no una máscara nuclear. El campo receptivo cruza sus límites; desactivar contexto no elimina toda información contextual. Las anotaciones permiten cotejar centrado, pero no se sustituyen por etiquetas inferidas. La dispersión cambia con la escala del encoder: no es incertidumbre calibrada. No se normaliza ni rediseña ahora para evitar cambiar silenciosamente el candidato.

## Secuencia hacia la entrega

1. Mientras corre E3 (PCam detenido): documentación, revisión de fuentes y dashboard independientes.
2. Al terminar PCam: conservar su resumen y cuaderno ejecutado; iniciar el único cuaderno vigente de E3.
3. Tras el piloto: validar cinco corridas y sus hashes; integrar curvas, predicciones y diagnósticos disponibles. No convertir campos ausentes en ceros.
4. Dimensionar la comparación final con diferencias pareadas, familia completa y ajuste por multiplicidad. Si el plazo no permite la muestra requerida, informar el alcance observado.
5. Cotejar cada afirmación de contribución con antecedentes y ablaciones; publicar solo resultados trazables. Los datos externos siguen sujetos a licencias, fuentes y duplicados.

## Contrato para el dashboard

Cada resultado debe identificar modelo, semilla, partición, métrica, configuración y procedencia. E2 se rotula como histórico; el piloto E3 como validación exploratoria. La reserva ya observada no se presenta como prueba nueva. Hasta recibir resultados reales, no se muestran curvas ni predicciones simuladas. El cierre de PCam es una evidencia externa de E2, no un requisito de datos de CICO.
