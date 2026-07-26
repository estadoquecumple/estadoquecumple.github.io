import { readFileSync } from 'node:fs';
const files=['src/data/territorial/legal/legal-registry.ts','src/data/territorial/legal/figure-catalog.ts','src/data/territorial/legal/jurisprudence.ts','src/data/territorial/legal/consequence-rules.ts','src/data/territorial/legal/legal-paths.ts'];
const text=files.map((file)=>readFileSync(file,'utf8')).join('\n');
const required=['Ley 1454 de 2011','Ley 1962 de 2019','Decreto 1033 de 2021','Ley 1625 de 2013','Ley 2199 de 2022','Ley 2200 de 2022','Ley 136 de 1994','Ley 1551 de 2012','Ley 1617 de 2013','Decreto Ley 1421 de 1993','Decreto 1953 de 2014','C-540 de 2001','C-489 de 2012','C-035 de 2016','C-119 de 2020','C-447 de 2025','Estado federado','Área metropolitana','Comuna','Localidad'];
const errors=required.filter((term)=>!text.includes(term)).map((term)=>`falta ${term}`);
for(const field of ['currentStatus','normType','officialUrl','reviewedAt','conclusion','limitations'])if(!text.includes(field))errors.push(`falta campo ${field}`);
if(!text.includes('No corresponde a una figura vigente'))errors.push('falta advertencia constitucional');
if(errors.length){console.error(`LEGAL AUDIT: ${errors.join('; ')}`);process.exit(1);}
console.log(`LEGAL AUDIT OK: ${required.length} referencias/figuras mínimas, estados, URLs oficiales, revisión y advertencia constitucional.`);
