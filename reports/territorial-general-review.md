# Revisión general del Laboratorio Territorial

Fecha: 2026-07-26  
Base revisada: `6633335`

## Alcance

Se revisaron RAÍCES, SAVIA, SEMILLAS, mapa, alternativa tabular, búsqueda,
selección, topología, operaciones, escenarios, consecuencias, fuentes, datos,
seguridad, accesibilidad, escritorio, móvil, scripts de actualización,
auditorías, build y despliegue.

## Hallazgos y correcciones

1. Los 48 botones visibles conservan manejador y una interacción Playwright
   ejecutada. No se encontraron botones huérfanos.
2. Los datos de población, IDF, MDM y tipologías tenían adaptadores, pero sus
   archivos estaban vacíos. Se mantienen como `manual-required`; no se generan
   cifras ni puntajes simulados.
3. SAVIA mostraba un resultado `calculated` solo por existir una selección. Se
   corrigió: todas las dimensiones permanecen `unavailable` mientras no exista
   evidencia comparable completa.
4. Los datos parciales existentes de SGR y los conteos nacionales de SECOP no se
   mostraban. Ahora se presentan con cobertura, tipo de resultado y advertencias
   explícitas. SECOP se identifica como cobertura del sistema, no como gasto de
   la selección.
5. Se incorporó el Directorio Georreferenciado de Entidades Públicas de Función
   Pública, agregado por DIVIPOLA: 7.285 filas oficiales y 1.123 códigos. Solo se
   publican conteos, sectores, órdenes y clasificaciones; no datos personales.
6. Se añadió un registro local de fuentes y herramientas oficiales para DANE,
   Función Pública/SIGEP, SECOP II, SGR, CHIP/FUT/CUIPO y MapaInversiones. Los
   enlaces externos usan HTTPS, `noopener` y texto seguro.
7. La actualización de datos integra el nuevo adaptador SIGEP tanto en modo
   conectado como sin conexión, y la validación falla ante fuente, DIVIPOLA o
   URL inválidos.
8. Las capas de población y fiscal permanecen deshabilitadas y ahora dicen “No
   integrada”, evitando que una fuente registrada se confunda con una capa
   cartográfica ya disponible.

## Fuentes verificadas

- DANE, proyecciones municipales 2018–2042.
- Función Pública, Directorio Georreferenciado de Entidades Públicas, conjunto
  `kqut-4h4r`.
- Colombia Compra Eficiente, SECOP II, conjunto nacional `p6dx-8zbt`.
- DNP, Sistema General de Regalías, API `mzgh-shtp`.
- Contaduría General de la Nación, CHIP, FUT y CUIPO.
- DNP, MapaInversiones.

El registro técnico y las URL canónicas están en
`public/data/territorial/official-sources.json`.

## Limitaciones honestas

- La descarga municipal DANE y las series IDF/MDM no están incorporadas. Una
  página oficial o un archivo manual no equivale a datos integrados.
- CHIP y MapaInversiones se conectan como herramientas públicas externas porque
  no exponen un API estable documentado usado por este proyecto.
- El conteo SIGEP representa sede reportada, no planta de personal, capacidad ni
  cobertura del servicio.
- El agregado SGR es una muestra API de hasta 5.000 filas y no se extrapola.
- Los conteos SECOP cubren conjuntos nacionales y no se atribuyen a una unidad
  seleccionada.
