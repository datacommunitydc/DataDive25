/**
 * Variable configurations for scatterplot explorer
 * Includes B-READY pillars, governance indicators, and outcome variables
 */

import type { CombinedCountryData } from './combined-data';

export interface ScatterplotVariable {
  key: keyof CombinedCountryData;
  label: string;
  category: 'pillar' | 'governance' | 'outcome' | 'demographic';
  description?: string;
  unit?: string;
}

export const scatterplotVariables: ScatterplotVariable[] = [
  // B-READY Pillars
  {
    key: 'pillar1_regulatory_framework',
    label: 'Pillar 1: Regulatory Framework',
    category: 'pillar',
    description: 'Quality of business regulations',
    unit: 'Score (0-100)',
  },
  {
    key: 'pillar2_public_services',
    label: 'Pillar 2: Public Services',
    category: 'pillar',
    description: 'Quality of public services',
    unit: 'Score (0-100)',
  },
  {
    key: 'pillar3_operational_efficiency',
    label: 'Pillar 3: Operational Efficiency',
    category: 'pillar',
    description: 'Efficiency in practice',
    unit: 'Score (0-100)',
  },
  {
    key: 'bready_overall_score',
    label: 'B-READY Overall Score',
    category: 'pillar',
    description: 'Average of three pillars',
    unit: 'Score (0-100)',
  },

  // Governance Indicators
  {
    key: 'regulatory_quality',
    label: 'Regulatory Quality',
    category: 'governance',
    description: 'Ability to formulate sound policies',
    unit: 'Score (-2.5 to 2.5)',
  },
  {
    key: 'government_effectiveness',
    label: 'Government Effectiveness',
    category: 'governance',
    description: 'Quality of public services',
    unit: 'Score (-2.5 to 2.5)',
  },
  {
    key: 'control_of_corruption',
    label: 'Control of Corruption',
    category: 'governance',
    description: 'Extent to which power is not abused',
    unit: 'Score (-2.5 to 2.5)',
  },
  {
    key: 'rule_of_law',
    label: 'Rule of Law',
    category: 'governance',
    description: 'Quality of contract enforcement',
    unit: 'Score (-2.5 to 2.5)',
  },
  {
    key: 'voice_and_accountability',
    label: 'Voice and Accountability',
    category: 'governance',
    description: 'Political rights and civil liberties',
    unit: 'Score (-2.5 to 2.5)',
  },
  {
    key: 'political_stability',
    label: 'Political Stability',
    category: 'governance',
    description: 'Likelihood of political instability',
    unit: 'Score (-2.5 to 2.5)',
  },

  // Economic Outcomes
  {
    key: 'gdp_per_capita_ppp',
    label: 'GDP per capita (PPP)',
    category: 'outcome',
    description: 'GDP per capita, purchasing power parity',
    unit: 'International $',
  },
  {
    key: 'gdp_current_usd',
    label: 'GDP (current USD)',
    category: 'outcome',
    description: 'Gross domestic product',
    unit: 'USD',
  },
  {
    key: 'unemployment_rate',
    label: 'Unemployment Rate',
    category: 'outcome',
    description: 'Unemployment as % of labor force',
    unit: '%',
  },

  // Environmental Outcomes
  {
    key: 'co2_emissions_per_capita',
    label: 'CO₂ per capita',
    category: 'outcome',
    description: 'CO₂ emissions per person',
    unit: 'Tonnes',
  },
  {
    key: 'co2_emissions_mt',
    label: 'CO₂ Emissions (total)',
    category: 'outcome',
    description: 'Total CO₂ emissions',
    unit: 'Million tonnes',
  },
  {
    key: 'energy_per_capita',
    label: 'Energy per capita',
    category: 'outcome',
    description: 'Energy consumption per person',
    unit: 'kWh',
  },
  {
    key: 'energy_per_gdp',
    label: 'Energy per GDP',
    category: 'outcome',
    description: 'Energy intensity of economy',
    unit: 'kWh/$GDP',
  },

  // Demographics
  {
    key: 'population_total',
    label: 'Population',
    category: 'demographic',
    description: 'Total population',
    unit: 'People',
  },
  {
    key: 'pop2022',
    label: 'Population (2022)',
    category: 'demographic',
    description: 'Population as of 2022',
    unit: 'People',
  },
  {
    key: 'area',
    label: 'Land Area',
    category: 'demographic',
    description: 'Total land area',
    unit: 'km²',
  },
  {
    key: 'density',
    label: 'Population Density',
    category: 'demographic',
    description: 'People per km²',
    unit: 'People/km²',
  },
];

/**
 * Group variables by category
 */
export const groupedScatterplotVariables = [
  {
    label: 'B-READY Pillars',
    options: scatterplotVariables.filter((v) => v.category === 'pillar'),
  },
  {
    label: 'Governance Indicators',
    options: scatterplotVariables.filter((v) => v.category === 'governance'),
  },
  {
    label: 'Economic & Environmental Outcomes',
    options: scatterplotVariables.filter((v) => v.category === 'outcome'),
  },
  {
    label: 'Demographics',
    options: scatterplotVariables.filter((v) => v.category === 'demographic'),
  },
];

/**
 * Get variable config by key
 */
export function getScatterplotVariable(key: keyof CombinedCountryData): ScatterplotVariable | undefined {
  return scatterplotVariables.find((v) => v.key === key);
}
