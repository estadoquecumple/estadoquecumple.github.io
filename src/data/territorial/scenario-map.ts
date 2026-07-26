import type { TerritorialScenario, TerritorialUnit } from './scenario-v2';

type Feature = {
  type: 'Feature';
  id: string;
  properties: Record<string, unknown>;
  geometry: unknown;
};
type Collection = { type: 'FeatureCollection'; features: Feature[] };
export type ScenarioMapCollectionId =
  | 'scenario-created' | 'scenario-transformed' | 'scenario-suppressed'
  | 'scenario-functional' | 'scenario-units' | 'candidate-units'
  | 'selected-departments' | 'selected-municipalities';

const empty = (): Collection => ({ type: 'FeatureCollection', features: [] });
const feature = (unit: TerritorialUnit): Feature => ({
  type: 'Feature',
  id: unit.id,
  properties: {
    id: unit.id,
    name: unit.name,
    state: unit.state,
    levelId: unit.levelId,
    officialCodes: unit.officialCodes,
  },
  geometry: unit.geometry,
});

export function scenarioToMapCollections(scenario: TerritorialScenario): Record<ScenarioMapCollectionId, Collection> {
  const result = {
    'scenario-created': empty(),
    'scenario-transformed': empty(),
    'scenario-suppressed': empty(),
    'scenario-functional': empty(),
    'scenario-units': empty(),
    'candidate-units': empty(),
    'selected-departments': empty(),
    'selected-municipalities': empty(),
  } satisfies Record<ScenarioMapCollectionId, Collection>;
  for (const unit of scenario.units.filter((item) => item.geometry)) {
    const item = feature(unit);
    result['scenario-units'].features.push(item);
    if (unit.id.startsWith('cams-')) result['scenario-created'].features.push(item);
    if (unit.state === 'transformed' || unit.state === 'absorbed') result['scenario-transformed'].features.push(item);
    if (unit.state === 'suppressed-in-scenario') result['scenario-suppressed'].features.push(item);
    if (scenario.memberships.some((membership) => membership.childId === unit.id && membership.relation === 'functional')) {
      result['scenario-functional'].features.push(item);
    }
    if (unit.levelId === 'department') result['selected-departments'].features.push(item);
    if (unit.levelId === 'municipality' || unit.levelId === 'district') result['selected-municipalities'].features.push(item);
  }
  return result;
}
