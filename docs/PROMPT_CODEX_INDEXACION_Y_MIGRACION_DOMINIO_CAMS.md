# PROMPT MAESTRO PARA CODEX
# INDEXACIÓN, SEO TÉCNICO Y MIGRACIÓN FUTURA DE DOMINIO
# ESTADO QUE CUMPLE / CAMS

Trabaje sobre el repositorio Astro actual de la organización `estadoquecumple`, sin cambiar rutas públicas ni publicar directamente.

## Objetivo

Deje el sitio `https://estadoquecumple.github.io/` técnicamente preparado para:

1. indexación inmediata en Google y Bing;
2. lectura correcta por rastreadores y sistemas de búsqueda;
3. consolidación de la identidad:
   - Estado que Cumple;
   - CAMS;
   - Carlos Arturo Martínez Sánchez;
4. migración futura, con el menor cambio posible, a uno de estos dominios:
   - `https://estadoquecumple.co/`
   - `https://estadoquecumple.com.co/`

No configure como canónico un dominio que todavía no existe o no está conectado. El dominio canónico actual debe seguir siendo `https://estadoquecumple.github.io`.

No haga `git commit`, `git merge` ni `git push`.

---

## 1. Auditoría inicial obligatoria

Antes de editar:

- inspeccione `astro.config.mjs`;
- inspeccione `package.json`;
- inspeccione `src/layouts/BaseLayout.astro`;
- inspeccione el componente SEO actual;
- inspeccione JSON-LD;
- inspeccione `robots.txt`;
- inspeccione la integración de sitemap;
- inspeccione `llms.txt`;
- inspeccione `site-index.json`;
- inspeccione el buscador;
- inspeccione todas las rutas en `src/pages`;
- inspeccione el workflow de GitHub Pages;
- ejecute `npm run validate`;
- compile y revise `dist/`.

Busque referencias a:

- `camscarlosmartinez.github.io`;
- `estadoquecumple.github.io`;
- dominios futuros;
- canonical;
- `og:url`;
- `robots`;
- `noindex`;
- sitemap;
- datos estructurados.

Informe primero qué está correcto, qué falta y qué está duplicado. Después implemente todo sin pedir aprobaciones intermedias.

---

## 2. Fuente única de URL pública

Centralice la URL del sitio.

En `astro.config.mjs`, use una fuente equivalente a:

```js
const siteUrl =
  process.env.SITE_URL ??
  'https://estadoquecumple.github.io';
```

Configure:

```js
site: siteUrl
```

No use `base`, porque este es el sitio raíz de la organización.

Cree una configuración compartida, por ejemplo:

`src/config/site.ts`

Debe contener:

- nombre principal: `Estado que Cumple`;
- nombre alternativo: `CAMS`;
- autor: `Carlos Arturo Martínez Sánchez`;
- descripción principal;
- idioma `es-CO`;
- locale `es_CO`;
- URL del repositorio;
- rutas sociales confirmadas;
- imagen social;
- identidad editorial;
- fecha de actualización solo cuando sea real.

Todas las URLs públicas absolutas deben derivarse de `Astro.site` o de esta configuración. Evite repetir el host en componentes.

Al final, debe ser posible migrar a dominio propio cambiando únicamente:

- `SITE_URL`;
- configuración de GitHub Pages;
- DNS;
- Search Console/Bing;
- documentación puntual.

---

## 3. Canonicalización

Cada página indexable debe tener:

- canonical absoluta y autorreferente;
- una sola etiqueta canonical;
- `og:url` igual a la canonical;
- título único;
- descripción única;
- idioma `es-CO`;
- estado indexable explícito o implícito.

No use el futuro dominio todavía.

Excluya de indexación páginas que no aporten valor independiente, por ejemplo:

- resultados internos de búsqueda;
- páginas técnicas;
- borradores;
- rutas de prueba;
- páginas duplicadas.

Use `noindex, follow` solo cuando esté justificado.

No aplique `noindex` a:

- portada;
- CAMS;
- Estado que Cumple;
- propuestas;
- investigaciones publicadas;
- documentos publicados;
- Observatorio;
- Laboratorio Territorial;
- Archivo;
- Participar;
- metodología sustantiva.

---

## 4. Sitemap

Use la integración oficial de Astro para sitemap.

El sitemap debe:

- contener solo URLs canónicas;
- excluir `noindex`;
- excluir 404;
- excluir buscador interno;
- excluir páginas de prueba;
- usar el host actual;
- incluir `lastmod` solo cuando sea real y trazable;
- no inventar fechas;
- reflejar todas las rutas publicadas.

Confirme la salida real:

- `sitemap-index.xml`;
- archivos sitemap secundarios, si los genera Astro.

Actualice la auditoría para comprobar:

- que todas las URLs del sitemap existen;
- que todas usan el host canónico;
- que no aparecen dominios antiguos;
- que no aparecen dominios futuros;
- que no aparecen rutas excluidas.

---

## 5. robots.txt

Genere `robots.txt` desde la URL central o mantenga un archivo estático correctamente construido.

Debe contener:

```txt
User-agent: *
Allow: /

Sitemap: https://estadoquecumple.github.io/sitemap-index.xml
```

Si el nombre real del sitemap difiere, use la ruta real.

No bloquee:

- CSS;
- JavaScript;
- imágenes;
- PDF;
- JSON público necesario;
- mapas;
- metodología.

No use reglas específicas para bloquear rastreadores de IA salvo decisión editorial expresa del autor.

---

## 6. Datos estructurados

Implemente JSON-LD prudente y válido.

### Portada

Use:

- `WebSite`;
- `Person`;
- `CreativeWork` o `CollectionPage` cuando corresponda.

Identidad:

```text
Estado que Cumple
alternateName: CAMS
author: Carlos Arturo Martínez Sánchez
```

No presente CAMS como una entidad jurídica ni como organismo público.

### Página CAMS

Use `Person` con:

- nombre completo;
- alternateName `CAMS`;
- URL de perfil;
- `sameAs` únicamente para perfiles confirmados;
- formación o cargos solo cuando estén sustentados.

### Estado que Cumple

Use `CreativeWork`:

- nombre;
- autor;
- descripción;
- fecha/versiones reales;
- estado de propuesta no oficial;
- URL del documento.

### Documentos

Use `DigitalDocument` o `CreativeWork`.

### Bitácora

Use `Article` únicamente cuando exista un artículo real.

### Laboratorio Territorial

Use `Dataset`, `SoftwareApplication` o `WebApplication` solo si los campos están completos y son verdaderos. No invente cobertura, licencia o fecha.

Valide los bloques JSON-LD y evite entidades duplicadas con IDs diferentes.

---

## 7. Identidad y búsquedas de marca

La portada y metadatos deben permitir asociar:

- Estado que Cumple;
- CAMS;
- Carlos Arturo Martínez Sánchez;
- Estado que Cumple Colombia;
- Laboratorio Territorial CAMS;
- capacidad estatal;
- administración pública;
- diseño institucional.

No haga `keyword stuffing`.

Asegure que el contenido HTML visible explique:

```text
Estado que Cumple es una plataforma pública desarrollada
por Carlos Arturo Martínez Sánchez bajo la identidad CAMS.
```

La página `/cams/` debe enlazarse desde:

- encabezado;
- pie;
- autoría de documentos;
- Estado que Cumple;
- páginas de metodología.

La página de Estado que Cumple debe enlazar al autor y al documento.

---

## 8. Open Graph, imágenes y redes

Cada página debe tener:

- `og:title`;
- `og:description`;
- `og:type`;
- `og:url`;
- `og:image` absoluta;
- `og:locale=es_CO`;
- Twitter Card.

Verifique que la imagen social:

- exista;
- tenga dimensiones apropiadas;
- sea pública;
- no dependa de JavaScript;
- use branding CAMS;
- no contenga texto ilegible.

Añada ancho, alto y tipo cuando sea posible.

---

## 9. Contenido rastreable

El contenido sustantivo debe estar en HTML generado por Astro.

No deje dentro de JavaScript únicamente:

- títulos;
- explicaciones;
- fuentes;
- metodología;
- resultados esenciales;
- advertencias.

Las herramientas interactivas deben tener:

- texto introductorio;
- tabla alternativa;
- enlaces rastreables;
- estados sin JavaScript;
- fuente y fecha visibles.

Evite botones sin enlaces para navegación sustantiva.

---

## 10. Enlaces internos

Construya una malla interna coherente.

La portada debe enlazar a:

- CAMS;
- Estado que Cumple;
- Propuestas;
- Conocimiento;
- Observatorio;
- Laboratorio Territorial;
- documentos principales.

Cada capítulo de Estado que Cumple debe enlazar a:

- capítulo anterior;
- siguiente;
- portada del micrositio;
- documento;
- autor;
- laboratorio cuando sea pertinente.

Documentos, investigaciones y Bitácora deben tener contenidos relacionados.

Evite páginas huérfanas.

---

## 11. Verificación de Google Search Console

Prepare el repositorio para verificación por archivo HTML.

El archivo que Google entregue se colocará en:

`public/googleXXXXXXXXXXXX.html`

No invente el nombre ni el contenido. Documente el procedimiento en:

`docs/INDEXACION.md`

Incluya:

1. agregar propiedad de prefijo de URL:
   `https://estadoquecumple.github.io/`;
2. descargar archivo HTML;
3. copiarlo a `public/`;
4. compilar;
5. publicar;
6. comprobar que abre en la raíz;
7. verificar;
8. enviar sitemap;
9. solicitar indexación de páginas prioritarias.

No incluya tokens ficticios.

---

## 12. Bing Webmaster Tools e IndexNow

Documente que Bing puede importar la propiedad verificada desde Google Search Console.

Implemente IndexNow de manera preparada para cambio de dominio:

- host derivado de `SITE_URL`;
- clave suministrada mediante secreto o variable;
- archivo de clave generado en `public/` solo cuando exista clave real;
- no codificar claves inventadas;
- script que lea URLs canónicas del sitemap;
- máximo razonable de URLs;
- no enviar rutas `noindex`;
- workflow manual tras despliegue;
- no bloquear el build si IndexNow falla.

Cree comandos equivalentes:

- `npm run indexnow:prepare`;
- `npm run indexnow:submit`.

No active envíos con una clave ficticia.

---

## 13. site-index.json y llms.txt

Mantenga estos archivos como ayudas complementarias, pero no como sustitutos de:

- sitemap;
- robots;
- canonical;
- enlaces;
- datos estructurados.

`site-index.json` debe generarse desde la misma fuente de rutas y contener:

- título;
- URL canónica;
- descripción;
- grupo;
- tipo;
- fecha real, cuando exista;
- autor;
- estado editorial.

`llms.txt` debe:

- describir identidad;
- ofrecer rutas canónicas;
- enlazar documentos y metodología;
- señalar el dominio canónico actual;
- indicar que el sitio migrará en el futuro solo cuando el dominio nuevo sea real;
- no inventar estándares ni garantías de indexación.

---

## 14. Página de política editorial y correcciones

Asegure páginas rastreables para:

- criterios y transparencia;
- correcciones;
- privacidad y datos;
- accesibilidad;
- metodología;
- archivo/versiones.

Estas páginas mejoran la comprensión y confianza, pero no deben contener afirmaciones legales no sustentadas.

---

## 15. Preparación para dominio propio

Documente dos alternativas futuras:

- `estadoquecumple.co`;
- `estadoquecumple.com.co`.

No elija una ni la configure todavía.

Cree en `docs/MIGRACION_DOMINIO.md` una lista exacta:

1. registrar dominio;
2. decidir dominio canónico;
3. si se compran ambos, uno debe redirigir al otro;
4. verificar dominio en la organización GitHub;
5. configurar GitHub Pages;
6. configurar DNS;
7. cambiar `SITE_URL`;
8. actualizar canonical, sitemap, robots, Open Graph y JSON-LD desde la fuente central;
9. mantener exactamente las mismas rutas;
10. verificar propiedad nueva en Search Console;
11. verificar propiedad antigua;
12. comprobar redirecciones de cada URL antigua a su equivalente;
13. usar Cambio de dirección de Search Console si la propiedad es elegible;
14. enviar sitemap nuevo;
15. mantener redirecciones al menos 180 días;
16. conservar la propiedad antigua para monitoreo;
17. actualizar Bing e IndexNow;
18. no rediseñar estructura y dominio simultáneamente.

Incluya comandos de comprobación:

```powershell
Invoke-WebRequest -Method Head https://estadoquecumple.github.io/
Invoke-WebRequest -Method Head https://DOMINIO-NUEVO/
```

Y una tabla de correspondencia de URLs.

---

## 16. Auditoría

Amplíe `npm run audit` y `npm run validate`.

Debe fallar si:

- falta canonical;
- hay más de una canonical;
- una canonical usa un host incorrecto;
- falta título o descripción;
- `og:url` no coincide;
- una URL indexable no aparece en sitemap;
- una URL `noindex` aparece en sitemap;
- sitemap usa un dominio distinto;
- robots no enlaza al sitemap;
- aparecen referencias a `camscarlosmartinez.github.io`;
- aparece prematuramente `estadoquecumple.co` o `.com.co` como canonical;
- hay JSON-LD inválido;
- hay páginas huérfanas;
- existen enlaces internos rotos;
- existen imágenes sociales inexistentes;
- una página principal tiene menos contenido HTML del esperado;
- la ruta de verificación de Google no se conserva al compilar;
- la salida contiene `localhost`.

Cree:

- `npm run seo:audit`;
- `npm run seo:report`;
- integre SEO en `npm run validate`.

Genere un informe legible en:

`reports/seo-report.json`

y un resumen en consola.

---

## 17. README y documentación

Actualice README con:

- URL pública;
- identidad;
- instalación;
- build;
- validación;
- SEO;
- Search Console;
- Bing;
- IndexNow;
- migración futura;
- cómo cambiar el dominio sin editar muchos archivos.

Cree:

- `docs/INDEXACION.md`;
- `docs/MIGRACION_DOMINIO.md`;
- `docs/SEO_CHECKLIST.md`.

---

## 18. Validación final

Ejecute:

```text
npm run check
npm run build
npm run audit
npm run seo:audit
npm run validate
```

Compruebe en `dist/`:

- portada;
- canonical;
- sitemap;
- robots;
- JSON-LD;
- imágenes sociales;
- site-index;
- llms;
- buscador;
- rutas prioritarias.

No haga commit ni push.

---

## 19. Informe final

Entregue:

1. diagnóstico inicial;
2. archivos modificados;
3. archivos creados;
4. URL canónica;
5. número de páginas indexables;
6. páginas noindex y justificación;
7. sitemap generado;
8. resultados de robots;
9. resultados de JSON-LD;
10. estado de Search Console;
11. estado de Bing/IndexNow;
12. preparación para dominio propio;
13. resultado exacto de todos los comandos;
14. pasos manuales que debe hacer el usuario;
15. comandos para commit, push y publicación.
