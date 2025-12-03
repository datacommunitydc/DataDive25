import type {
  CountryPillarDataset,
  CountryPillarTopicDataset,
  BReadyWithOutcomesDataset,
  BReadyWithOutcomes,
  CountryOutcomesDataset,
} from './types';
import countryPillarData from './country-pillar.json';
import countryPillarTopicData from './country-pillar-topic.json';
import bReadyWithOutcomesData from './bready_with_outcomes.json';
import countryOutcomesData from './country_outcomes_data.json';

export const countryPillar: CountryPillarDataset = countryPillarData;
export const countryPillarTopic: CountryPillarTopicDataset = countryPillarTopicData;
export const bReadyWithOutcomes: BReadyWithOutcomesDataset = bReadyWithOutcomesData;
export const countryOutcomes: CountryOutcomesDataset = countryOutcomesData;

/**
 * Get B-READY data for a specific country by code
 */
export function getBReadyCountryData(countryCode: string): BReadyWithOutcomes | undefined {
  return bReadyWithOutcomes.find((d) => d.country_code === countryCode);
}

/**
 * Get countries sorted by overall B-READY score
 */
export function getCountriesByBReadyScore(ascending = false): BReadyWithOutcomes[] {
  return [...bReadyWithOutcomes].sort((a, b) =>
    ascending
      ? a.bready_overall_score - b.bready_overall_score
      : b.bready_overall_score - a.bready_overall_score
  );
}

/**
 * Get countries sorted by a specific pillar
 */
export function getCountriesByPillar(
  pillar: 'pillar1_regulatory_framework' | 'pillar2_public_services' | 'pillar3_operational_efficiency',
  ascending = false
): BReadyWithOutcomes[] {
  return [...bReadyWithOutcomes].sort((a, b) =>
    ascending ? a[pillar] - b[pillar] : b[pillar] - a[pillar]
  );
}

/**
 * Get countries with largest pillar gaps
 */
export function getCountriesByPillarGap(
  gap: 'pillar_gap_1_2' | 'pillar_gap_1_3' | 'pillar_gap_2_3',
  ascending = false
): BReadyWithOutcomes[] {
  return [...bReadyWithOutcomes].sort((a, b) =>
    ascending ? a[gap] - b[gap] : b[gap] - a[gap]
  );
}

/**
 * Calculate correlation between B-READY score and an outcome variable
 */
export function calculateCorrelation(outcomeKey: keyof BReadyWithOutcomes): number | null {
  const validPairs = bReadyWithOutcomes
    .filter((d) => d.bready_overall_score != null && d[outcomeKey] != null)
    .map((d) => ({
      x: d.bready_overall_score,
      y: d[outcomeKey] as number,
    }));

  if (validPairs.length < 3) return null;

  const n = validPairs.length;
  const sumX = validPairs.reduce((acc, p) => acc + p.x, 0);
  const sumY = validPairs.reduce((acc, p) => acc + p.y, 0);
  const sumXY = validPairs.reduce((acc, p) => acc + p.x * p.y, 0);
  const sumX2 = validPairs.reduce((acc, p) => acc + p.x * p.x, 0);
  const sumY2 = validPairs.reduce((acc, p) => acc + p.y * p.y, 0);

  const numerator = n * sumXY - sumX * sumY;
  const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

  return denominator === 0 ? null : numerator / denominator;
}

/**
 * Get top N countries by B-READY score
 */
export function getTopBReadyCountries(n = 10): BReadyWithOutcomes[] {
  return getCountriesByBReadyScore(false).slice(0, n);
}

/**
 * Get bottom N countries by B-READY score
 */
export function getBottomBReadyCountries(n = 10): BReadyWithOutcomes[] {
  return getCountriesByBReadyScore(true).slice(0, n);
}

// Re-export types
export type {
  CountryPillarDataset,
  CountryPillarTopicDataset,
  BReadyWithOutcomesDataset,
  BReadyWithOutcomes,
  CountryOutcomesDataset,
} from './types';

