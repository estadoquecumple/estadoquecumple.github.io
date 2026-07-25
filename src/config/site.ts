export const SITE = {
  name: 'Estado que Cumple',
  alternateName: 'CAMS',
  author: 'Carlos Arturo Martínez Sánchez',
  description: 'Plataforma pública de propuestas, conocimiento y herramientas sobre capacidad estatal, administración pública y diseño institucional en Colombia.',
  language: 'es-CO',
  locale: 'es_CO',
  repository: 'https://github.com/estadoquecumple/estadoquecumple.github.io',
  socialImage: '/assets/og-cams-v3.png',
  socialImageWidth: 1200,
  socialImageHeight: 630,
  socialImageType: 'image/png',
  editorialIdentity: 'Identidad pública personal e independiente de Carlos Arturo Martínez Sánchez; no es una entidad jurídica ni un organismo público.',
  social: ['https://github.com/estadoquecumple/estadoquecumple.github.io','https://www.instagram.com/cams.carlosmartinez/','https://co.linkedin.com/in/cams0802','https://www.facebook.com/CAMS.CarlosMartinez/'],
} as const;

export type RouteRecord = { path:string; title:string; description:string; group:string; type:'WebPage'|'CollectionPage'|'ProfilePage'|'DigitalDocument'; editorialStatus:string; indexable:boolean; dateModified?:string };
const route = (path:string,title:string,description:string,group:string,type:RouteRecord['type']='WebPage',editorialStatus='Publicado',indexable=true,dateModified?:string):RouteRecord => ({path,title,description,group,type,editorialStatus,indexable,dateModified});
export const ROUTES: RouteRecord[] = [
  route('/', 'Estado que Cumple', SITE.description, 'General'),
  route('/cams/', 'CAMS', 'Identidad pública, agenda, capacidades, método y producción de Carlos Arturo Martínez Sánchez.', 'CAMS', 'ProfilePage'),
  route('/cams/trayectoria/', 'Trayectoria', 'Trayectoria pública verificable de Carlos Arturo Martínez Sánchez.', 'CAMS'),
  route('/cams/metodo/', 'Método CAMS', 'Método de investigación, formulación, contraste, publicación y corrección de CAMS.', 'CAMS'),
  route('/cams/criterios-y-transparencia/', 'Criterios y transparencia', 'Independencia, fuentes, correcciones, versiones, IA, privacidad y límites editoriales de CAMS.', 'CAMS'),
  ...[
    ['/estado-que-cumple/','Estado que Cumple','Propuesta ciudadana para cerrar la brecha entre forma institucional y capacidad pública real.'],
    ['/estado-que-cumple/problema/','El problema público','Diagnóstico de la brecha entre diseño institucional y capacidad pública real.'],
    ['/estado-que-cumple/fundamentos/','Fundamentos','Capacidad estatal, marco jurídico y antecedentes de Estado que Cumple.'],
    ['/estado-que-cumple/metodo/','Método','RAÍCES, SAVIA, SEMILLAS y expediente técnico integrado.'],
    ['/estado-que-cumple/arquitectura/','Arquitectura institucional','Arquitectura institucional propuesta para Estado que Cumple.'],
    ['/estado-que-cumple/activacion/','Rutas de activación','Rutas institucionales y ciudadanas para activar Estado que Cumple.'],
    ['/estado-que-cumple/implementacion/','Implementación','Transición, recursos, talento, datos, territorio, control y evaluación.'],
    ['/estado-que-cumple/aplicaciones/','Aplicaciones','Estándar para documentar aplicaciones reales de Estado que Cumple.'],
    ['/estado-que-cumple/documento/','Documento','Documento, ficha, descarga y autoría de Estado que Cumple.'],
  ].map(([path,title,description])=>route(path,title,description,'Estado que Cumple','WebPage','Propuesta no oficial')),
  route('/propuestas/','Propuestas','Catálogo real de iniciativas públicas formuladas por Carlos Arturo Martínez Sánchez y CAMS.','Conocimiento','CollectionPage'),
  route('/conocimiento/','Conocimiento','Centro orientador de investigaciones, documentos, Bitácora, Observatorio y Archivo de CAMS.','Conocimiento','CollectionPage'),
  route('/investigaciones/','Investigaciones','Estándar editorial de investigaciones CAMS; no hay estudios completos publicados.','Conocimiento','CollectionPage'),
  route('/documentos/','Documentos','Biblioteca de documentos efectivamente publicados por CAMS.','Conocimiento','CollectionPage'),
  route('/documentos/estado-que-cumple-2026-2030/','Estado que Cumple 2026–2030','Ficha documental, descarga, versión, autoría, citación e historial de Estado que Cumple.','Documentos','DigitalDocument','Publicado',true,'2026-06-06'),
  route('/bitacora/','Bitácora','Estado y agenda editorial de la Bitácora CAMS, sin artículos ficticios.','Conocimiento','CollectionPage'),
  route('/observatorio/','Observatorio de capacidad pública','Observatorio de capacidad pública y acceso al Laboratorio Territorial CAMS.','Observatorio','CollectionPage'),
  route('/observatorio/laboratorio-territorial/','Laboratorio Territorial CAMS','RAÍCES consulta el sistema vigente, SAVIA evalúa capacidad y SEMILLAS modela escenarios territoriales e institucionales.','Observatorio'),
  route('/archivo/','Archivo','Versiones del sitio y documentos, repositorio, cambios, correcciones y preservación.','Conocimiento','CollectionPage'),
  route('/participar/','Participar','Acciones reales para corregir, aportar fuentes, comentar y colaborar con CAMS.','Participación'),
  route('/participar/correcciones/','Corregir un error','Guía y plantilla pública para reportar errores verificables en CAMS.','Participación'),
  route('/participar/aportar-fuente/','Aportar una fuente','Guía y plantilla pública para aportar referencias verificables a CAMS.','Participación'),
  route('/participar/colaborar/','Colaborar','Alcance y plantilla pública para proponer colaboraciones concretas con CAMS.','Participación'),
  route('/accesibilidad/','Accesibilidad','Características, pruebas y canal de corrección de accesibilidad de CAMS.','Políticas'),
  route('/privacidad-y-datos/','Privacidad y datos','Tratamiento local, enlaces externos y límites de privacidad de un sitio CAMS estático.','Políticas'),
  route('/buscar/','Buscar','Buscador interno de páginas y contenidos publicados en CAMS.','General','WebPage','Funcional',false),
];
export const absoluteUrl=(path:string,site:URL)=>new URL(path,site).toString();
export const routeFor=(path:string)=>ROUTES.find((item)=>item.path===path);
