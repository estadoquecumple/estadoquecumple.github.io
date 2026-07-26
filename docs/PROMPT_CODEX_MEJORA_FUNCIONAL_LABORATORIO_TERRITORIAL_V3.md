# PROMPT OPERATIVO PARA CODEX
# MEJORA FUNCIONAL, VALIDACIÓN, FUSIÓN Y PUBLICACIÓN
# LABORATORIO TERRITORIAL V3
# SIN PULL REQUEST NI INTERFAZ WEB DE GITHUB

Trabaje en:

`C:\Users\Usuario\GitHub\estadoquecumple.github.io`

Puede modificar código, ejecutar pruebas, crear commits, fusionar localmente y hacer `git push origin main`.

No use pull request.
No use la interfaz web de GitHub.
No use `push --force`.
No use `reset --hard`.
No elimine ramas de respaldo.

---

# 0. Estado actual real

Antes de modificar cualquier archivo, verifique:

```powershell
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status
git log --oneline --decorate -8
git merge-base --is-ancestor f0f802e HEAD
$LASTEXITCODE
```

Estado esperado:

- `main` limpio y actualizado con `origin/main`;
- el commit V3 `f0f802e` ya está contenido en `main`;
- no existe cherry-pick pendiente;
- no existen conflictos activos;
- la antigua rama remota `laboratorio-territorial-v3-final` fue eliminada;
- la V3 ya está integrada en el código actual.

Si el código no cumple ese estado, deténgase e informe la diferencia exacta.  
No intente repetir el cherry-pick de la V3.

Cree una rama local nueva desde el `main` actualizado:

```powershell
git switch -c mejora-laboratorio-territorial-v3
```

No haga push todavía.

---

# 1. Propósito

Esta intervención no es una restauración ni una vuelta atrás.

Su objetivo es **mejorar la V3 actual para que el Laboratorio Territorial sea realmente funcional**.

Debe cerrar la cadena:

```text
selección territorial real
→ operación estructurada
→ geometría nueva o transformada
→ escenario institucional coherente
→ consecuencias diferenciadas
→ comparación antes/después
→ representación cartográfica
```

No amplíe nuevamente la cantidad de menús antes de corregir el funcionamiento central.

---

# 2. Auditoría inicial honesta

Antes de implementar, genere:

`reports/territorial-v3-improvement-initial.md`

Revise directamente:

- RAÍCES;
- SAVIA;
- SEMILLAS;
- mapa;
- búsqueda;
- selección;
- topología;
- escenarios;
- ejemplos;
- consecuencias;
- catálogo jurídico;
- importación/exportación;
- workflow.

Para cada control visible registre:

- selector;
- archivo;
- manejador;
- cambio de estado;
- efecto visible;
- efecto cartográfico;
- manejo de error;
- prueba Playwright real;
- clasificación:
  - funcional;
  - parcial;
  - nominal;
  - roto;
  - duplicado;
  - no disponible.

No certifique controles por:

- aparición textual;
- comentarios;
- existencia de un selector;
- mensajes `aria-live` sin cambio real;
- pruebas que no interactúan con el control.

La auditoría inicial no puede sobrescribirse al terminar.

---

# 3. Auditorías automáticas verificables

Reescriba:

- `tools/audit-territorial-v3-functional.mjs`;
- `tools/audit-territorial-v3-buttons.mjs`.

Reglas:

1. Los comentarios no cuentan como cobertura.
2. Un selector no equivale a una prueba.
3. Cada botón debe vincularse con una prueba Playwright ejecutada.
4. La prueba debe demostrar al menos uno:
   - mutación de estado;
   - cambio cartográfico;
   - cambio de escenario;
   - resultado visible;
   - error controlado.
5. La auditoría debe fallar ante:
   - controles huérfanos;
   - botones nominales;
   - ejemplos que solo cargan texto;
   - capas que no cambian;
   - operaciones sin efecto;
   - pruebas basadas solo en comentarios.

Genere:

- `reports/territorial-v3-controls-initial.json`;
- `reports/territorial-v3-controls-final.json`.

---

# 4. Seguridad

Elimine `innerHTML` cuando el contenido provenga de:

- escenarios importados;
- enlaces compartidos;
- nombres introducidos por el usuario;
- niveles;
- unidades;
- consecuencias;
- comparaciones;
- fuentes externas.

Use:

- `textContent`;
- `createElement`;
- fragmentos DOM seguros;
- sanitización estricta solo cuando sea imprescindible conservar formato.

Añada pruebas para:

- etiquetas `<script>`;
- atributos `onerror`;
- SVG malicioso;
- URLs `javascript:`;
- nombres con HTML;
- escenarios compartidos manipulados.

Proteja CSV contra fórmulas que comiencen por:

- `=`;
- `+`;
- `-`;
- `@`.

No muestre “contenido seguro” o “no se ejecutó contenido” sin una prueba específica.

---

# 5. Clasificación territorial DANE

Conserve y normalice el campo oficial equivalente a `MPIO_TIPO`.

Distinga como mínimo:

- municipio;
- distrito;
- Distrito Capital;
- área no municipalizada.

No denomine “municipios” indiscriminadamente a las 1.122 unidades del índice.

Actualice:

- índice nacional;
- GeoJSON;
- búsqueda;
- tabla;
- fichas;
- ejemplos;
- escenarios;
- topología;
- exportaciones;
- pruebas.

Genere un informe con los conteos exactos por tipo:

`reports/territorial-unit-types.json`

No invente la clasificación de una unidad cuando la fuente no la suministre.

---

# 6. Búsqueda y selección territorial

Implemente una máquina de selección coherente.

La búsqueda debe:

- mostrar lista de resultados;
- desambiguar nombres repetidos;
- mostrar tipo;
- mostrar departamento padre;
- buscar por código;
- cargar automáticamente la geometría;
- centrar;
- resaltar;
- actualizar ficha;
- conservar selección múltiple cuando corresponda.

La selección debe distinguir:

- primaria;
- múltiple;
- departamento;
- unidad local;
- candidata;
- unidad de escenario.

Corregir:

- selección departamental completa;
- invertir selección con universo explícito;
- persistencia entre departamentos;
- carga de más de un conjunto municipal;
- selección espacial nacional;
- vecinos;
- contiguos;
- resaltado;
- ficha.

---

# 7. Topología robusta

Reemplace la igualdad exacta de segmentos.

Implemente:

- reparación de geometrías;
- índice espacial;
- tolerancia documentada;
- `rook contiguity`;
- `queen contiguity`;
- frontera compartida;
- contacto puntual;
- solape;
- isla;
- discontinuidad.

Investigue la tasa de unidades con cero vecinos.

Genere:

`reports/territorial-topology-quality.json`

Debe incluir:

- total por tipo;
- vecinos promedio;
- unidades aisladas;
- contactos puntuales;
- solapes;
- geometrías inválidas;
- casos revisados.

Pruebe casos conocidos y falle ante resultados topológicamente anómalos.

---

# 8. Escenario representado en el mapa

Implemente un adaptador único:

```ts
scenarioToMapCollections(scenario)
```

Debe generar colecciones GeoJSON para:

- `scenario-created`;
- `scenario-transformed`;
- `scenario-suppressed`;
- `scenario-functional`;
- `scenario-units`;
- `candidate-units`;
- `selected-departments`;
- `selected-municipalities`.

Debe ejecutarse después de:

- crear;
- cargar;
- importar;
- cargar ejemplo;
- unir;
- dividir;
- transformar;
- suprimir;
- mover membresía;
- deshacer;
- rehacer.

Toda operación territorial debe producir un cambio visible en el mapa.

---

# 9. Operaciones territoriales reales

## 9.1 Unión

- disolver geometrías;
- conservar multipolígonos;
- detectar discontinuidad;
- crear unidad;
- crear membresías;
- conservar trazabilidad;
- representar antes/después.

## 9.2 División por grupos

- validar pertenencia;
- validar cobertura completa;
- impedir duplicados;
- crear geometrías;
- verificar continuidad;
- crear unidades;
- reasignar membresías;
- mostrar unidades no asignadas.

## 9.3 División geométrica

- validar corte;
- crear dos o más geometrías;
- impedir polígonos vacíos o inválidos;
- crear unidades nuevas;
- conservar padre como transformado;
- mostrar vista previa y confirmación.

## 9.4 Supresión departamental

No permitir confirmar hasta definir:

- unidades sustitutas;
- asignación total de unidades locales;
- ausencia de duplicados;
- ausencia de vacíos;
- gobierno;
- representación;
- competencias;
- financiación;
- planeación;
- control;
- transición.

Debe producir comparación antes/después.

## 9.5 Nuevo nivel

No concatene datos dentro de `nature`.

Modele campos separados:

- nombre;
- código;
- orden;
- naturaleza;
- cobertura;
- autoridad;
- forma de selección;
- corporación;
- competencias;
- financiación;
- planeación;
- control;
- relaciones.

## 9.6 Subdivisiones internas

Cree estructuras reales para:

- comuna;
- corregimiento;
- localidad;
- barrio;
- vereda;
- centro poblado;
- JAL;
- alcalde local;
- corregidor;
- fondo local.

Distinga unidad territorial, subdivisión, órgano e institución.

---

# 10. Ejemplos funcionales

Implemente completamente primero:

1. Bogotá–Sabana.
2. RAP Caribe → RET.
3. Colombia sin departamentos.

Cada ejemplo debe cargar:

- IDs reales;
- selección;
- geometría;
- jerarquía;
- figura;
- gobierno;
- competencias;
- financiación;
- mapa;
- consecuencias;
- ruta jurídica;
- comparación;
- supuestos;
- datos faltantes.

Los demás ejemplos deben:

- quedar deshabilitados;
- mostrar `No disponible todavía`;
- no crear un escenario vacío;
- no fingir resultados.

---

# 11. Motor de consecuencias

Reemplace cualquier cálculo basado únicamente en el resumen textual de la operación.

Implemente:

```ts
calculateScenarioDiff(before, operation, after, context)
```

Debe considerar:

- figura;
- unidad;
- autoridad;
- elección o nombramiento;
- representación;
- competencias;
- roles;
- financiación;
- planeación;
- control;
- continuidad;
- población;
- capacidad;
- ruta jurídica;
- transición;
- riesgos;
- datos faltantes.

Las consecuencias deben variar entre:

- RAP;
- RET;
- área metropolitana;
- región funcional;
- departamento;
- distrito;
- municipio;
- escenario federal hipotético;
- supresión departamental;
- administrador profesional.

No use expresiones regulares sobre una frase como motor jurídico.

---

# 12. Catálogo jurídico conectado

Conecte realmente:

- `figure-catalog`;
- `legal-registry`;
- `jurisprudence`;
- `legal-paths`;
- `consequence-rules`.

Corrija categorías:

- Nación no es entidad territorial del artículo 286;
- JAL es un órgano;
- resguardo indígena tiene naturaleza jurídica especial;
- figura legalmente habilitada no equivale a entidad efectivamente constituida;
- escenarios constitucionales deben marcarse como hipotéticos.

Para cada sentencia almacene:

- asunto;
- regla;
- alcance;
- operación relevante;
- límite;
- fuente;
- fecha de revisión.

La ruta jurídica debe derivarse de la operación real y la figura elegida.

---

# 13. SAVIA

Mientras falten datos:

- mostrar `No disponible`;
- no producir puntaje;
- no mostrar `calculated`;
- no recomendar por existir una selección.

Conecte primero:

- población;
- área;
- densidad;
- tipo territorial;
- cobertura;
- desempeño fiscal, cuando exista.

Los pesos deben modificar una fórmula real.

Mostrar:

- valor;
- peso;
- contribución;
- cobertura;
- sensibilidad;
- vigencia;
- fuente;
- dato faltante.

---

# 14. Workflow bloqueante

Modifique:

`.github/workflows/deploy.yml`

Antes del build y deploy debe ejecutarse:

```text
npm ci
npm run validate
npm run lab:e2e
```

El despliegue debe depender de ese job.

No publique si falla una prueba.

---

# 15. Pruebas obligatorias

Añada y ejecute pruebas para:

- controles reales;
- comentarios excluidos;
- búsqueda;
- desambiguación;
- clasificación territorial;
- topología;
- vecinos;
- contiguos;
- selección espacial;
- escenario → mapa;
- unión;
- división;
- supresión;
- nuevo nivel;
- subdivisiones;
- Bogotá–Sabana;
- RAP Caribe → RET;
- Colombia sin departamentos;
- consecuencias distintas;
- catálogo jurídico;
- SAVIA sin datos;
- SAVIA con datos de prueba;
- importación maliciosa;
- CSV seguro;
- escritorio;
- móvil;
- fallo cartográfico;
- alternativa tabular.

No elimine pruebas válidas.
No reduzca cobertura.
No deje omisiones injustificadas.

---

# 16. Validación y commit

Ejecute y corrija hasta código 0:

```powershell
npm install
npm run validate
npm run lab:e2e
git diff --check
```

Si `reports/seo-report.json` cambia únicamente en `generatedAt`, restaure ese archivo.

No agregue:

- `dist`;
- `node_modules`;
- `artifacts`;
- `playwright-report`;
- `test-results`;
- trazas;
- capturas temporales.

Genere:

`reports/territorial-v3-improvement-final.md`

Después:

```powershell
git status
git add -A
git commit -m "Mejorar funcionamiento integral del Laboratorio Territorial V3"
```

---

# 17. Integración local y publicación

Integre cambios recientes:

```powershell
git fetch origin --prune
git merge --no-ff origin/main -m "Integrar main antes de publicar mejoras del Laboratorio Territorial"
```

Resuelva conflictos combinando ambos lados. No use `ours` o `theirs` globalmente.

Repita:

```powershell
npm run validate
npm run lab:e2e
git diff --check
```

Solo con todo en verde:

```powershell
git switch main
git pull --ff-only origin main
git merge --no-ff mejora-laboratorio-territorial-v3 -m "Publicar mejoras funcionales del Laboratorio Territorial V3"

npm run validate
npm run lab:e2e
git diff --check
git status
git push origin main
```

No use pull request.
No use la interfaz web.
No use force push.

Si el push es rechazado, deténgase e informe el error exacto.

---

# 18. Informe final

Entregue:

- estado Git inicial;
- hash base;
- auditoría inicial;
- controles corregidos;
- clasificación territorial;
- topología;
- escenarios;
- ejemplos;
- operaciones;
- consecuencias;
- catálogo jurídico;
- SAVIA;
- seguridad;
- workflow;
- resultados exactos de pruebas;
- hashes de commits;
- hash publicado de `main`;
- URL pública;
- limitaciones reales;
- confirmación de que no se usó pull request ni force push.
