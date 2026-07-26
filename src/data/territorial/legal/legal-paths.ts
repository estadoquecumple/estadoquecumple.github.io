import type { LegalRule } from './legal-registry';
export const legalPath = (rules: LegalRule[]) => rules.map((rule) => ({
  requirement: rule.reference,
  status: rule.currentStatus,
  conclusion: rule.conclusion,
  verification: rule.limitations,
}));

