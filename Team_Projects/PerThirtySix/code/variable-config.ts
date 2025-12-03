import type { MergedCountryData } from './merged-data';

export interface VariableConfig {
  key: keyof MergedCountryData;
  label: string;
  category: 'regulatory' | 'governance' | 'demographic' | 'outcome';
  topic?: string;
  pillar?: string;
}

export const variableConfigs: VariableConfig[] = [
  // Business Entry
  {
    key: 'businessEntryP1',
    label: 'Business Entry - Regulatory Framework',
    category: 'regulatory',
    topic: 'Business Entry',
    pillar: 'Pillar 1',
  },
  {
    key: 'businessEntryP2',
    label: 'Business Entry - Public Services',
    category: 'regulatory',
    topic: 'Business Entry',
    pillar: 'Pillar 2',
  },
  {
    key: 'businessEntryP3',
    label: 'Business Entry - Operational Efficiency',
    category: 'regulatory',
    topic: 'Business Entry',
    pillar: 'Pillar 3',
  },
  // Business Location
  {
    key: 'businessLocationP1',
    label: 'Business Location - Regulatory Framework',
    category: 'regulatory',
    topic: 'Business Location',
    pillar: 'Pillar 1',
  },
  {
    key: 'businessLocationP2',
    label: 'Business Location - Public Services',
    category: 'regulatory',
    topic: 'Business Location',
    pillar: 'Pillar 2',
  },
  {
    key: 'businessLocationP3',
    label: 'Business Location - Operational Efficiency',
    category: 'regulatory',
    topic: 'Business Location',
    pillar: 'Pillar 3',
  },
  // Utility Services
  {
    key: 'utilityServicesP1',
    label: 'Utility Services - Regulatory Framework',
    category: 'regulatory',
    topic: 'Utility Services',
    pillar: 'Pillar 1',
  },
  {
    key: 'utilityServicesP2',
    label: 'Utility Services - Public Services',
    category: 'regulatory',
    topic: 'Utility Services',
    pillar: 'Pillar 2',
  },
  {
    key: 'utilityServicesP3',
    label: 'Utility Services - Operational Efficiency',
    category: 'regulatory',
    topic: 'Utility Services',
    pillar: 'Pillar 3',
  },
  // Labor
  {
    key: 'laborP1',
    label: 'Labor - Regulatory Framework',
    category: 'regulatory',
    topic: 'Labor',
    pillar: 'Pillar 1',
  },
  {
    key: 'laborP2',
    label: 'Labor - Public Services',
    category: 'regulatory',
    topic: 'Labor',
    pillar: 'Pillar 2',
  },
  {
    key: 'laborP3',
    label: 'Labor - Operational Efficiency',
    category: 'regulatory',
    topic: 'Labor',
    pillar: 'Pillar 3',
  },
  // Financial Services
  {
    key: 'financialServicesP1',
    label: 'Financial Services - Regulatory Framework',
    category: 'regulatory',
    topic: 'Financial Services',
    pillar: 'Pillar 1',
  },
  {
    key: 'financialServicesP2',
    label: 'Financial Services - Public Services',
    category: 'regulatory',
    topic: 'Financial Services',
    pillar: 'Pillar 2',
  },
  {
    key: 'financialServicesP3',
    label: 'Financial Services - Operational Efficiency',
    category: 'regulatory',
    topic: 'Financial Services',
    pillar: 'Pillar 3',
  },
  // International Trade
  {
    key: 'internationalTradeP1',
    label: 'International Trade - Regulatory Framework',
    category: 'regulatory',
    topic: 'International Trade',
    pillar: 'Pillar 1',
  },
  {
    key: 'internationalTradeP2',
    label: 'International Trade - Public Services',
    category: 'regulatory',
    topic: 'International Trade',
    pillar: 'Pillar 2',
  },
  {
    key: 'internationalTradeP3',
    label: 'International Trade - Operational Efficiency',
    category: 'regulatory',
    topic: 'International Trade',
    pillar: 'Pillar 3',
  },
  // Taxation
  {
    key: 'taxationP1',
    label: 'Taxation - Regulatory Framework',
    category: 'regulatory',
    topic: 'Taxation',
    pillar: 'Pillar 1',
  },
  {
    key: 'taxationP2',
    label: 'Taxation - Public Services',
    category: 'regulatory',
    topic: 'Taxation',
    pillar: 'Pillar 2',
  },
  {
    key: 'taxationP3',
    label: 'Taxation - Operational Efficiency',
    category: 'regulatory',
    topic: 'Taxation',
    pillar: 'Pillar 3',
  },
  // Dispute Resolution
  {
    key: 'disputeResolutionP1',
    label: 'Dispute Resolution - Regulatory Framework',
    category: 'regulatory',
    topic: 'Dispute Resolution',
    pillar: 'Pillar 1',
  },
  {
    key: 'disputeResolutionP2',
    label: 'Dispute Resolution - Public Services',
    category: 'regulatory',
    topic: 'Dispute Resolution',
    pillar: 'Pillar 2',
  },
  {
    key: 'disputeResolutionP3',
    label: 'Dispute Resolution - Operational Efficiency',
    category: 'regulatory',
    topic: 'Dispute Resolution',
    pillar: 'Pillar 3',
  },
  // Governance Indicators
  {
    key: 'regulatoryQuality',
    label: 'Regulatory Quality',
    category: 'governance',
  },
  {
    key: 'governmentEffectiveness',
    label: 'Government Effectiveness',
    category: 'governance',
  },
  {
    key: 'controlOfCorruption',
    label: 'Control of Corruption',
    category: 'governance',
  },
  {
    key: 'ruleOfLaw',
    label: 'Rule of Law',
    category: 'governance',
  },
  {
    key: 'voiceAndAccountability',
    label: 'Voice and Accountability',
    category: 'governance',
  },
  {
    key: 'politicalStability',
    label: 'Political Stability',
    category: 'governance',
  },
  // Demographics
  {
    key: 'population',
    label: 'Population',
    category: 'demographic',
  },
  {
    key: 'area',
    label: 'Area (km²)',
    category: 'demographic',
  },
  {
    key: 'density',
    label: 'Population Density',
    category: 'demographic',
  },
  // Outcome Variables
  {
    key: 'gdpCurrentUsd',
    label: 'GDP (Current USD)',
    category: 'outcome',
  },
  {
    key: 'co2EmissionsMt',
    label: 'CO2 Emissions (Mt)',
    category: 'outcome',
  },
  {
    key: 'co2EmissionsPerCapita',
    label: 'CO2 Emissions per Capita',
    category: 'outcome',
  },
  {
    key: 'energyPerCapita',
    label: 'Energy Use per Capita',
    category: 'outcome',
  },
  {
    key: 'energyPerGdp',
    label: 'Energy Use per GDP',
    category: 'outcome',
  },
];

// Helper to get variable config by key
export function getVariableConfig(key: keyof MergedCountryData): VariableConfig | undefined {
  return variableConfigs.find((v) => v.key === key);
}
