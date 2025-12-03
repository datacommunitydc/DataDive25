export interface CountryPillarData {
  Economy: string;
  'Economy Code': string;
  'Pillar 1 Regulatory Framework': number;
  'Pillar 2 Public Services': number;
  'Pillar 3 Operational Efficiency': number;
}

export type CountryPillarDataset = CountryPillarData[];

export interface CountryPillarTopicData {
  Economy: string;
  'Economy Code': string;
  'Business Entry Pillar 1': number;
  'Business Entry Pillar 2': number;
  'Business Entry Pillar 3': number;
  'Business Location Pillar 1': number;
  'Business Location Pillar 2': number;
  'Business Location Pillar 3': number;
  'Utility Services Pillar 1': number;
  'Utility Services Pillar 2': number;
  'Utility Services Pillar 3': number;
  'Labor Pillar 1': number;
  'Labor Pillar 2': number;
  'Labor Pillar 3': number;
  'Financial Services Pillar 1': number;
  'Financial Services Pillar 2': number;
  'Financial Services Pillar 3': number;
  'International Trade Pillar 1': number;
  'International Trade Pillar 2': number;
  'International Trade Pillar 3': number;
  'Taxation Pillar 1': number;
  'Taxation Pillar 2': number;
  'Taxation Pillar 3': number;
  'Dispute Resolution Pillar 1': number;
  'Dispute Resolution Pillar 2': number;
  'Dispute Resolution Pillar 3': number;
}

export type CountryPillarTopicDataset = CountryPillarTopicData[];

/**
 * B-READY data augmented with country outcome indicators
 */
export interface BReadyWithOutcomes {
  economy_name: string;
  country_code: string;
  pillar1_regulatory_framework: number;
  pillar2_public_services: number;
  pillar3_operational_efficiency: number;
  country_name?: string | null;
  data_year?: number | null;
  population_total?: number | null;
  gdp_current_usd?: number | null;
  co2_emissions_mt?: number | null;
  co2_emissions_per_capita?: number | null;
  energy_per_capita?: number | null;
  energy_per_gdp?: number | null;
  gdp_per_capita_ppp?: number | null;
  gdp_ppp_year?: number | null;
  unemployment_rate?: number | null;
  unemployment_year?: number | null;
  bready_overall_score: number;
  pillar_gap_1_2: number;
  pillar_gap_1_3: number;
  pillar_gap_2_3: number;
}

export type BReadyWithOutcomesDataset = BReadyWithOutcomes[];

/**
 * Country outcome data (without B-READY scores)
 */
export interface CountryOutcomes {
  country_code: string;
  country_name: string;
  data_year?: number | null;
  population_total?: number | null;
  gdp_current_usd?: number | null;
  co2_emissions_mt?: number | null;
  co2_emissions_per_capita?: number | null;
  energy_per_capita?: number | null;
  energy_per_gdp?: number | null;
}

export type CountryOutcomesDataset = CountryOutcomes[];
