export type FigureCategory = 'entidad-territorial'|'entidad-administrativa'|'esquema-asociativo'|'subdivision-interna'|'division-estadistica'|'unidad-comunitaria'|'escenario-constitucional';
export type Figure = { id:string; name:string; category:FigureCategory; status:'vigente'|'transitorio'|'hipotetico'; warning?:string };
const current = (id:string,name:string,category:FigureCategory):Figure => ({id,name,category,status:'vigente'});
const constitutionalWarning = 'Escenario de rediseño constitucional. No corresponde a una figura vigente del ordenamiento colombiano.';
export const figureCatalog: Figure[] = [
  current('nation','Nación','entidad-territorial'), current('department','Departamento','entidad-territorial'),
  current('municipality','Municipio','entidad-territorial'), current('district','Distrito','entidad-territorial'),
  {id:'indigenous-territory',name:'Territorio indígena y régimen transitorio aplicable',category:'entidad-territorial',status:'transitorio'},
  current('rap','Región administrativa y de planificación — RAP','entidad-administrativa'),
  current('ret','Región entidad territorial — RET','entidad-territorial'),
  current('rpg','Región de planeación y gestión','entidad-administrativa'),
  current('department-association','Asociación de departamentos','esquema-asociativo'),
  current('municipality-association','Asociación de municipios','esquema-asociativo'),
  current('district-association','Asociación de distritos','esquema-asociativo'),
  current('pap','Provincia administrativa y de planificación — PAP','entidad-administrativa'),
  current('metropolitan-area','Área metropolitana','entidad-administrativa'),
  current('rm-bogota','Región Metropolitana Bogotá–Cundinamarca','entidad-administrativa'),
  current('commune','Comuna','subdivision-interna'), current('corregimiento','Corregimiento','subdivision-interna'),
  current('district-locality','Localidad distrital','subdivision-interna'), current('bogota-locality','Localidad de Bogotá','subdivision-interna'),
  current('jal','Junta Administradora Local','unidad-comunitaria'), current('neighborhood','Barrio','unidad-comunitaria'),
  current('vereda','Vereda','unidad-comunitaria'), current('population-center','Centro poblado','division-estadistica'),
  current('resguardo','Resguardo indígena','unidad-comunitaria'), current('functional-custom','Unidad personalizada funcional','entidad-administrativa'),
  ...['Estado federado','Provincia como entidad territorial plena','Supresión general de departamentos','Sustitución de alcaldes o gobernadores elegidos','Legislaturas territoriales','Soberanía fiscal subnacional','Municipios convertidos en comunas sin autonomía','Regiones con potestad legislativa']
    .map((name,index):Figure=>({id:`constitutional-${index+1}`,name,category:'escenario-constitucional',status:'hipotetico',warning:constitutionalWarning})),
];

