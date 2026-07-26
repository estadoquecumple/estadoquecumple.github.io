import { legalRegistry } from './legal-registry';
export const jurisprudence = legalRegistry.filter((rule) => rule.normType === 'sentencia');

