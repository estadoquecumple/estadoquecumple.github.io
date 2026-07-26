export type LegalRule = {
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
};

const senate = 'https://www.secretariasenado.gov.co/senado/basedoc/';
const court = 'https://www.corteconstitucional.gov.co/relatoria/';
const reviewedAt = '2026-07-25';
export const legalRegistry: LegalRule[] = [
  { id:'constitution-unitary', figure:'organización territorial', trigger:'crear, transformar o suprimir entidad territorial', currentStatus:'vigente', normType:'constitucion', reference:'Constitución Política, arts. 1, 286–321 y 325', officialUrl:`${senate}constitucion_politica_1991.html`, reviewedAt, conclusion:'Colombia es una república unitaria con autonomía de sus entidades territoriales dentro de la Constitución y la ley.', limitations:['La ruta depende de la naturaleza exacta de la operación.'] },
  { id:'lot-1454', figure:'esquemas asociativos territoriales', trigger:'asociación y ordenamiento territorial', currentStatus:'vigente', normType:'ley-organica', reference:'Ley 1454 de 2011', officialUrl:`${senate}ley_1454_2011.html`, reviewedAt, conclusion:'Regula instrumentos de ordenamiento y esquemas asociativos; no convierte por sí sola una asociación en entidad territorial.', limitations:['Revisar modificaciones y reglamentación aplicable al caso.'] },
  { id:'regions-1962', figure:'RAP y RET', trigger:'crear RAP o tramitar conversión a RET', currentStatus:'vigente', normType:'ley-organica', reference:'Ley 1962 de 2019', officialUrl:`${senate}ley_1962_2019.html`, reviewedAt, conclusion:'Distingue la región administrativa y de planificación de la región entidad territorial y establece condiciones de conversión.', limitations:['La aplicación exige verificar requisitos, decisiones territoriales y modificaciones vigentes.'] },
  { id:'regions-decree', figure:'RET', trigger:'desarrollar conversión regional', currentStatus:'vigente', normType:'decreto', reference:'Decreto 1033 de 2021', officialUrl:'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=167350', reviewedAt, conclusion:'Reglamenta aspectos del procedimiento regional.', limitations:['Verificar actos y requisitos particulares.'] },
  { id:'metro-1625', figure:'área metropolitana', trigger:'crear o modificar área metropolitana', currentStatus:'vigente', normType:'ley-ordinaria', reference:'Ley 1625 de 2013', officialUrl:`${senate}ley_1625_2013.html`, reviewedAt, conclusion:'El área metropolitana es una entidad administrativa, no una entidad territorial.', limitations:['No aplica a la Región Metropolitana Bogotá–Cundinamarca.'] },
  { id:'rm-bogota-2199', figure:'Región Metropolitana Bogotá–Cundinamarca', trigger:'asociar Bogotá y entidades de Cundinamarca', currentStatus:'vigente', normType:'ley-organica', reference:'Ley 2199 de 2022', officialUrl:`${senate}ley_2199_2022.html`, reviewedAt, conclusion:'Establece un régimen especial de coordinación metropolitana que conserva la autonomía de integrantes.', limitations:['La vinculación y los hechos metropolitanos requieren actos concretos.'] },
  { id:'departments-2200', figure:'departamento', trigger:'modificar régimen departamental', currentStatus:'vigente', normType:'ley-ordinaria', reference:'Ley 2200 de 2022', officialUrl:`${senate}ley_2200_2022.html`, reviewedAt, conclusion:'Regula la organización y funcionamiento departamental.', limitations:['No autoriza la supresión general del nivel departamental.'] },
  { id:'municipal-136', figure:'municipio, comuna y corregimiento', trigger:'organización municipal interna', currentStatus:'vigente', normType:'ley-ordinaria', reference:'Ley 136 de 1994 y Ley 1551 de 2012', officialUrl:`${senate}ley_0136_1994.html`, reviewedAt, conclusion:'Regula municipios y sus divisiones administrativas internas; comunas y corregimientos no son municipios.', limitations:['Revisar acuerdos municipales y régimen especial cuando corresponda.'] },
  { id:'district-1617', figure:'distrito especial y localidades', trigger:'organización distrital', currentStatus:'vigente', normType:'ley-ordinaria', reference:'Ley 1617 de 2013', officialUrl:`${senate}ley_1617_2013.html`, reviewedAt, conclusion:'Regula distritos especiales y su organización interna.', limitations:['Bogotá tiene régimen especial propio.'] },
  { id:'bogota-1421', figure:'Bogotá y localidades', trigger:'organización interna de Bogotá', currentStatus:'vigente', normType:'decreto', reference:'Decreto Ley 1421 de 1993 y modificaciones', officialUrl:`${senate}decreto_1421_1993.html`, reviewedAt, conclusion:'Regula Alcalde Mayor, localidades, alcaldes locales, JAL y fondos de desarrollo local.', limitations:['Revisar modificaciones vigentes y acuerdos distritales.'] },
  { id:'indigenous-1953', figure:'territorios indígenas', trigger:'administración de sistemas propios mientras se expide ley orgánica', currentStatus:'transitorio', normType:'decreto', reference:'Decreto 1953 de 2014', officialUrl:'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=59636', reviewedAt, conclusion:'Establece un régimen especial transitorio; resguardo, territorio indígena y entidad territorial no son categorías intercambiables.', limitations:['Puede requerir consulta previa y verificación del ámbito material.'] },
  ...[
    ['c-540-2001','C-540 de 2001','2001/C-540-01.htm'],
    ['c-489-2012','C-489 de 2012','2012/C-489-12.htm'],
    ['c-035-2016','C-035 de 2016','2016/C-035-16.htm'],
    ['c-119-2020','C-119 de 2020','2020/C-119-20.htm'],
    ['c-447-2025','C-447 de 2025','2025/C-447-25.htm'],
  ].map(([id, reference, path]): LegalRule => ({ id, figure:'jurisprudencia territorial', trigger:'interpretación constitucional específica', currentStatus:'requiere-verificacion', normType:'sentencia', reference, officialUrl:`${court}${path}`, reviewedAt, conclusion:'Referencia jurisprudencial incluida en el catálogo; su pertinencia debe verificarse contra la operación concreta.', limitations:['No se infiere una regla causal o de vigencia solo a partir del número de sentencia.'] })),
];

