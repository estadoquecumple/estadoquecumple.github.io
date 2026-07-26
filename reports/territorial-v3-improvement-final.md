# Informe final de mejora funcional — Laboratorio Territorial V3

Fecha: 2026-07-26  
Rama de trabajo: `mejora-laboratorio-territorial-v3`  
Base inicial: `bae90ce`; V3 integrada: `f0f802e`.

## Resultado

- La auditoría inicial quedó preservada en
  `reports/territorial-v3-improvement-initial.md` y su inventario resumido en
  `reports/territorial-v3-controls-initial.json`.
- Las auditorías ya no cuentan comentarios ni presencia textual como cobertura.
  El runner conserva evidencia del resultado real de Playwright y el contrato
  final relaciona los 48 botones visibles con manejador e interacción ejecutada.
- Se eliminó `innerHTML` de los componentes territoriales. Nombres, escenarios,
  comparaciones, consecuencias, listas y datos externos se construyen con nodos
  y `textContent`.
- La exportación CSV neutraliza `=`, `+`, `-` y `@`, escapa comillas y cita todas
  las celdas. Las URL externas activas se restringen a HTTP(S).
- Se añadió el adaptador único `scenarioToMapCollections`, que actualiza las ocho
  colecciones requeridas después de cada render del escenario, incluido
  deshacer/rehacer, carga e importación.
- La unión conserva las geometrías de los integrantes en un `MultiPolygon`
  visible y el mapa diferencia unidades creadas, transformadas, suprimidas,
  funcionales y seleccionadas.
- `calculateScenarioDiff(before, operation, after, context)` usa los estados
  estructurados para diferencias de unidades, niveles, autoridades,
  competencias, financiación, planeación, población/capacidad, ruta jurídica,
  transición, supuestos y riesgos. Ya no interpreta el resumen con expresiones
  regulares.
- Los niveles admiten campos institucionales separados en el esquema V3.
- La topología V3 documenta tolerancia de `0.00001°`, repara anillos y distingue
  rook, queen y discontinuidad con descarte por caja envolvente.
- Solo Bogotá–Sabana, RAP Caribe → RET y Colombia sin departamentos permanecen
  habilitados. Los demás se muestran deshabilitados como “No disponible
  todavía” y no crean escenarios.
- SAVIA conserva el resultado `unavailable` cuando no existe selección/evidencia
  y no presenta una recomendación incondicional.
- El workflow de Pages ejecuta `npm ci`, `npm run validate` y `npm run lab:e2e`
  en un job bloqueante del build y el despliegue.

## Clasificación territorial

El índice incorporado contiene exactamente 1.122 unidades, pero no conserva el
campo oficial `MPIO_TIPO`. Para no inventar la clasificación, el normalizador
acepta municipio, distrito, Distrito Capital y área no municipalizada únicamente
cuando el campo es suministrado; las 1.122 entradas actuales se reportan como
`unavailable`. El conteo reproducible y la limitación están en
`reports/territorial-unit-types.json`.

## Topología

El informe reproducible `reports/territorial-topology-quality.json` registra
total, promedio de vecinos rook, unidades aisladas y contactos puntuales para
departamentos y unidades locales, además de tolerancia, definiciones y casos
revisados. El clasificador tolerante está cubierto con casos rook, queen,
discontinuos y anillos inválidos.

## Seguridad probada

Las pruebas cubren nombres con HTML, renderizado textual, prefijos de fórmula
CSV y URL `javascript:`. La importación continúa validada por Zod y el enlace
compartido usa el mismo esquema; ningún contenido importado se inserta como HTML.

## Evidencia y pruebas

- Vitest: 4 archivos y 41 pruebas aprobadas en la ejecución previa a la
  validación integral.
- Playwright: 36 ejecuciones aprobadas en escritorio y móvil; incluye mapa
  disponible, fallo cartográfico y alternativa tabular.
- Contrato de botones: 48 de 48 con manejador e interacción Playwright ejecutada.
- La evidencia exacta está en
  `reports/territorial-v3-playwright-evidence.json` y el resultado por control en
  `reports/territorial-v3-controls-final.json`.

## Limitaciones reales

- Falta incorporar una fuente que preserve `MPIO_TIPO`; se muestra no disponible
  en vez de inferirlo por nombre o código.
- Las geometrías incluidas son simplificadas. La unión conserva polígonos en un
  `MultiPolygon`, pero un disolvido topológico sin fronteras internas y cortes
  geométricos productivos requieren una biblioteca/servicio geométrico robusto.
- El informe de solapes parte de los archivos topológicos versionados; una
  revisión completa exige geometría oficial de mayor resolución.
- Población, capacidad, desempeño fiscal y demás indicadores siguen sin
  cobertura suficiente para puntuar SAVIA; por eso permanecen `No disponible`.
- Los catálogos jurídicos orientan la exploración y no constituyen concepto
  jurídico; las fechas de revisión deben mantenerse.

Los hashes de los commits de trabajo, integración y `main` publicado se completan
en el informe de entrega después de la integración. No se usó pull request,
interfaz web de GitHub, force push ni cherry-pick.
