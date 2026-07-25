# PROMPT MAESTRO PARA CODEX
# LABORATORIO TERRITORIAL CAMS V2
# LIMPIEZA DE LEGADO + MODOS RAÍCES/SAVIA/SEMILLAS + MODELADOR TERRITORIAL

Trabaje directamente sobre el repositorio Astro actual de `estadoquecumple/estadoquecumple.github.io`, en una rama nueva denominada `laboratorio-territorial-v2`.

## Mandato

Transforme el Laboratorio Territorial CAMS actual en una herramienta pública de análisis y construcción de escenarios territoriales.

La V1 ya corrigió el renderizado de MapLibre, procesa 33 entidades departamentales, carga municipios por código DIVIPOLA y tiene pruebas reales. No deshaga esa corrección.

La V2 debe:

1. eliminar entradas, textos, índices, rutas y datos heredados que ya no correspondan al sitio actual;
2. diferenciar de forma inequívoca RAÍCES, SAVIA y SEMILLAS;
3. permitir seleccionar departamentos y municipios;
4. permitir crear, unir, dividir, transformar, conservar o suprimir unidades y niveles territoriales dentro de escenarios exploratorios;
5. permitir cambiar la naturaleza institucional, las autoridades, las competencias, la financiación, la planeación y los mecanismos de coordinación;
6. recalcular resultados cuando los datos lo permitan;
7. distinguir siempre dato observado, cálculo e hipótesis;
8. clasificar preliminarmente el impacto jurídico, sin presentarlo como concepto legal;
9. guardar, comparar, exportar e importar escenarios;
10. mantener accesibilidad, rendimiento, trazabilidad y metodología pública.

No haga `git commit`, `git merge` ni `git push`.

No entregue solamente un plan. Implemente y valide toda la V2.

---

# 1. Auditoría y limpieza completa de legado

Antes de editar, ejecute una auditoría integral.

Busque y clasifique:

- referencias a `camscarlosmartinez.github.io`;
- nombres antiguos del repositorio;
- rutas antiguas;
- enlaces rotos;
- entradas viejas del buscador;
- tarjetas que anuncien el laboratorio como “en desarrollo” o “prototipo” cuando ya existe;
- textos que describan una arquitectura anterior;
- datos duplicados;
- escenarios duplicados;
- componentes no usados;
- scripts no usados;
- CSS no usado;
- imports anteriores de MapLibre;
- referencias fijas a `11.geojson`;
- `localStorage` o IndexedDB con claves de versiones anteriores;
- informes SEO desactualizados;
- `site-index.json`, `llms.txt`, sitemap y buscador con entradas obsoletas;
- artefactos o capturas que estén siendo rastreados por Git;
- JSON públicos anteriores que ya no tengan consumidor;
- rutas de “demo”, “prototipo” o “laboratorio anterior”;
- textos duplicados entre Observatorio, Estado que Cumple y Laboratorio.

Cree:

`reports/legacy-audit.json`

Cada elemento debe indicar:

- archivo;
- referencia;
- categoría;
- decisión: conservar, migrar, reemplazar o eliminar;
- justificación.

Después realice la limpieza.

Reglas:

- no cree una carpeta `legacy`;
- Git conserva el historial;
- elimine archivos sustituidos;
- no conserve dos fuentes del mismo contenido;
- regenere buscador, sitemap, `site-index.json`, `llms.txt` e informes;
- actualice la portada del Observatorio y Estado que Cumple para enlazar la V2;
- elimine menciones públicas a una versión anterior si ya no aportan valor;
- mantenga un historial técnico breve en Archivo, no en la interfaz principal.

Añada una migración de estado local:

```ts
const LAB_SCHEMA_VERSION = 2;
```

Si encuentra claves antiguas, migre solo preferencias compatibles y elimine datos incompatibles de forma segura. Muestre un aviso único:

`El Laboratorio fue actualizado. Los escenarios incompatibles de la versión anterior no se reutilizaron.`

---

# 2. Principio conceptual

Los tres instrumentos no son pestañas decorativas ni tres nombres para el mismo mapa.

## RAÍCES

Pregunta:

`¿Qué Estado existe realmente sobre este territorio?`

Debe mostrar el sistema actual, sin editarlo.

## SAVIA

Pregunta:

`¿Qué capacidad, escala y viabilidad tiene este territorio o agrupación?`

Debe evaluar unidades actuales o agrupaciones candidatas.

## SEMILLAS

Pregunta:

`¿Qué alternativa institucional puede diseñarse, compararse y pilotarse?`

Debe permitir editar escenarios.

Cada modo debe cambiar:

- herramientas disponibles;
- panel izquierdo;
- comportamiento del mapa;
- panel derecho;
- leyenda;
- resultados;
- descargas;
- URL;
- instrucciones;
- atajos;
- colores de interacción.

La selección debe conservarse entre modos solo cuando tenga sentido.

---

# 3. Diseño general de interfaz

La página debe estructurarse así:

```text
┌─────────────────────────────────────────────────────────────────────┐
│ LABORATORIO TERRITORIAL CAMS                                       │
│ explicación, versión, fecha de datos, estado y advertencia          │
├─────────────────────────────────────────────────────────────────────┤
│ RAÍCES — VER | SAVIA — EVALUAR | SEMILLAS — DISEÑAR                │
├──────────────────┬────────────────────────────┬─────────────────────┤
│ PANEL CONTEXTUAL │ MAPA                       │ ANÁLISIS / RESULTADO│
│                  │                            │                     │
├──────────────────┴────────────────────────────┴─────────────────────┤
│ ESCENARIO | HISTORIAL | METODOLOGÍA | FUENTES | DESCARGAS          │
└─────────────────────────────────────────────────────────────────────┘
```

En móvil:

- selector de modo fijo y compacto;
- pestañas: Controles, Mapa, Resultados, Método;
- mapa no menor de 440 px;
- controles accesibles;
- panel inferior deslizable;
- no esconder resultados esenciales tras hover.

Cree o reorganice componentes funcionalmente separados para:

- navegación de modo;
- espacio de trabajo RAÍCES;
- espacio de trabajo SAVIA;
- espacio de trabajo SEMILLAS;
- búsqueda territorial;
- selección;
- capas;
- inspección actual;
- evaluación de capacidad;
- construcción de escenarios;
- edición de estructura territorial;
- gobierno;
- competencias;
- financiación;
- planeación;
- transición;
- impacto jurídico;
- comparación;
- historial;
- metodología;
- tabla accesible;
- descargas.

---

# 4. RAÍCES — modo de diagnóstico actual

RAÍCES es inmutable. No permite cambiar límites ni autoridades.

## Herramientas

- seleccionar departamento;
- seleccionar municipio;
- búsqueda por nombre o DIVIPOLA;
- zoom territorial;
- capas;
- superposición institucional;
- inspección de competencias;
- rastreo de una función pública;
- comparación de dos territorios actuales;
- exportación de ficha.

## Capas iniciales

- departamentos;
- municipios;
- distritos;
- áreas no municipalizadas cuando existan;
- RAP y RAPE cuando haya datos;
- áreas metropolitanas;
- regiones PDET;
- CAR;
- cuencas disponibles;
- tipologías DNP;
- población;
- desempeño fiscal;
- desempeño municipal;
- SGR;
- SECOP agregado;
- centros urbanos o nodos;
- fuentes y fecha.

No simule capas que no tengan datos.

## Ficha RAÍCES

Al seleccionar una unidad:

- identidad;
- código;
- nivel;
- unidad superior;
- población;
- área;
- estructura político-administrativa;
- autoridades;
- competencias;
- ingresos disponibles;
- dependencia fiscal;
- proyectos;
- contratos;
- capas institucionales superpuestas;
- vacíos de datos;
- fuentes;
- fecha.

## Rutas de función

Permita seleccionar una función:

- salud;
- educación;
- agua;
- transporte;
- catastro;
- residuos;
- vivienda;
- ambiente;
- contratación;
- defensa jurídica;
- planeación.

Muestre:

`quién regula → quién financia → quién planifica → quién ejecuta → quién controla`

Si la información no está completa, muestre el vacío.

---

# 5. SAVIA — modo de evaluación

SAVIA no modifica el escenario oficial. Evalúa:

- una unidad actual;
- varias unidades seleccionadas;
- una agrupación candidata;
- una unidad creada en SEMILLAS.

## Dimensiones

- capacidad fiscal;
- capacidad administrativa;
- estabilidad y profesionalización;
- información y archivo;
- ejecución y mantenimiento;
- accesibilidad;
- escala poblacional;
- relaciones funcionales;
- coordinación;
- sostenibilidad;
- autonomía;
- representación;
- riesgo de captura;
- costo de transición;
- viabilidad jurídica preliminar.

No reduzca todo a una puntuación.

Muestre un perfil multidimensional.

## Pesos

El usuario puede cambiar pesos, pero:

- debe ver los valores originales;
- debe ver la fórmula;
- debe poder restablecer;
- debe distinguir valoración CAMS de preferencia del usuario;
- no debe generar una falsa conclusión científica.

## Resultados posibles

SAVIA puede recomendar de forma condicionada:

- conservar capacidad plena;
- conservar con asistencia;
- compartir administración;
- regionalizar función;
- crear autoridad funcional;
- delegar temporalmente;
- pilotar;
- requerir mayor evidencia.

Nunca mostrar:

`Este modelo es el mejor`.

Mostrar:

`Bajo estos criterios y pesos, esta alternativa presenta mayor coherencia en estas dimensiones y mayores riesgos en estas otras.`

## Comparador

Permita comparar:

- municipio A frente a municipio B;
- agrupación A frente a agrupación B;
- sistema actual frente a escenario;
- misma unidad con diferente distribución competencial.

---

# 6. SEMILLAS — modelador territorial

SEMILLAS debe ser un editor real de escenarios.

El estado actual debe aparecer bloqueado como referencia.

El usuario debe crear o duplicar un escenario para editar.

## Selección territorial

Implemente:

- clic individual;
- Ctrl/Cmd + clic para selección múltiple;
- Shift + clic para rango cuando aplique;
- búsqueda;
- seleccionar departamento completo;
- seleccionar municipios de un departamento;
- seleccionar unidades contiguas;
- seleccionar vecinos;
- selección por rectángulo;
- selección por polígono;
- selección por filtro;
- invertir selección;
- limpiar selección.

Use una integración compatible con MapLibre para dibujo y selección. Puede usar Terra Draw o una integración equivalente, siempre que quede empaquetada y probada.

## Operaciones con unidades

### Unión

Permitir unir:

- municipios;
- departamentos;
- unidades creadas;
- agrupaciones funcionales.

Crear como:

- región;
- departamento;
- provincia;
- distrito funcional;
- área metropolitana;
- ciudad-región;
- mancomunidad;
- unidad administrativa compartida;
- unidad personalizada.

La unión no implica automáticamente la desaparición política de los miembros. El usuario debe escoger:

- conservar integrantes como entidades políticas;
- conservarlos como subdivisiones administrativas;
- absorberlos;
- mantenerlos solo como identidades o comunas;
- mantener límites estadísticos sin administración propia.

### División

Dos modalidades:

#### División por unidades existentes

Ejemplo:

- dividir un departamento asignando municipios a dos nuevas unidades;
- separar municipios de una región;
- crear una nueva unidad con municipios seleccionados.

Esta modalidad permite recalcular datos completos.

#### División geométrica experimental

Permitir dibujar una línea o polígono de corte.

Reglas:

- marcar como `experimental`;
- no redistribuir automáticamente población, ingresos, contratos o proyectos si no existen datos submunicipales;
- mostrar geometría, área y unidades intersectadas;
- clasificar resultados fiscales y poblacionales como `sin estimación`, o usar una estimación explícita de alta incertidumbre solo si existe una fuente granular válida;
- no usar prorrateo por área como si fuera dato real;
- registrar el método.

Use operaciones geoespaciales reproducibles y Web Worker.

### Supresión o transformación

Permitir dentro del escenario:

- mantener departamentos;
- suprimir el nivel departamental;
- convertir departamentos en regiones administrativas;
- convertirlos en regiones político-administrativas;
- conservarlos como circunscripciones sin administración;
- reemplazarlos por regiones;
- crear un nivel supradepartamental;
- crear provincias;
- fortalecer municipios;
- crear distritos funcionales variables;
- crear ciudades-región;
- crear administración nacional temporal;
- cambiar relaciones de subordinación o coordinación.

No borre datos originales. Use estados:

- active;
- transformed;
- absorbed;
- statistical-only;
- political-only;
- administrative-only;
- suppressed-in-scenario.

### Nuevos niveles

Permitir definir:

- nombre;
- posición jerárquica;
- naturaleza;
- competencias;
- autoridad;
- financiación;
- planeación;
- control;
- relación con niveles superiores e inferiores.

No limite el editor a Nación–Departamento–Municipio.

---

# 7. Editor institucional

Cada escenario debe permitir configurar separadamente:

## Estructura territorial

- niveles;
- unidades;
- geometrías;
- pertenencia;
- capital o nodo;
- asimetría;
- relaciones.

## Gobierno

- elección directa;
- elección por corporación;
- nombramiento;
- procedimiento híbrido;
- ejecutivo colegiado;
- administrador profesional;
- separación entre dirección política y administración;
- duración;
- reelección como hipótesis;
- corporación representativa;
- mecanismos de participación.

## Competencias

Matriz para:

- educación;
- salud;
- agua;
- residuos;
- transporte;
- vivienda;
- ambiente;
- catastro;
- tributación;
- contratación;
- defensa jurídica;
- seguridad;
- infraestructura;
- planeación;
- desarrollo productivo;
- ciencia y tecnología;
- cultura;
- cuidado.

Asignar a:

- Nación;
- región;
- departamento;
- provincia;
- distrito funcional;
- municipio;
- comuna;
- unidad personalizada.

Permitir:

- exclusiva;
- concurrente;
- compartida;
- delegada;
- subsidiaria;
- temporal.

## Financiación

- impuestos propios;
- impuestos compartidos;
- transferencias;
- igualación;
- regalías;
- fondos regionales;
- presupuesto plurianual;
- financiación por misión;
- contribuciones metropolitanas;
- tarifas;
- endeudamiento;
- cofinanciación.

No calcule recaudos futuros sin modelo sustentado.

## Planeación

- horizonte;
- relación entre planes;
- plan de gobierno;
- plan estratégico;
- contratos territoriales;
- programas de misión;
- continuidad;
- revisión;
- evaluación.

## Intervención subsidiaria

Definir cuándo una unidad:

- recibe asistencia;
- comparte administración;
- pierde temporalmente una competencia;
- es intervenida;
- recupera la competencia;
- es evaluada.

---

# 8. Modelo de datos V2

No vincule directamente nivel territorial y geometría.

Cree un modelo tipado y versionado.

Ejemplo conceptual:

```ts
interface TerritorialScenario {
  schemaVersion: 2;
  id: string;
  name: string;
  version: string;
  status: 'draft' | 'exploratory' | 'published' | 'archived';
  baseScenarioId: string;
  createdAt: string;
  updatedAt: string;
  author: string;
  levels: AdministrativeLevel[];
  units: TerritorialUnit[];
  memberships: Membership[];
  governments: GovernmentModel[];
  competences: CompetenceAssignment[];
  finances: FinanceRule[];
  planning: PlanningRule[];
  interventions: InterventionRule[];
  assumptions: Assumption[];
  risks: Risk[];
  legalImpacts: LegalImpact[];
  transitions: TransitionStep[];
  sources: SourceReference[];
  history: ScenarioOperation[];
}
```

## Unidad territorial

Debe distinguir:

- identidad;
- geometría;
- estatus político;
- estatus administrativo;
- estatus estadístico;
- unidad superior;
- integrantes;
- autoridades;
- código interno CAMS;
- códigos oficiales de origen.

## Operaciones

Use un registro inmutable:

- select;
- create-unit;
- merge-units;
- split-by-membership;
- split-by-geometry;
- transform-unit;
- suppress-unit;
- restore-unit;
- move-membership;
- create-level;
- remove-level;
- assign-competence;
- change-government;
- change-finance;
- change-planning.

Esto debe alimentar:

- deshacer;
- rehacer;
- historial;
- comparación;
- exportación.

---

# 9. Geometría

Mantenga MapLibre como renderizador.

Use módulos geoespaciales específicos para:

- union;
- dissolve;
- intersect;
- difference;
- booleanIntersects;
- booleanTouches;
- centroid o centerOfMass;
- bbox;
- area.

Reglas:

- ejecutar operaciones pesadas en Web Worker;
- validar Polygon/MultiPolygon;
- conservar IDs únicos;
- mostrar errores topológicos;
- simplificar solo para visualización;
- conservar una geometría de cálculo separada si es necesario;
- no escribir geometría editada sobre la cartografía oficial;
- actualizar MapLibre mediante `setData()` o `updateData()`.

---

# 10. Resultados y recálculo

Cuando la unidad está formada por municipios completos, recalcular:

- población;
- área;
- municipios;
- departamentos de origen;
- ingresos disponibles;
- dependencia;
- proyectos SGR;
- contratos agregados;
- tipologías;
- cobertura de datos;
- población promedio;
- concentración;
- distancia a nodo si existe método;
- proporción urbana/rural si hay datos.

Clasifique:

- observed;
- calculated;
- assumption;
- unavailable.

Cuando exista división geométrica sin datos submunicipales:

- área: calculated;
- municipios intersectados: calculated;
- población: unavailable o assumption explícita;
- finanzas: unavailable;
- SGR/SECOP: unavailable salvo georreferenciación suficiente;
- advertencia visible.

No permita exportar una hipótesis como dato observado.

---

# 11. Impacto jurídico preliminar

Cree una clasificación pedagógica:

- compatible con figura vigente;
- posible mediante convenio o asociación;
- requiere reglamentación o acto administrativo;
- requiere ley ordinaria;
- requiere ley orgánica;
- probablemente requiere reforma constitucional;
- requiere revisión jurídica especializada.

El sistema debe justificar qué característica activó la categoría.

Ejemplos:

- asociación entre entidades;
- RAP;
- RET;
- área metropolitana;
- cambio de competencias;
- creación de departamento;
- supresión del nivel departamental;
- cambio en elección de gobernador;
- cambio en elección de alcalde;
- creación de una entidad territorial no prevista;
- cambio del núcleo de autonomía.

No emita concepto jurídico definitivo.

Incluya fuentes normativas y fecha.

---

# 12. Persistencia, exportación y colaboración

Sin backend, implemente:

- IndexedDB para escenarios locales;
- listado de escenarios;
- crear;
- duplicar;
- renombrar;
- archivar;
- eliminar con confirmación;
- guardar automático;
- indicador de guardado;
- importar JSON;
- exportar JSON;
- exportar GeoJSON;
- exportar CSV de resultados;
- exportar ficha metodológica;
- imprimir;
- generar enlace compartible para configuraciones pequeñas;
- descargar archivo para escenarios grandes.

No almacene datos personales.

## Compatibilidad

Importador:

- rechaza esquemas desconocidos;
- valida con Zod;
- migra V1 solo si es seguro;
- muestra errores detallados;
- nunca ejecuta código importado.

---

# 13. Comparación

Permita:

- actual vs escenario;
- escenario A vs escenario B;
- modo espejo;
- deslizador visual cuando sea útil;
- tabla de diferencias;
- unidades creadas, transformadas y suprimidas;
- cambios de competencias;
- cambios de autoridades;
- cambios fiscales;
- cambios de planeación;
- riesgos;
- impacto jurídico;
- cobertura de datos.

No use solo verde/rojo.

---

# 14. Metodología visible

Cada escenario debe mostrar:

- quién lo creó;
- versión;
- fecha;
- base;
- operaciones;
- fuentes;
- supuestos;
- límites;
- datos faltantes;
- cálculos;
- hipótesis;
- impacto jurídico preliminar;
- historial.

Añada una leyenda permanente:

- dato observado;
- cálculo;
- hipótesis;
- sin dato.

---

# 15. Limpieza de interfaz pública

Después de implementar:

- elimine tarjetas viejas del laboratorio;
- sustituya capturas, textos y enlaces anteriores;
- actualice Observatorio;
- actualice Estado que Cumple;
- actualice Aplicaciones;
- actualice buscador;
- actualice `site-index.json`;
- actualice `llms.txt`;
- regenere sitemap;
- regenere informe SEO;
- actualice Archivo con una nota breve:
  `Laboratorio Territorial V2 — modelador de escenarios`;
- no muestre dos versiones del laboratorio.

---

# 16. Rendimiento

- carga inicial departamental;
- municipios bajo demanda;
- cache de archivos ya cargados;
- selección multi-departamental;
- worker para geometría y agregación;
- debounce;
- no recalcular todo ante cada movimiento;
- división de bundles;
- carga dinámica de editor SEMILLAS;
- RAÍCES debe cargar más rápido que SEMILLAS;
- MapLibre y herramientas de dibujo solo en el laboratorio;
- advertir tamaño de exportaciones.

Evalúe el warning de bundle de MapLibre, pero no sacrifique estabilidad solo por eliminarlo.

---

# 17. Accesibilidad

- todas las operaciones del mapa deben tener alternativa por búsqueda/lista;
- tabla de selección;
- lista de unidades seleccionadas;
- botones de unión/división;
- foco visible;
- atajos documentados;
- `aria-live` para operaciones;
- no depender de color;
- confirmación para supresión;
- recuperación mediante deshacer;
- alternativa textual para escenario;
- teclado para selección;
- tabla funcional sin WebGL.

---

# 18. Pruebas

## Unitarias

- esquema V2;
- migración de estado;
- unión;
- división por municipios;
- división geométrica;
- supresión;
- transformación;
- pertenencias;
- competencia;
- gobierno;
- financiación;
- planeación;
- undo/redo;
- agregaciones;
- clasificación de resultados;
- impacto jurídico preliminar;
- importación/exportación.

## Playwright

RAÍCES:

- seleccionar departamento;
- seleccionar municipio;
- activar capas;
- abrir ficha;
- comparar territorios.

SAVIA:

- evaluar selección;
- cambiar peso;
- restablecer;
- comparar;
- comprobar advertencia metodológica.

SEMILLAS:

- crear escenario;
- seleccionar municipios;
- unir;
- crear región;
- conservar o absorber integrantes;
- cambiar naturaleza;
- suprimir nivel departamental dentro del escenario;
- asignar competencia;
- cambiar autoridad;
- configurar financiación;
- dividir por municipios;
- dibujar selección;
- deshacer;
- rehacer;
- guardar;
- recargar;
- exportar;
- importar;
- comparar con actual.

Fallo:

- WebGL;
- GeoJSON;
- IndexedDB;
- geometría inválida;
- schema incompatible.

Capturas:

- RAÍCES;
- SAVIA;
- SEMILLAS;
- comparación;
- móvil.

---

# 19. Scripts

Cree o actualice:

- `npm run lab:test`;
- `npm run lab:e2e`;
- `npm run lab:audit`;
- `npm run lab:legacy-audit`;
- `npm run validate`.

La auditoría debe fallar si:

- quedan entradas antiguas públicas;
- quedan dominios viejos;
- existen escenarios duplicados;
- existe código fijo de Bogotá;
- RAÍCES permite edición;
- SAVIA modifica el escenario oficial;
- SEMILLAS no puede guardar o exportar;
- un resultado no indica tipo;
- una división geométrica produce cifras observadas falsas;
- una operación no entra al historial;
- falta alternativa tabular;
- hay enlace roto;
- hay ruta obsoleta en sitemap o buscador.

---

# 20. Terminación

No considere terminada la V2 hasta que:

1. la auditoría de legado quede limpia;
2. no existan entradas públicas antiguas;
3. RAÍCES, SAVIA y SEMILLAS tengan interfaces distintas;
4. se puedan seleccionar municipios y departamentos;
5. se puedan unir unidades;
6. se puedan dividir por unidades existentes;
7. exista división geométrica experimental;
8. se pueda transformar o suprimir un nivel dentro de un escenario;
9. se pueda cambiar gobierno;
10. se puedan reasignar competencias;
11. se pueda configurar financiación y planeación;
12. exista impacto jurídico preliminar;
13. exista undo/redo;
14. exista guardado;
15. exista importación/exportación;
16. exista comparación;
17. se distingan observación, cálculo, hipótesis y ausencia;
18. todas las pruebas pasen;
19. `npm run validate` termine correctamente;
20. no haya commit ni push.

---

# 21. Informe final

Entregue:

- diagnóstico de entradas antiguas;
- elementos eliminados;
- elementos migrados;
- arquitectura V2;
- explicación de RAÍCES;
- explicación de SAVIA;
- explicación de SEMILLAS;
- operaciones territoriales implementadas;
- operaciones institucionales implementadas;
- modelo de datos;
- dependencias;
- impacto del bundle;
- rutas;
- capturas;
- pruebas;
- auditoría;
- limitaciones;
- fuentes jurídicas;
- comandos exactos para revisión, commit, push, merge y publicación.
