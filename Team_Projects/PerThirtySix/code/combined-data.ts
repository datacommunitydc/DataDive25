/**
 * Combined data structure that merges B-READY outcomes with country metadata and topic data
 * This provides a unified interface for the ScatterplotExplorer component
 */

import { bReadyWithOutcomes, countryPillarTopic } from './index';
import type { BReadyWithOutcomes, CountryPillarTopicData } from './types';
import countryMetadata from '../country/country_metadata.json';

interface CountryMetadata {
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

/**
 * Extended country data combining B-READY outcomes with governance metadata and topic data
 */
export interface CombinedCountryData extends BReadyWithOutcomes {
  // Display fields
  code: string; // alias for country_code
  name: string; // alias for economy_name

  // From metadata
  region: string;
  incomeGroup: string; // camelCase alias
  regulatory_quality: number;
  government_effectiveness: number;
  control_of_corruption: number;
  rule_of_law: number;
  voice_and_accountability: number;
  political_stability: number;
  pop2022?: number;
  area?: number;
  density?: number;

  // B-READY Topic Scores (Pillar 1)
  businessEntryP1: number;
  businessLocationP1: number;
  utilityServicesP1: number;
  laborP1: number;
  financialServicesP1: number;
  internationalTradeP1: number;
  taxationP1: number;
  disputeResolutionP1: number;

  // B-READY Topic Scores (Pillar 2)
  businessEntryP2: number;
  businessLocationP2: number;
  utilityServicesP2: number;
  laborP2: number;
  financialServicesP2: number;
  internationalTradeP2: number;
  taxationP2: number;
  disputeResolutionP2: number;

  // B-READY Topic Scores (Pillar 3)
  businessEntryP3: number;
  businessLocationP3: number;
  utilityServicesP3: number;
  laborP3: number;
  financialServicesP3: number;
  internationalTradeP3: number;
  taxationP3: number;
  disputeResolutionP3: number;
}

/**
 * Merge B-READY outcomes with country metadata and topic data
 */
function mergeBReadyWithMetadata(): CombinedCountryData[] {
  const metadata = countryMetadata as CountryMetadata[];
  const metadataMap = new Map<string, CountryMetadata>();
  const topicDataMap = new Map<string, CountryPillarTopicData>();

  metadata.forEach((m) => {
    if (m.Code) {
      metadataMap.set(m.Code, m);
    }
  });

  countryPillarTopic.forEach((t) => {
    topicDataMap.set(t['Economy Code'], t);
  });

  return bReadyWithOutcomes
    .map((country): CombinedCountryData => {
      const meta = metadataMap.get(country.country_code);
      const topics = topicDataMap.get(country.country_code);

      return {
        ...country,
        // Display aliases
        code: country.country_code,
        name: country.economy_name,
        // Metadata
        region: meta?.region || 'Unknown',
        incomeGroup: meta?.income_group || 'Unknown',
        regulatory_quality: meta?.RegulatoryQuality || 0,
        government_effectiveness: meta?.GovernmentEffectiveness || 0,
        control_of_corruption: meta?.ControlOfCorruption || 0,
        rule_of_law: meta?.RuleofLaw || 0,
        voice_and_accountability: meta?.VoiceAndAccountability || 0,
        political_stability: meta?.PoliticalStabilityNoViolence || 0,
        pop2022: meta?.pop2022,
        area: meta?.area,
        density: meta?.density,
        // Topic data (Pillar 1)
        businessEntryP1: topics?.['Business Entry Pillar 1'] || 0,
        businessLocationP1: topics?.['Business Location Pillar 1'] || 0,
        utilityServicesP1: topics?.['Utility Services Pillar 1'] || 0,
        laborP1: topics?.['Labor Pillar 1'] || 0,
        financialServicesP1: topics?.['Financial Services Pillar 1'] || 0,
        internationalTradeP1: topics?.['International Trade Pillar 1'] || 0,
        taxationP1: topics?.['Taxation Pillar 1'] || 0,
        disputeResolutionP1: topics?.['Dispute Resolution Pillar 1'] || 0,
        // Topic data (Pillar 2)
        businessEntryP2: topics?.['Business Entry Pillar 2'] || 0,
        businessLocationP2: topics?.['Business Location Pillar 2'] || 0,
        utilityServicesP2: topics?.['Utility Services Pillar 2'] || 0,
        laborP2: topics?.['Labor Pillar 2'] || 0,
        financialServicesP2: topics?.['Financial Services Pillar 2'] || 0,
        internationalTradeP2: topics?.['International Trade Pillar 2'] || 0,
        taxationP2: topics?.['Taxation Pillar 2'] || 0,
        disputeResolutionP2: topics?.['Dispute Resolution Pillar 2'] || 0,
        // Topic data (Pillar 3)
        businessEntryP3: topics?.['Business Entry Pillar 3'] || 0,
        businessLocationP3: topics?.['Business Location Pillar 3'] || 0,
        utilityServicesP3: topics?.['Utility Services Pillar 3'] || 0,
        laborP3: topics?.['Labor Pillar 3'] || 0,
        financialServicesP3: topics?.['Financial Services Pillar 3'] || 0,
        internationalTradeP3: topics?.['International Trade Pillar 3'] || 0,
        taxationP3: topics?.['Taxation Pillar 3'] || 0,
        disputeResolutionP3: topics?.['Dispute Resolution Pillar 3'] || 0,
      };
    })
    .filter((c) => c.region !== 'Unknown'); // Filter out countries without metadata
}

export const combinedCountryData = mergeBReadyWithMetadata();

/**
 * Get combined data for a specific country by code
 */
export function getCombinedCountryData(countryCode: string): CombinedCountryData | undefined {
  return combinedCountryData.find((d) => d.country_code === countryCode);
}
