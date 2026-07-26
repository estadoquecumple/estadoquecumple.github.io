# Auditoría inicial de mejora funcional — Laboratorio Territorial V3

Fecha: 2026-07-26  
Rama: `mejora-laboratorio-territorial-v3`  
Base: `bae90ce` (`origin/main`)  
V3 integrada: `f0f802e` es antepasado de la base.

## Método

Se inspeccionaron directamente los componentes RAÍCES, SAVIA, SEMILLAS, mapa y
salidas; el modelo de escenarios, selección, consecuencias, ejemplos, catálogo
jurídico y subdivisiones; los GeoJSON e índices; las auditorías Node; las pruebas
Vitest y Playwright; y el workflow. La clasificación exige que el control tenga
manejador, mutación o resultado observable, manejo de error y una interacción
Playwright que compruebe el efecto. La aparición textual, comentarios, selectores
y mensajes `aria-live` aislados no se aceptaron como evidencia.

## Hallazgos por familia visible

| Control / selector | Archivo y manejador | Estado / efecto visible | Efecto cartográfico | Error | Playwright real | Clasificación |
|---|---|---|---|---|---|---|
| Modos `[data-mode]` | `TerritorialLab.astro`, `setMode` | cambia workspace y salidas | cambia leyenda/capas | modo canónico por defecto | sí | funcional |
| Búsqueda `[data-territory-search]` | `TerritorialLab.astro`, teclado | selecciona por primer resultado | carga departamento, resalta y centra | mensaje de carga | parcial: código, no lista/desambiguación | parcial |
| Selectores departamento/unidad local | `TerritorialLab.astro`, `change` | ficha, tabla y selección | carga y centra | `catch` de red | sí | funcional |
| Capas `[data-layer]` | `TerritorialLab.astro`, `change` | visibilidad; datos pendientes deshabilitados | sí | estado deshabilitado | sí solo departamentos | parcial |
| Función `[data-function-route]` | `TerritorialLab.astro`, `change` | cadena institucional | no | opción vacía | sí | funcional |
| Comparar RAÍCES | `TerritorialLab.astro`, `click` | exige dos unidades | no | controlado | sí | funcional |
| Pesos / evaluar SAVIA | `TerritorialLab.astro` | cambia pesos; sin evidencia muestra insuficiencia | no | faltantes explícitos | sí sin datos | parcial |
| Escenarios CRUD | `TerritorialLab.astro` + `ScenarioStore` | estado completo en IndexedDB | render de geometría existente | `catch` de almacenamiento | parcial | parcial |
| Selección completa/invertir/limpiar | `TerritorialLab.astro` | muta selección | actualiza dos fuentes | mensajes | parcial | parcial |
| Vecinos/contiguos | `connectedSelection` | muta selección | resalta | topología no disponible | sí | parcial: topología por segmentos exactos redondeados |
| Dibujo y selección espacial | mapa + laboratorio | candidatos, aplicar/cancelar | dibujo y selección | sin candidatos | parcial | parcial |
| Unión | `mergeUnits` | unidad/membresías/historial | geometría de unión queda `null` | valida mínimo/existencia | sí, sin disolución | nominal |
| División por grupos | `splitByMembership` | crea unidades/membresías | geometrías quedan `null` | duplicados y faltantes | parcial | parcial |
| División geométrica | `splitByGeometry` | solo registra corte experimental | no crea partes | worker informa error | sí, solo texto | nominal |
| Supresión departamental | manejador directo | suprime y añade nivel/transición | unidades suprimidas si tenían geometría | solo `confirm()` | no prueba requisitos | parcial |
| Nuevo nivel | `createLevel` | crea nivel | no aplica | identidad básica | sí | parcial: datos institucionales concatenados en `nature` |
| Subdivisiones | `subdivisionModels` | resultado descriptivo | no | modelo requerido | sí | parcial |
| Gobierno/competencias/finanzas/planeación | funciones de escenario | mutan arreglos/historial | solo si la unidad ya tiene geometría | validación de esquema | sí | funcional parcial |
| Deshacer/rehacer | `ScenarioTimeline` | restaura estado | `renderScenario` | no-op seguro | sí | funcional |
| Importar/compartir | Zod + JSON/base64 | carga escenario | geometrías validadas solo como `unknown` | rechazo controlado | parcial | parcial |
| Exportar JSON/GeoJSON | manejadores de descarga | archivo | GeoJSON de unidades con geometría | esquema JSON | no inspecciona descarga | parcial |
| Exportar CSV | interpolación directa | archivo | no | sin protección de fórmulas | no | roto |
| Comparación | `comparison` con `innerHTML` | tabla antes/después | no | retorno silencioso | sí | roto por inyección HTML |
| Cámaras/fondo/reintento | `TerritoryMap.astro` | cambia vista/fondo/reintenta | sí | estado error + tabla | sí | funcional |
| Alternativa tabular/filtro/checks | `TerritorialLab.astro` | filtra y selecciona | resalta | tabla base | parcial | funcional |
| Ejemplos | `examples-v3.ts` + carga | texto y escenario genérico | selección parcial | no disponibilidad no distinguida | ejemplos parciales | nominal |
| Pestañas de consecuencias | `TerritorialLab.astro` | cambia dimensión visible | no | no aplica | comentario, no toda pestaña | parcial |

## Defectos estructurales iniciales

- `audit-territorial-v3-functional.mjs` certificaba controles por coincidencias
  textuales, cambiaba todas las clasificaciones a “working” y reescribía el
  informe; no ejecutaba Playwright.
- `audit-territorial-v3-buttons.mjs` aceptaba comentarios de una spec como
  cobertura.
- El índice de 1.122 unidades no conserva `MPIO_TIPO`; todos sus elementos
  carecen de clasificación oficial.
- La topología usa igualdad de segmentos redondeados, sin reparación, índice
  espacial, tolerancia geométrica, solapes ni métricas de calidad.
- No existe un adaptador único `scenarioToMapCollections`.
- La unión y las divisiones no materializan las geometrías requeridas.
- Las consecuencias se recalculan desde `op.summary`, no desde
  `before/operation/after/context`.
- Hay `innerHTML` con nombres de escenarios y nombres seleccionados.
- El CSV permite fórmulas.
- Solo tres ejemplos debían estar disponibles; los demás aparentaban ser
  cargables.
- El workflow ejecutaba únicamente `npm run check`, no `validate` ni `lab:e2e`.

Este archivo es la línea base inmutable y no será regenerado por las auditorías.
