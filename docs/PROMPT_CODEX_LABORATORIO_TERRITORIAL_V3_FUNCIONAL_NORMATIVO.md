# PROMPT MAESTRO PARA CODEX
# LABORATORIO TERRITORIAL ESTADO QUE CUMPLE V3
# FUNCIONAL, CARTOGRÁFICO, NORMATIVO Y DE CONSECUENCIAS

Trabaje directamente sobre el repositorio Astro actual:

`estadoquecumple/estadoquecumple.github.io`

Cree y utilice una rama nueva:

`laboratorio-territorial-v3-funcional`

No haga `git commit`, `git merge` ni `git push`.

No entregue únicamente un diagnóstico, wireframe, mockup o lista de tareas. Implemente una V3 funcional, coherente, probada y publicable.

---

# 0. Propósito

El Laboratorio Territorial debe dejar de ser una interfaz que registra operaciones nominales y convertirse en una herramienta pública capaz de:

1. describir la organización territorial vigente;
2. seleccionar correctamente departamentos, municipios y subdivisiones;
3. construir escenarios territoriales e institucionales;
4. distinguir figuras jurídicas vigentes de reformas legales o constitucionales;
5. mostrar las consecuencias previsibles de cada decisión;
6. cargar ejemplos pedagógicos reproducibles;
7. comparar escenarios;
8. señalar límites, incertidumbre y datos faltantes;
9. mantener la cartografía oficial del DANE como capa territorial principal;
10. ofrecer un contexto cartográfico legible con países vecinos, océanos, costas, islas y asentamientos.

La identidad principal del sitio es **Estado que Cumple**.  
**CAMS** se conserva como identidad del autor, método y sistema editorial de Carlos Arturo Martínez Sánchez.

---

# 1. Auditoría funcional obligatoria

Antes de modificar código, cree:

`reports/territorial-v3-functional-audit.json`

La auditoría debe inventariar todos los elementos interactivos de:

- RAÍCES;
- SAVIA;
- SEMILLAS;
- mapa;
- gestor de escenarios;
- comparación;
- exportación;
- navegación móvil.

Cada control debe registrar:

```json
{
  "control": "data-territory-search",
  "label": "Buscar territorio",
  "file": "src/components/territorial/RootsWorkspace.astro",
  "eventHandler": false,
  "stateMutation": false,
  "mapMutation": false,
  "visibleResult": false,
  "testCoverage": false,
  "classification": "broken",
  "decision": "implement"
}
```

Clasificaciones:

- `working`;
- `partial`;
- `misleading`;
- `broken`;
- `placeholder`;
- `obsolete`;
- `duplicate`.

La auditoría debe fallar si un botón visible no tiene:

- manejador;
- validación;
- resultado visible;
- mensaje de error;
- prueba de navegador;
- efecto real sobre mapa, selección, escenario o salida.

No considere suficiente que un botón solo emita un anuncio.

---

# 2. Fallas actuales que deben corregirse

El estado actual del repositorio presenta, como mínimo, estas fallas verificadas:

## 2.1 Controles sin funcionamiento

Implementar realmente:

- `data-territory-search`;
- checkboxes `data-layer`;
- `data-function-route`;
- `data-roots-compare`.

## 2.2 Controles que actualmente son marcadores de posición

Actualmente “Seleccionar vecinos” y “Seleccionar contiguos” solo muestran un mensaje. Deben ejecutar selección espacial real.

## 2.3 Selecciones incompletas o engañosas

Corregir:

- “Seleccionar departamento completo” no puede depender de que los municipios ya estén cargados;
- “Invertir selección” debe informar claramente el universo sobre el que opera;
- búsqueda municipal debe cargar automáticamente el departamento correcto;
- seleccionar un municipio debe resaltarlo y centrarlo;
- selección múltiple debe persistir y visualizarse;
- cambiar de departamento no debe perder selecciones sin advertencia;
- selección nacional no puede depender de un único archivo municipal cargado;
- departamentos y municipios deben tener capas de selección diferenciadas.

## 2.4 Dibujo sin selección real

La selección rectangular y poligonal debe:

1. dibujar la geometría;
2. calcular las unidades intersectadas;
3. mostrar una vista previa;
4. permitir aplicar o cancelar;
5. seleccionar realmente departamentos o municipios;
6. distinguir intersección, contención y contacto;
7. registrar la regla utilizada.

No basta con guardar la geometría dibujada.

## 2.5 División ficticia

“Dividir por municipios” no puede partir automáticamente la selección por la mitad en “Unidad A” y “Unidad B”.

Debe existir un editor de grupos donde el usuario:

- escoja la unidad padre;
- cree dos o más grupos;
- arrastre o asigne municipios;
- nombre los grupos;
- valide que no existan duplicados;
- vea municipios no asignados;
- vea continuidad territorial;
- confirme la división.

## 2.6 Supresión departamental incompleta

Los escenarios no pueden comenzar con `units: []`.

El escenario base debe materializar:

- Nación;
- 33 unidades departamentales/Distrito Capital según cartografía y clasificación;
- municipios y distritos bajo demanda;
- pertenencias;
- estatus político;
- estatus administrativo;
- estatus estadístico;
- autoridades vigentes;
- referencias legales.

“Suprimir nivel departamental” debe producir una transformación completa:

- marcar unidades afectadas;
- reasignar pertenencias;
- reasignar competencias;
- señalar autoridades que desaparecen o cambian;
- señalar recursos y controles afectados;
- crear el nivel sustituto, si existe;
- generar transición;
- clasificar impacto constitucional;
- comparar antes/después.

## 2.7 Nuevos niveles incompletos

“Crear nuevo nivel” no puede depender de `prompt()` ni usar siempre orden 2.

Debe abrir un editor con:

- nombre;
- código interno;
- orden jerárquico;
- naturaleza;
- estatus jurídico;
- cobertura;
- unidades integrantes;
- autoridad;
- corporación representativa;
- competencias;
- financiación;
- planeación;
- control;
- relación con otros niveles;
- carácter permanente, temporal o funcional.

## 2.8 Competencias incompletas

La lista de niveles debe generarse desde el escenario. No debe quedar fija en:

- Nación;
- Departamento;
- Municipio.

Cada función pública debe modelarse mediante roles:

- regulación;
- financiación;
- planeación;
- ejecución;
- operación;
- mantenimiento;
- inspección;
- vigilancia;
- control fiscal;
- control político;
- evaluación.

Cada rol puede asignarse a un nivel o unidad diferente.

## 2.9 Consecuencias inexistentes

Cambiar gobierno, financiación, competencias o planeación debe modificar un modelo de consecuencias. No basta con guardar una regla.

## 2.10 Enlace compartible incompleto

El enlace compartible actual codifica solo nombre, id e historial parcial.

Debe:

- codificar la configuración completa cuando sea pequeña;
- o generar un archivo exportable cuando exceda el límite;
- importar el parámetro compartido al abrir;
- validar esquema;
- advertir versión;
- nunca ejecutar contenido;
- preservar fuentes, supuestos y operaciones.

## 2.11 Esquemas de escenario desconectados

Unifique:

- escenarios JSON públicos V1;
- modelo V2 en TypeScript;
- ejemplos predeterminados;
- estado actual;
- escenarios importados.

Debe existir un único contrato V3 versionado.

## 2.12 Archivo heredado

Revise y elimine o migre:

`src/data/territorial/lab.ts`

No debe permanecer una segunda definición de modos o escenarios con `roots/sap/seeds`.

## 2.13 package.json

Elimine la clave duplicada `lab:e2e`.

---

# 3. Mapa base completo y legible

## 3.1 Contexto cartográfico local obligatorio

La aplicación actual usa únicamente un fondo beige.

Incorpore un mapa contextual local, liviano y funcional incluso sin red:

```text
public/data/territorial/context/
├── countries-near-colombia.geojson
├── country-borders.geojson
├── coastline.geojson
├── ocean.geojson
├── geographic-labels.geojson
├── capital-cities.geojson
└── context-manifest.json
```

Fuentes recomendadas:

- Natural Earth, escalas 1:50m o 1:110m;
- datos de dominio público;
- recorte regional alrededor de Colombia.

Cobertura mínima:

- Colombia;
- Panamá;
- Costa Rica;
- Nicaragua, si entra en vista;
- Venezuela;
- Brasil;
- Perú;
- Ecuador;
- mar Caribe;
- océano Pacífico;
- San Andrés, Providencia y Santa Catalina;
- fronteras marítimas solo si existe fuente oficial apropiada; de lo contrario no dibujarlas como oficiales.

Añada una advertencia:

`Las fronteras de países vecinos se muestran solo como contexto cartográfico. Los límites territoriales colombianos provienen de las fuentes oficiales declaradas.`

## 3.2 Mapa base externo opcional

Añada un selector:

- Atlas institucional local;
- calles y asentamientos;
- relieve, si se habilita una fuente válida;
- fondo claro;
- fondo oscuro;
- sin mapa base.

Puede usar una fuente raster/vector externa únicamente como capa opcional y con atribución. La herramienta no puede depender de ella para funcionar.

## 3.3 Orden de capas

Orden recomendado:

1. océano;
2. países vecinos;
3. costas;
4. mapa base opcional;
5. límites internacionales contextuales;
6. Colombia;
7. departamentos;
8. municipios;
9. subdivisiones internas;
10. unidades seleccionadas;
11. escenarios;
12. dibujos;
13. etiquetas.

## 3.4 Capas seleccionadas

Cree fuentes y capas específicas:

- `selected-departments`;
- `selected-municipalities`;
- `candidate-units`;
- `scenario-created`;
- `scenario-transformed`;
- `scenario-suppressed`;
- `scenario-functional`.

La selección debe verse siempre.

Use `setData()` o `updateData()` sobre fuentes GeoJSON con IDs únicos.

## 3.5 Control de cámara

Añada:

- ver Colombia completa;
- ver Caribe e islas;
- volver a selección;
- ajustar a unidad;
- conservar zoom al cambiar de modo, cuando sea lógico;
- no ocultar San Andrés por ajustar solo al territorio continental.

---

# 4. Máquina de selección territorial

Cree un estado central tipado:

```ts
interface TerritorialSelectionState {
  mode: 'raices' | 'savia' | 'semillas';
  level: 'department' | 'municipality' | 'district' | 'locality' | 'commune' | 'corregimiento' | 'custom';
  selectedIds: string[];
  primaryId: string | null;
  loadedDepartmentCodes: string[];
  selectionMethod:
    | 'click'
    | 'search'
    | 'table'
    | 'department'
    | 'neighbours'
    | 'contiguous'
    | 'rectangle'
    | 'polygon'
    | 'filter'
    | 'example';
  universe: string;
}
```

## 4.1 Comportamiento por modo

### RAÍCES

- clic simple selecciona una unidad;
- clic en departamento abre ficha;
- botón explícito “Explorar municipios”;
- no transformar;
- comparar máximo configurable;
- selección persistente entre ficha y tabla.

### SAVIA

- selección múltiple;
- cesta de evaluación;
- añadir/quitar;
- comparar agrupaciones;
- avisar cobertura de datos;
- no modificar el escenario oficial.

### SEMILLAS

- selección múltiple;
- Ctrl/Cmd + clic;
- selección espacial;
- operaciones territoriales;
- vista previa;
- deshacer;
- rehacer.

## 4.2 Búsqueda real

El buscador debe:

- buscar departamentos;
- buscar todos los municipios mediante índice nacional;
- buscar códigos DIVIPOLA;
- normalizar tildes;
- mostrar nivel;
- mostrar departamento padre;
- cargar el GeoJSON correcto;
- seleccionar;
- centrar;
- resaltar;
- actualizar ficha.

## 4.3 Vecindad y contigüidad

Genere:

```text
public/data/territorial/topology/
├── department-neighbours.json
└── municipalities/
    ├── 05.json
    ├── 08.json
    └── ...
```

Defina y documente:

- vecino por frontera compartida;
- contacto solo por punto;
- unidad insular;
- continuidad terrestre;
- continuidad funcional opcional;
- conectividad mediante corredor.

“Seleccionar vecinos”:

- añade el primer anillo.

“Seleccionar contiguos”:

- construye el componente conexo a partir de una regla o hasta un límite definido;
- permite número de anillos;
- muestra por qué cada unidad fue incluida.

No trate automáticamente un contacto puntual como frontera sustantiva sin marcarlo.

---

# 5. Catálogo jurídico-territorial

Cree un registro normativo, no una lista fija en un componente:

```text
src/data/territorial/legal/
├── legal-registry.ts
├── figure-catalog.ts
├── jurisprudence.ts
├── consequence-rules.ts
└── legal-paths.ts
```

Cada figura debe distinguir:

- entidad territorial;
- entidad administrativa;
- esquema asociativo;
- subdivisión interna;
- división estadística;
- unidad comunitaria;
- escenario constitucional.

## 5.1 Figuras vigentes o reconocidas

Incluir, como mínimo:

- Nación;
- departamento;
- municipio;
- distrito;
- territorio indígena y régimen transitorio aplicable;
- región administrativa y de planificación — RAP;
- región entidad territorial — RET;
- región de planeación y gestión;
- asociación de departamentos;
- asociación de municipios;
- asociación de distritos;
- provincia administrativa y de planificación — PAP;
- área metropolitana;
- Región Metropolitana Bogotá–Cundinamarca;
- comuna;
- corregimiento;
- localidad distrital;
- localidad de Bogotá;
- Junta Administradora Local;
- barrio;
- vereda;
- centro poblado;
- resguardo indígena;
- unidad personalizada funcional.

No trate barrios y veredas como entidades territoriales.

## 5.2 Escenarios de reforma

Incluir, con etiqueta roja:

- Estado federado;
- provincia como entidad territorial plena;
- supresión general de departamentos;
- sustitución de alcaldes o gobernadores elegidos;
- legislaturas territoriales;
- soberanía fiscal subnacional;
- municipios convertidos en comunas sin autonomía;
- regiones con potestad legislativa.

Mostrar:

`Escenario de rediseño constitucional. No corresponde a una figura vigente del ordenamiento colombiano.`

Colombia es una república unitaria. Las entidades territoriales no tienen soberanía ni función legislativa propia equivalente a un estado federado.

## 5.3 Subdivisiones internas

El modelador debe permitir:

### Municipio ordinario

- área urbana;
- área rural;
- comunas urbanas;
- corregimientos rurales;
- JAL;
- corregidor;
- barrios;
- veredas;
- centros poblados.

### Distrito especial

- localidades;
- alcalde local;
- JAL;
- fondos de desarrollo local;
- competencias distritales/locales.

### Bogotá

- localidades;
- Alcalde Mayor;
- alcaldes locales;
- JAL;
- fondos de desarrollo local;
- relación con sectores distritales.

No use una única categoría “comuna/localidad” para todo.

---

# 6. Motor de consecuencias

Cree funciones puras y reproducibles:

```text
src/data/territorial/consequences/
├── governance.ts
├── competences.ts
├── finance.ts
├── representation.ts
├── capacity.ts
├── transition.ts
├── legal.ts
├── service-delivery.ts
└── compare.ts
```

Cada operación debe recalcular una matriz de consecuencias.

## 6.1 Dimensiones obligatorias

- naturaleza jurídica;
- ruta normativa;
- autonomía;
- autoridades;
- elección o nombramiento;
- representación;
- corporaciones públicas;
- competencias;
- financiación;
- planeación;
- control político;
- control fiscal;
- control judicial;
- coordinación;
- concurrencia;
- subsidiariedad;
- capacidad administrativa;
- escala;
- proximidad;
- accesibilidad;
- continuidad territorial;
- identidad territorial;
- enfoque étnico;
- consulta previa potencial;
- prestación de servicios;
- mantenimiento;
- transición;
- costos de transición;
- riesgos de captura;
- datos faltantes;
- incertidumbre.

## 6.2 Resultado antes/después

Para cada cambio muestre:

```text
Antes
→ decisión
→ después
→ efectos directos
→ efectos condicionados
→ riesgos
→ requisitos
→ datos faltantes
```

Ejemplo:

`Departamento → Región administrativa`

Debe indicar, como mínimo:

- si conserva o no entidad territorial;
- quién gobierna;
- cómo se integra el órgano de dirección;
- qué competencias son propias o delegadas;
- cómo se financia;
- si los departamentos subsisten;
- qué cambia en representación;
- qué no cambia;
- ruta jurídica;
- transición.

## 6.3 No inventar causalidad

No afirmar:

- reducción exacta de corrupción;
- ahorro exacto;
- crecimiento futuro;
- mejora automática;
- disminución exacta de trámites.

Usar:

- efecto normativo directo;
- consecuencia administrativa probable;
- hipótesis;
- dato faltante;
- incertidumbre.

## 6.4 Comparación de tipos de gobierno

Permita comparar:

- ejecutivo elegido directamente;
- ejecutivo elegido por corporación;
- ejecutivo colegiado;
- administrador profesional nombrado;
- dirección política + administración profesional;
- autoridad intergubernamental;
- gobierno propio indígena;
- modelo federal hipotético.

Comparar:

- legitimidad;
- rendición de cuentas;
- continuidad;
- profesionalización;
- control;
- coordinación;
- riesgo de captura;
- capacidad de implementación;
- complejidad;
- ruta jurídica.

---

# 7. RAÍCES V3

RAÍCES debe ser un atlas institucional real.

## 7.1 Ficha territorial

Mostrar:

- nombre;
- código;
- naturaleza;
- unidad superior;
- subdivisiones;
- autoridades;
- forma de elección;
- competencias;
- ingresos disponibles;
- transferencias;
- indicadores;
- esquemas asociativos;
- superposiciones;
- funciones rastreadas;
- fuentes;
- fecha;
- calidad.

## 7.2 Cadena de función pública

El selector debe cambiar el contenido.

Para cada función, modelar:

- regulador;
- financiador;
- planificador;
- ejecutor;
- operador;
- mantenedor;
- inspector;
- controlador;
- nivel territorial;
- fuente normativa;
- variaciones por régimen.

No mostrar una misma frase genérica para todas las funciones.

## 7.3 Capas reales

Los checkboxes deben cambiar visibilidad.

Si una capa no tiene datos:

- deshabilitar;
- mostrar `Fuente pendiente`;
- no fingir que está disponible.

---

# 8. SAVIA V3

El SAVIA actual solo refleja pesos y selección.

Debe consumir datos reales.

## 8.1 Indicadores

Conectar, cuando haya cobertura:

- población;
- densidad;
- área;
- accesibilidad;
- desempeño fiscal;
- desempeño municipal;
- tipología;
- SGR;
- SECOP territorial;
- distancia;
- centralidad;
- continuidad;
- concentración urbana;
- capacidad administrativa.

## 8.2 Cobertura

Cada resultado debe mostrar:

- municipios cubiertos;
- municipios sin datos;
- vigencia;
- fuente;
- tipo de resultado;
- confiabilidad.

Si población, fiscal, tipologías o desempeño siguen `manual-required`, SAVIA debe marcar esas dimensiones como no disponibles, no como “evidencia parcial” genérica.

## 8.3 Perfil multidimensional

Mostrar:

- valores;
- percentiles, cuando proceda;
- peso;
- contribución;
- cobertura;
- sensibilidad;
- comparación;
- razones.

No usar una nota única como conclusión definitiva.

---

# 9. SEMILLAS V3

## 9.1 Flujo de trabajo

1. Elegir ejemplo o comenzar desde Colombia actual.
2. Elegir objetivo.
3. Seleccionar unidades.
4. Escoger operación.
5. Configurar figura.
6. Configurar gobierno.
7. Configurar competencias.
8. Configurar financiación.
9. Configurar planeación.
10. Revisar consecuencias.
11. Revisar ruta jurídica.
12. Comparar.
13. Guardar/exportar.

## 9.2 Editor jerárquico

Incorpore un árbol:

```text
Nación
├── Región
│   ├── Provincia
│   │   ├── Municipio
│   │   │   ├── Comuna
│   │   │   └── Corregimiento
```

Debe permitir:

- crear;
- mover;
- transformar;
- suprimir;
- restaurar;
- reordenar;
- vincular funcionalmente;
- conservar una unidad como estadística;
- distinguir jerarquía política de red funcional.

## 9.3 Geometría real

Al unir unidades:

- calcular geometría disuelta;
- conservar polígonos múltiples;
- advertir discontinuidad;
- asignar geometría al escenario;
- dibujarla.

Al dividir:

- crear nuevas unidades;
- crear nuevas geometrías;
- transformar la unidad padre;
- registrar datos no redistribuibles;
- mostrar antes/después.

---

# 10. Ejemplos predeterminados

Cree una biblioteca visible con botón `Cargar ejemplo`.

Cada ejemplo debe incluir:

- objetivo;
- selección;
- operaciones;
- figura;
- gobierno;
- competencias;
- financiación;
- resultados esperados;
- fuentes;
- supuestos;
- incertidumbre;
- ruta jurídica;
- recorrido guiado.

Ejemplos obligatorios:

## 10.1 Bogotá–Sabana

- Bogotá y municipios seleccionados de Cundinamarca;
- Región Metropolitana;
- servicios compartidos;
- autonomía conservada;
- hechos metropolitanos;
- comparación con área metropolitana ordinaria.

## 10.2 Pacífico Medio

- agrupación para servicios compartidos;
- contratación especializada;
- asistencia técnica;
- coordinación territorial;
- enfoque étnico y consulta cuando corresponda.

## 10.3 Municipios pequeños

- ejemplo documentado de administración compartida;
- catastro;
- defensa jurídica;
- compras;
- sistemas de información;
- mantenimiento.

## 10.4 RAP Caribe → RET

- diferenciar RAP vigente o posible;
- conversión a RET;
- requisitos;
- departamentos conservados;
- gobierno regional;
- financiación;
- incertidumbre.

## 10.5 Colombia sin departamentos

- sustitución por regiones;
- reasignación de municipios;
- gobernanza;
- competencias;
- transición;
- reforma constitucional probable.

## 10.6 Colombia federal hipotética

- “estados”;
- legislaturas hipotéticas;
- autonomía fiscal;
- relación federal;
- advertencia constitucional;
- comparación con Estado unitario regional.

## 10.7 Distrito con localidades

- distrito;
- localidades;
- alcaldes locales;
- JAL;
- fondos;
- competencias.

## 10.8 Municipio con comunas y corregimientos

- división urbana/rural;
- JAL;
- presupuesto participativo;
- barrio/vereda como unidades no territoriales.

## 10.9 Gobierno político + administrador profesional

- autoridad elegida;
- gerente profesional;
- reparto de responsabilidad;
- control;
- continuidad;
- riesgos.

Ningún ejemplo puede presentarse como propuesta definitiva de CAMS.

---

# 11. Corrección de escenarios existentes

Revise:

`public/data/territorial/scenarios/regional-exploratory.json`

Actualmente algunas asignaciones departamentales se superponen.

Decida una de estas dos rutas:

1. convertirlo en partición exclusiva y corregir duplicados;
2. declararlo expresamente como regiones funcionales superpuestas.

No llamarlo división político-administrativa exclusiva si un departamento aparece en varias unidades.

Migre todos los escenarios al esquema V3.

---

# 12. Registro legal V3

Cada regla debe contener:

```ts
{
  id: string;
  figure: string;
  trigger: string;
  currentStatus: 'vigente' | 'transitorio' | 'hipotetico' | 'requiere-verificacion';
  normType: 'constitucion' | 'ley-organica' | 'ley-ordinaria' | 'decreto' | 'sentencia';
  reference: string;
  officialUrl: string;
  reviewedAt: string;
  conclusion: string;
  limitations: string[];
}
```

Fuentes oficiales mínimas:

- Constitución Política, arts. 1, 286–321, 325 y concordantes;
- Ley 1454 de 2011;
- Ley 1962 de 2019 y modificaciones vigentes;
- Decreto 1033 de 2021;
- Ley 1625 de 2013;
- Ley 2199 de 2022;
- Ley 2200 de 2022;
- Ley 136 de 1994 y modificaciones;
- Ley 1551 de 2012;
- Ley 1617 de 2013;
- Decreto Ley 1421 de 1993 y modificaciones;
- Decreto 1953 de 2014;
- jurisprudencia constitucional relevante.

Jurisprudencia mínima:

- C-540 de 2001;
- C-489 de 2012;
- C-035 de 2016;
- C-119 de 2020;
- C-447 de 2025;
- otras sentencias necesarias para la figura concreta.

Mostrar:

`Última revisión normativa: FECHA`

No afirmar vigencia futura sin revisión.

---

# 13. Fuentes de datos

No presentar SAVIA como plenamente operativo mientras estas fuentes estén vacías:

- población;
- desempeño fiscal;
- desempeño municipal;
- tipologías.

Implemente adaptadores o importación manual validada.

SECOP:

- no basta mostrar conteos nacionales de datasets;
- crear agregaciones territoriales reales;
- distinguir entidad contratante de lugar de ejecución;
- vigencia;
- cobertura.

SGR:

- documentar cobertura;
- asociar por código;
- separar valores, proyectos, ejecución física y financiera.

---

# 14. Interfaz

## 14.1 Asistente de escenario

Añada una barra de pasos visible en SEMILLAS.

## 14.2 Consecuencias

El panel derecho debe tener pestañas:

- Resumen;
- Gobierno;
- Competencias;
- Finanzas;
- Servicios;
- Representación;
- Transición;
- Ruta jurídica;
- Datos y límites.

## 14.3 Explicación contextual

Cada control debe tener:

- qué hace;
- qué no hace;
- requisitos;
- consecuencia inmediata;
- ejemplo.

## 14.4 Estado de operación

Después de cada operación mostrar:

- operación aplicada;
- unidades afectadas;
- resultado;
- advertencias;
- posibilidad de deshacer.

---

# 15. Accesibilidad

- toda selección cartográfica debe poder hacerse mediante lista;
- búsqueda;
- tabla;
- árbol;
- teclado;
- botones con estado;
- foco visible;
- mensajes `aria-live`;
- no depender del color;
- comparación textual;
- alternativa sin WebGL;
- operaciones destructivas con confirmación;
- deshacer disponible.

---

# 16. Pruebas

## 16.1 Contrato de botones

Cree una prueba que enumere todos los botones `data-*` del laboratorio y verifique que:

- no estén huérfanos;
- cambien estado o produzcan resultado;
- tengan prueba específica.

## 16.2 Selección

Probar:

- buscar departamento;
- buscar municipio no cargado;
- cargar departamento;
- seleccionar municipio;
- resaltar;
- seleccionar vecinos;
- seleccionar contiguos;
- rectángulo;
- polígono;
- invertir con universo visible;
- persistencia entre departamentos.

## 16.3 Capas

Probar cada checkbox.

## 16.4 RAÍCES

- función pública cambia;
- comparación funciona;
- ficha real.

## 16.5 SAVIA

- datos disponibles;
- datos faltantes;
- cobertura;
- pesos;
- sensibilidad;
- comparación.

## 16.6 SEMILLAS

- ejemplos;
- unión geométrica;
- división por grupos;
- división geométrica;
- nuevo nivel;
- supresión;
- gobierno;
- competencias por rol;
- financiación;
- planeación;
- consecuencias;
- ruta jurídica;
- importar/exportar;
- compartir;
- undo/redo.

## 16.7 Cartografía

- países vecinos;
- océano;
- costas;
- Colombia;
- islas;
- departamento;
- municipio;
- selección;
- escenario.

## 16.8 Legal

- figura vigente;
- esquema asociativo;
- subdivisión;
- reforma legal;
- reforma constitucional;
- Estado federado hipotético;
- no confundir área metropolitana con entidad territorial;
- no confundir comuna/localidad con municipio.

## 16.9 Capturas

- RAÍCES Colombia;
- RAÍCES municipio;
- SAVIA;
- SEMILLAS ejemplo Bogotá–Sabana;
- SEMILLAS federal hipotético;
- comparación;
- móvil;
- error sin WebGL.

---

# 17. Scripts y workflow

Añada:

- `npm run lab:functional-audit`;
- `npm run lab:legal-audit`;
- `npm run lab:button-contract`;
- `npm run lab:e2e`;
- `npm run validate`.

El workflow de despliegue debe ejecutar:

```text
npm run validate
npm run lab:e2e
```

No desplegar si falla una prueba E2E.

---

# 18. Criterios de terminación

No considere terminada la V3 hasta que:

1. todos los botones funcionen;
2. el buscador funcione;
3. las capas funcionen;
4. países y océanos sean visibles;
5. la selección municipal sea nacional y correcta;
6. vecinos y contiguos funcionen;
7. dibujo seleccione unidades;
8. exista selección visible;
9. existan ejemplos predeterminados;
10. SAVIA use datos o declare ausencia;
11. los escenarios base materialicen unidades;
12. unión genere geometría;
13. división genere unidades;
14. supresión produzca consecuencias;
15. crear nivel sea un editor;
16. competencias sean dinámicas y por rol;
17. gobierno tenga consecuencias;
18. financiación tenga consecuencias;
19. planeación tenga consecuencias;
20. exista jerarquía territorial;
21. existan subdivisiones municipales/distritales;
22. exista catálogo jurídico;
23. se distinga figura vigente de reforma constitucional;
24. exista comparación antes/después;
25. compartir escenario funcione;
26. escenarios antiguos estén migrados;
27. no exista esquema duplicado;
28. no exista `lab:e2e` duplicado;
29. todos los tests pasen;
30. `npm run validate` y `npm run lab:e2e` terminen con código 0.

---

# 19. Informe final

Entregue:

1. auditoría inicial;
2. botones corregidos;
3. botones eliminados;
4. arquitectura;
5. fuentes cartográficas;
6. selección territorial;
7. catálogo de figuras;
8. motor de consecuencias;
9. normativa y jurisprudencia;
10. ejemplos implementados;
11. datos conectados;
12. datos pendientes;
13. pruebas;
14. capturas;
15. tamaños;
16. advertencias;
17. limitaciones;
18. resultado exacto de comandos;
19. comandos para commit, push, solicitud de extracción y publicación.

No haga commit ni push.
