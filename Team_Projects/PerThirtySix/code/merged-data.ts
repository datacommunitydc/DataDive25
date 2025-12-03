import type { CountryPillarTopicDataset, BReadyWithOutcomesDataset } from './types';
import countryPillarTopicData from './country-pillar-topic.json';
import countryMetadata from '../country/country_metadata.json';
import bReadyWithOutcomesData from './bready_with_outcomes.json';

export interface CountryMetadata {
  Code: string;
  cca3: string;
  region: string;
  income_group: string;
  RegulatoryQuality: number;
  GovernmentEffectiveness: number;
  ControlOfCorruption: number;
  RuleofLaw: number;
  VoiceAndAccountability: number;
  PoliticalStabilityNoViolence: number;
  pop2022?: number;
  area?: number;
  density?: number;
}

export interface MergedCountryData {
  code: string;
  name: string;
  region: string;
  incomeGroup: string;
  // World Bank Pillars by Topic
  businessEntryP1: number;
  businessEntryP2: number;
  businessEntryP3: number;
  businessLocationP1: number;
  businessLocationP2: number;
  businessLocationP3: number;
  utilityServicesP1: number;
  utilityServicesP2: number;
  utilityServicesP3: number;
  laborP1: number;
  laborP2: number;
  laborP3: number;
  financialServicesP1: number;
  financialServicesP2: number;
  financialServicesP3: number;
  internationalTradeP1: number;
  internationalTradeP2: number;
  internationalTradeP3: number;
  taxationP1: number;
  taxationP2: number;
  taxationP3: number;
  disputeResolutionP1: number;
  disputeResolutionP2: number;
  disputeResolutionP3: number;
  // Governance indicators
  regulatoryQuality: number;
  governmentEffectiveness: number;
  controlOfCorruption: number;
  ruleOfLaw: number;
  voiceAndAccountability: number;
  politicalStability: number;
  // Demographics (optional)
  population?: number;
  area?: number;
  density?: number;
  // Outcome variables (optional - from bReadyWithOutcomes)
  gdpCurrentUsd?: number;
  co2EmissionsMt?: number;
  co2EmissionsPerCapita?: number;
  energyPerCapita?: number;
  energyPerGdp?: number;
}

function mergeCountryData(): MergedCountryData[] {
  const metadata = countryMetadata as CountryMetadata[];
  const pillarData = countryPillarTopicData as CountryPillarTopicDataset;
  const outcomesData = bReadyWithOutcomesData as BReadyWithOutcomesDataset;

  // Create maps for quick lookup
  const metadataMap = new Map<string, CountryMetadata>();
  metadata.forEach((m) => {
    if (m.Code) {
      metadataMap.set(m.Code, m);
    }
  });

  const outcomesMap = new Map<string, BReadyWithOutcomesDataset[0]>();
  outcomesData.forEach((o) => {
    if (o.country_code) {
      outcomesMap.set(o.country_code, o);
    }
  });

  // Merge datasets
  const merged: MergedCountryData[] = [];

  pillarData.forEach((country) => {
    const meta = metadataMap.get(country['Economy Code']);
    if (!meta) {
      return; // Skip if no metadata found
    }

    const outcomes = outcomesMap.get(country['Economy Code']);

    merged.push({
      code: country['Economy Code'],
      name: country.Economy,
      region: meta.region || 'Unknown',
      incomeGroup: meta.income_group || 'Unknown',
      // Business Entry
      businessEntryP1: country['Business Entry Pillar 1'],
      businessEntryP2: country['Business Entry Pillar 2'],
      businessEntryP3: country['Business Entry Pillar 3'],
      // Business Location
      businessLocationP1: country['Business Location Pillar 1'],
      businessLocationP2: country['Business Location Pillar 2'],
      businessLocationP3: country['Business Location Pillar 3'],
      // Utility Services
      utilityServicesP1: country['Utility Services Pillar 1'],
      utilityServicesP2: country['Utility Services Pillar 2'],
      utilityServicesP3: country['Utility Services Pillar 3'],
      // Labor
      laborP1: country['Labor Pillar 1'],
      laborP2: country['Labor Pillar 2'],
      laborP3: country['Labor Pillar 3'],
      // Financial Services
      financialServicesP1: country['Financial Services Pillar 1'],
      financialServicesP2: country['Financial Services Pillar 2'],
      financialServicesP3: country['Financial Services Pillar 3'],
      // International Trade
      internationalTradeP1: country['International Trade Pillar 1'],
      internationalTradeP2: country['International Trade Pillar 2'],
      internationalTradeP3: country['International Trade Pillar 3'],
      // Taxation
      taxationP1: country['Taxation Pillar 1'],
      taxationP2: country['Taxation Pillar 2'],
      taxationP3: country['Taxation Pillar 3'],
      // Dispute Resolution
      disputeResolutionP1: country['Dispute Resolution Pillar 1'],
      disputeResolutionP2: country['Dispute Resolution Pillar 2'],
      disputeResolutionP3: country['Dispute Resolution Pillar 3'],
      // Governance
      regulatoryQuality: meta.RegulatoryQuality,
      governmentEffectiveness: meta.GovernmentEffectiveness,
      controlOfCorruption: meta.ControlOfCorruption,
      ruleOfLaw: meta.RuleofLaw,
      voiceAndAccountability: meta.VoiceAndAccountability,
      politicalStability: meta.PoliticalStabilityNoViolence,
      // Demographics
      population: meta.pop2022,
      area: meta.area,
      density: meta.density,
      // Outcome variables
      gdpCurrentUsd: outcomes?.gdp_current_usd ?? undefined,
      co2EmissionsMt: outcomes?.co2_emissions_mt ?? undefined,
      co2EmissionsPerCapita: outcomes?.co2_emissions_per_capita ?? undefined,
      energyPerCapita: outcomes?.energy_per_capita ?? undefined,
      energyPerGdp: outcomes?.energy_per_gdp ?? undefined,
    });
  });

  return merged;
}

export const mergedCountryData = mergeCountryData();
