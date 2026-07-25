# CAMS v7 — Arquitectura, diseño y plan de migración

## 1. Decisión de producto

CAMS no debe diseñarse como una sola página larga, una hoja de vida, un blog ni un micrositio exclusivo de Estado que Cumple. Debe funcionar como una **plataforma pública personal de investigación, propuestas e incidencia**, con una propuesta principal destacada y espacio para crecer sin fragmentarse.

### Jerarquía de identidad

1. **Carlos Arturo Martínez Sánchez** — persona, autor y responsable público.
2. **CAMS** — identidad editorial, método de trabajo y archivo público.
3. **Estado que Cumple** — propuesta principal o insignia.
4. **Otras propuestas** — proyectos programáticos distintos.
5. **Investigaciones, documentos y análisis** — base de conocimiento que sustenta o cuestiona propuestas.
6. **Participación** — comentarios, colaboración, correcciones y seguimiento.

La interfaz debe comunicar siempre:

- Autor: Carlos Arturo Martínez Sánchez.
- Identidad editorial: CAMS.
- Propuesta principal: Estado que Cumple.
- Estado de cada contenido: investigación, borrador, propuesta pública, versión publicada o archivo.
- Carácter independiente y no oficial.

## 2. Arquitectura de navegación recomendada

### Navegación principal

- **Inicio**
- **CAMS**
- **Estado que Cumple**
- **Propuestas**
- **Conocimiento**
- **Participar**

La navegación no debe listar todas las páginas del sitio. Debe orientar por funciones.

### Menú secundario de “Conocimiento”

- Investigaciones
- Documentos
- Bitácora
- Observatorio
- Archivo y versiones

### Mapa de rutas

```text
/
├── /cams/
├── /estado-que-cumple/
│   ├── /problema/
│   ├── /metodo/
│   ├── /arquitectura/
│   ├── /implementacion/
│   ├── /aplicaciones/
│   └── /documento/
├── /propuestas/
│   └── /[slug]/
├── /conocimiento/
│   ├── /investigaciones/
│   │   └── /[slug]/
│   ├── /documentos/
│   ├── /bitacora/
│   │   └── /[slug]/
│   ├── /observatorio/
│   └── /archivo/
└── /participar/
```

Las rutas antiguas deben redirigir o mantenerse compatibles:

- `/documentos/`
- `/observatorio/`
- `/bitacora/`
- `/archivo/`

## 3. Función de cada página

### Inicio

La portada orienta. No contiene todo el sitio.

Orden recomendado:

1. Hero breve.
2. Tres caminos principales.
3. Estado que Cumple como proyecto insignia.
4. Trabajo reciente.
5. Agenda pública.
6. Método CAMS.
7. Perfil breve.
8. Participación.

Debe eliminar:

- selectores de audiencia antes de explicar el sitio;
- mapas que repitan el menú;
- varias colecciones de tarjetas con la misma función;
- cuatro o más CTA compitiendo en el hero;
- estados repetidos en cada bloque.

### CAMS

Debe responder:

- quién es Carlos Arturo Martínez Sánchez;
- qué es CAMS;
- qué experiencia pública y administrativa tiene;
- qué sabe hacer;
- qué temas investiga;
- cómo construye propuestas;
- cuál es su horizonte público;
- qué proyectos tiene activos;
- cómo verificar su producción.

Secciones:

1. Identificación pública.
2. Biografía ampliada.
3. Línea de tiempo.
4. Capacidades de trabajo.
5. Agenda pública.
6. Método CAMS.
7. Producción y proyectos.
8. Principios editoriales.
9. Redes y contacto.

### Estado que Cumple

La página principal debe ser un resumen guiado, no todo el documento.

Subpáginas:

- **Problema:** brecha forma-capacidad, causas, efectos y tipología.
- **Método:** RAÍCES, SAVIA, SEMILLAS, teoría de cambio.
- **Arquitectura:** sistema, comisión, secretaría, ventanilla, expediente y tablero.
- **Implementación:** rutas, competencias, instrumentos, riesgos y evaluación.
- **Aplicaciones:** casos sectoriales y territoriales.
- **Documento:** PDF, resumen, metadatos, citación, versiones y anexos.

Las herramientas interactivas deben vivir en la subpágina donde cumplen una función real.

### Propuestas

Debe ser un catálogo público estructurado.

Cada propuesta contiene:

- código;
- título;
- resumen;
- problema público;
- tesis o cambio propuesto;
- escala territorial;
- población o sector;
- evidencia disponible;
- alternativas consideradas;
- ruta institucional;
- instrumentos posibles;
- costos o condiciones;
- riesgos;
- estado de madurez;
- versión;
- fecha;
- documentos relacionados;
- próximos pasos.

Estados permitidos:

- idea registrada;
- investigación;
- borrador;
- propuesta pública;
- piloto;
- archivada.

Usar un solo indicador de estado por propuesta, no varios badges decorativos.

### Conocimiento

Es un centro de producción intelectual.

- **Investigaciones:** trabajos académicos, estudios de caso y análisis extensos.
- **Documentos:** biblioteca y descargas.
- **Bitácora:** artículos breves y series editoriales.
- **Observatorio:** seguimiento real cuando existan datos; mientras tanto, metodología y hoja de ruta.
- **Archivo:** versiones, licencias, repositorios y preservación.

### Participar

Debe ofrecer acciones reales:

- comentar una propuesta;
- señalar un error;
- aportar una fuente;
- proponer colaboración;
- seguir actualizaciones;
- revisar el repositorio;
- participar en discusiones públicas.

No mostrar formularios ficticios. Usar GitHub Discussions como primera capa abierta y trazable. Un formulario externo puede agregarse después para personas sin cuenta de GitHub.

## 4. Diseño visual

### Concepto

**Editorial institucional contemporáneo**, no imitación de un portal oficial.

La web debe sentirse como:

- archivo público;
- cuaderno de investigación;
- laboratorio de políticas;
- dossier institucional;
- plataforma personal seria.

### Roles visuales

- Rojo CAMS: tesis, propuesta, decisión.
- Azul institucional: evidencia, análisis, documentos.
- Dorado: autoría, metadatos, hitos y archivo.
- Verde sobrio: participación, implementación y resultados.
- Neutros cálidos: lectura y fondo.

### Tipos de composición

No usar tarjetas para todo.

Usar:

- dossier;
- línea de tiempo;
- mesa de trabajo;
- matriz de alternativas;
- cadena de evidencia;
- mapa de relaciones;
- ficha de propuesta;
- artículo editorial;
- panel de decisión;
- tabla de versiones;
- navegación por capítulos;
- índice lateral para páginas largas.

### Reglas

- máximo dos CTA principales por hero;
- ancho de lectura entre 60 y 75 caracteres;
- una jerarquía clara por página;
- tarjetas solo para colecciones intercambiables;
- no usar bordes y sombras por decoración;
- estados como metadatos, no como protagonistas;
- no esconder contenido esencial en tabs;
- diagramas deben tener alternativa textual;
- responsive funcional a 320 px y zoom 400 %.

## 5. Innovaciones prioritarias

No implementar todas a la vez.

### Primera ola

1. Buscador global por contenido y tipo.
2. Catálogo de propuestas con filtros.
3. Navegación por capítulos en Estado que Cumple.
4. Línea de tiempo pública de Carlos/CAMS.
5. Historial de versiones y citación.
6. GitHub Discussions para participación real.

### Segunda ola

1. Comparador de propuestas.
2. Grafo de evidencia.
3. Comparador de alternativas institucionales.
4. Ruta institucional pedagógica.
5. Lecturas relacionadas por etiquetas.
6. Lista de lectura guardada localmente.

### Tercera ola

1. Expediente técnico exportable.
2. Panel de seguimiento con datos reales.
3. Aplicaciones territoriales interactivas.
4. Visualizador geográfico.
5. API o base de datos, solo cuando exista necesidad real.

## 6. Arquitectura técnica recomendada

Migrar a **Astro con TypeScript**, manteniendo salida estática para GitHub Pages.

No usar React para todo. Emplear:

- componentes Astro para HTML;
- Markdown/MDX para contenido;
- TypeScript o JavaScript modular para herramientas;
- islas interactivas solo donde sean necesarias;
- GitHub Actions para compilar y desplegar.

### Estructura

```text
src/
├── components/
│   ├── global/
│   ├── navigation/
│   ├── content/
│   ├── proposals/
│   ├── profile/
│   └── interactive/
├── content/
│   ├── proposals/
│   ├── research/
│   └── articles/
├── data/
│   ├── profile.ts
│   ├── navigation.ts
│   └── topics.ts
├── layouts/
│   ├── BaseLayout.astro
│   ├── ContentLayout.astro
│   ├── ProposalLayout.astro
│   ├── ArticleLayout.astro
│   └── ToolLayout.astro
├── pages/
└── styles/
public/
├── assets/
├── documents/
└── icons/
```

### Colecciones

- `proposals`
- `research`
- `articles`

Cada colección debe tener validación de metadatos.

### Componentes esenciales

- Header
- Footer
- Breadcrumbs
- PageHero
- SectionNav
- InPageNavigation
- ProfileSummary
- PublicTimeline
- WorkMethod
- ProposalCard
- ProposalMeta
- ProposalComparison
- ResearchCard
- DocumentDownload
- VersionHistory
- RelatedContent
- ParticipationCTA
- StatusLabel
- EvidenceChain

## 7. Perfil público propuesto

### Encabezado

**Carlos Arturo Martínez Sánchez**

**Administración pública, capacidad estatal, participación y territorio**

### Resumen

Estudiante de 11.º semestre de Administración Pública en la Escuela Superior de Administración Pública —ESAP—, con experiencia en seguimiento institucional y contractual, gestión administrativa, participación ciudadana, representación juvenil, control social, producción documental y articulación con entidades públicas.

Entre 2022 y 2025 ejerció como consejero local de juventud de Teusaquillo, con funciones de presidencia, vicepresidencia y secretaría. Durante 2024 y 2025 fue consejero distrital y secretario del Consejo Distrital de Juventud de Bogotá. También trabajó en seguimiento técnico y administrativo de contratos en la Alcaldía Local de Teusaquillo.

Su trabajo actual se concentra en capacidad estatal, diseño institucional, política pública, función pública, territorio, infraestructura, participación juvenil y condiciones de implementación. Bajo la identidad editorial CAMS organiza investigaciones, documentos, herramientas y propuestas abiertas a discusión pública. Su propuesta principal es Estado que Cumple.

### Horizonte público

CAMS busca contribuir a una administración pública más capaz, democrática, territorial y orientada a resultados. Su propósito es conectar investigación, experiencia institucional, participación ciudadana y formulación programática para producir propuestas ejecutables, evaluables y abiertas al control público.

### Capacidades

- investigación documental y comparada;
- análisis institucional y jurídico-administrativo;
- definición de problemas públicos;
- teoría de cambio;
- diseño de alternativas;
- rutas institucionales y normativas;
- seguimiento contractual y administrativo;
- planeación territorial;
- sistematización cualitativa;
- matrices, bases de datos y visualización;
- escritura técnica y pedagogía pública.

## 8. Flujo de trabajo con VS Code Chat

Para evitar límites de tokens:

1. Guardar esta especificación como `docs/CAMS_V7_ARQUITECTURA.md`.
2. Crear `docs/CAMS_V7_ESTADO.md`.
3. Trabajar una fase por conversación.
4. En cada nueva conversación pedir:
   - leer ambos archivos;
   - ejecutar una sola fase;
   - actualizar el estado;
   - no hacer commit ni push;
   - responder con un resumen breve.
5. No volver a pegar la especificación completa.

---

# Prompts por fases

## PROMPT 0 — Auditoría y plan de migración

```text
Trabaja en modo agente sobre el repositorio abierto.

Lee por completo:
- docs/CAMS_V7_ARQUITECTURA.md
- todos los HTML actuales
- styles.css y assets/css/
- script.js y assets/js/
- assets/data/
- sitemap.xml
- README.md

No modifiques todavía la interfaz.

Crea docs/CAMS_V7_ESTADO.md con:
1. inventario real del proyecto;
2. mapa de páginas y funciones actuales;
3. contenidos que se conservarán;
4. contenidos que se moverán;
5. componentes que se reemplazarán;
6. rutas antiguas que deberán mantenerse;
7. riesgos de migración;
8. orden exacto de fases;
9. pruebas obligatorias;
10. lista de decisiones que no pueden inventarse.

Investiga solo documentación oficial vigente de Astro, GitHub Pages, W3C WCAG, GOV.UK Design System y USWDS. Guarda en el documento las decisiones técnicas derivadas, sin copiar textos extensos.

No hagas commit ni push.
No borres archivos.
Al terminar responde solamente con el archivo creado, riesgos principales y primera fase recomendada.
```

## PROMPT 1 — Inicializar Astro sin romper el sitio actual

```text
Lee:
- docs/CAMS_V7_ARQUITECTURA.md
- docs/CAMS_V7_ESTADO.md

Implementa únicamente la fase de infraestructura Astro.

Objetivos:
- inicializar Astro con TypeScript en el repositorio actual;
- mantener temporalmente los archivos HTML existentes;
- instalar solo Astro y @astrojs/sitemap;
- configurar salida estática;
- configurar la URL https://estadoquecumple.github.io;
- crear scripts npm: dev, build, preview y check;
- crear src/, public/ y una página mínima de prueba;
- copiar o mover assets de forma segura;
- crear el flujo oficial de GitHub Actions para Pages;
- no activar todavía el despliegue ni eliminar la web anterior.

Ejecuta npm run build.
Corrige errores.
Actualiza docs/CAMS_V7_ESTADO.md.

No hagas commit ni push.
No migres todavía el contenido.
Responde con archivos creados, comando de prueba y resultado del build.
```

## PROMPT 2 — Sistema base, layouts y navegación

```text
Lee la arquitectura y el estado de migración.

Implementa únicamente:
- BaseLayout.astro;
- ContentLayout.astro;
- Header;
- navegación principal;
- menú Conocimiento;
- navegación móvil;
- Breadcrumbs;
- Footer;
- metadatos SEO base;
- skip link;
- estilos base y tokens.

Navegación:
Inicio | CAMS | Estado que Cumple | Propuestas | Conocimiento | Participar

Conocimiento:
Investigaciones | Documentos | Bitácora | Observatorio | Archivo

No diseñes todavía las páginas finales.
No uses tarjetas genéricas para la navegación.
Mantén la identidad CAMS y evita cualquier apariencia de portal gubernamental oficial.

Prueba:
- teclado;
- Escape;
- 320 px;
- zoom 200 %;
- npm run build.

Actualiza docs/CAMS_V7_ESTADO.md.
No hagas commit ni push.
```

## PROMPT 3 — Nueva portada

```text
Lee la especificación y el estado.

Construye la nueva portada solamente.

Orden:
1. hero breve con máximo dos CTA principales;
2. tres caminos: conocer CAMS, explorar Estado que Cumple, ver propuestas y conocimiento;
3. Estado que Cumple como proyecto insignia;
4. trabajo reciente alimentado por colecciones;
5. agenda pública;
6. método CAMS;
7. perfil breve;
8. participación.

Elimina del nuevo diseño:
- selector de audiencia en el inicio;
- mapa que duplica el menú;
- múltiples bloques de tarjetas equivalentes;
- estados repetidos;
- CTA redundantes.

La portada debe ser editorial, asimétrica, accesible y responsive.
No inventes publicaciones.
Usa contenido real migrado o una ausencia honesta.

Ejecuta build y actualiza el estado.
No hagas commit ni push.
```

## PROMPT 4 — Página CAMS y perfil público

```text
Lee docs/CAMS_V7_ARQUITECTURA.md y docs/CAMS_V7_ESTADO.md.

Construye /cams/ como página pública de Carlos Arturo Martínez Sánchez y de la identidad editorial CAMS.

Incluye:
- identificación;
- biografía ampliada;
- relación Carlos → CAMS → Estado que Cumple;
- trayectoria en línea de tiempo;
- capacidades de trabajo;
- agenda pública;
- método CAMS;
- horizonte público;
- producción actual;
- principios editoriales;
- redes confirmadas.

Usa el perfil aprobado en la especificación.
No publiques teléfono, dirección, identificación ni datos sensibles.
No inventes títulos, cargos, fechas, afiliaciones o candidaturas.
No conviertas la página en una hoja de vida extensa.
La declaración de independencia debe ocupar menos espacio que la trayectoria y el propósito.

Añade JSON-LD Person.
Ejecuta build y pruebas responsive.
Actualiza el estado.
No hagas commit ni push.
```

## PROMPT 5 — Colección de propuestas

```text
Implementa la colección Astro `proposals`.

Crea:
- esquema tipado;
- índice /propuestas/;
- ruta dinámica /propuestas/[slug]/;
- ProposalLayout;
- filtros por tema, escala y estado;
- metadatos de versión;
- contenido relacionado;
- citación;
- navegación anterior/siguiente.

Campos obligatorios:
code, title, summary, problem, thesis, status, version, datePublished,
dateModified, scale, topics, instruments, risks, evidence, relatedDocuments.

Estado que Cumple debe aparecer como propuesta insignia, pero su micrositio conserva ruta propia.

No inventes otras propuestas completas. Migra únicamente propuestas con contenido real y deja la arquitectura lista para añadir nuevas mediante Markdown.

Añade JSON-LD CreativeWork.
Ejecuta build y actualiza el estado.
No hagas commit ni push.
```

## PROMPT 6 — Micrositio Estado que Cumple

```text
Migra Estado que Cumple a la nueva arquitectura.

Crear:
- /estado-que-cumple/
- /estado-que-cumple/problema/
- /estado-que-cumple/metodo/
- /estado-que-cumple/arquitectura/
- /estado-que-cumple/implementacion/
- /estado-que-cumple/aplicaciones/
- /estado-que-cumple/documento/

La portada del micrositio debe ofrecer un recorrido guiado y un resumen.
Cada subpágina debe resolver una función principal.
No usar tabs como navegación entre páginas.
Usar navegación de capítulo y anterior/siguiente.

Reubicar:
- árbol del problema en Problema;
- núcleo RAÍCES/SAVIA/SEMILLAS en Método;
- mapa institucional en Arquitectura;
- simulador y expediente en Implementación;
- casos en Aplicaciones;
- PDF, versiones y citación en Documento.

Mantener alternativa textual y funcionamiento sin JavaScript.
Ejecutar build, probar anchors y actualizar el estado.
No hacer commit ni push.
```

## PROMPT 7 — Centro de conocimiento

```text
Construye /conocimiento/ y migra las áreas internas.

Crear:
- /conocimiento/investigaciones/
- /conocimiento/documentos/
- /conocimiento/bitacora/
- /conocimiento/observatorio/
- /conocimiento/archivo/

Mantener compatibilidad con rutas anteriores mediante páginas de redirección estática o enlaces canónicos.

Crear colecciones:
- research;
- articles.

Diferenciar:
- propuesta;
- investigación;
- documento;
- artículo;
- dato o indicador;
- archivo.

El Observatorio no debe fingir resultados. Si no existen datos, mostrar metodología, fuentes y hoja de ruta de forma compacta.

La Bitácora no debe presentar borradores como publicaciones.
La biblioteca debe mostrar versión, fecha, autor, estado, resumen, palabras clave y citación.

Ejecuta build y actualiza el estado.
No hagas commit ni push.
```

## PROMPT 8 — Participación real

```text
Rediseña /participar/.

Objetivo:
ofrecer acciones reales y trazables, no módulos decorativos.

Implementa:
- enlace a GitHub Discussions;
- categorías sugeridas: comentarios, fuentes, propuestas, preguntas y anuncios;
- enlace para reportar errores;
- guía para contribuir;
- código de conducta breve;
- política de privacidad y publicación;
- canales públicos confirmados.

No incrustes giscus hasta verificar que Discussions está habilitado y que existen repository-id y category-id válidos.
Si faltan, muestra una acción real que abra Discussions.

No recopiles datos personales localmente.
No inventes suscripción por correo.

Ejecuta build y actualiza el estado.
No hagas commit ni push.
```

## PROMPT 9 — Innovaciones de primera ola

```text
Implementa únicamente estas innovaciones:

1. buscador global por páginas, propuestas, investigaciones y artículos;
2. historial de versiones;
3. contenido relacionado por etiquetas;
4. comparador básico de dos propuestas;
5. lista de lectura guardada en localStorage.

No agregar animaciones decorativas.
No cargar JavaScript en páginas que no usan una herramienta.
Mantener progresive enhancement.

Prueba teclado, touch, 320 px y zoom 200 %.
Ejecuta build y actualiza el estado.
No hagas commit ni push.
```

## PROMPT 10 — SEO, accesibilidad, rendimiento y cierre

```text
Realiza auditoría final.

Revisar:
- titles y descriptions;
- canonical;
- Open Graph;
- sitemap;
- robots;
- JSON-LD Person, CreativeWork y Article;
- un h1 por página;
- jerarquía de headings;
- navegación por teclado;
- focus visible;
- reflow a 320 px;
- zoom 200 % y 400 %;
- contraste;
- prefers-reduced-motion;
- imágenes optimizadas;
- enlaces rotos;
- rutas antiguas;
- PDF y descargas;
- tamaño de JavaScript;
- carga diferida;
- 404 personalizada.

Ejecutar:
- npm run build;
- npm run check;
- auditorías existentes adaptadas a dist/;
- git diff --check.

Eliminar archivos antiguos solo si:
- el contenido ya fue migrado;
- las rutas funcionan;
- el build es correcto;
- docs/CAMS_V7_ESTADO.md registra el cambio.

No hacer commit ni push.
Entregar lista final de pruebas, problemas pendientes y comando exacto de publicación.
```

## 9. Comandos de validación

```powershell
node -v
npm -v
npm run dev
npm run build
npm run preview
npm run check
git status
git diff --stat
git diff --check
```

## 10. Regla final

Cada página debe tener una función principal.  
Cada interacción debe ayudar a comprender, comparar, decidir, documentar o participar.  
Cada contenido debe declarar autor, estado, versión y relación con el resto del archivo.  
CAMS debe mostrar a la persona, el método y la agenda; Estado que Cumple debe ser la propuesta principal, no la totalidad de la identidad.
