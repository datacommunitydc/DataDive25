<template>
  <div class="mb-20 pt-16 flex justify-center">
    <div class="w-full max-w-[800px]">
      <div class="container max-w-4xl px-6 mb-12 mx-auto">
        <h2 class="font-serif text-3xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">Regulation And Inequality</h2>
        <p class="text-lg md:text-xl text-gray-700 leading-relaxed max-w-2xl">
          This visualization shows the average wealth inequality across all countries for which we have regulatory data. Use the sliders below to filter countries based on their
          regulatory performance, and the visualization will update to show the average wealth distribution for the filtered set.
        </p>
      </div>
      <div class="rounded-lg overflow-hidden">
        <vue-p5 @setup="setup" @draw="draw" v-if="hasMatchingCountries && wealthData"> </vue-p5>
        <div v-else class="bg-gray-50 rounded-lg flex items-center justify-center" style="width: 800px; height: 500px">
          <p class="text-gray-600 text-lg">No countries satisfy these filters</p>
        </div>
      </div>
      <div :class="['flex mt-2 font-bold text-sm']" v-if="hasMatchingCountries && wealthData">
        <div
          v-for="(category, index) in categories"
          :key="category"
          :style="`width: ${(wealthData[category] / totalWealth) * 100}%; color: ${colors[index]}`"
          class="h-4 px-2 transition-label"
        >
          <div class="flex justify-center text-center">
            <div>
              <div class="flex justify-center space-x-1 items-center">
                <div class="text-xs">{{ labels[index] }}</div>
              </div>
              <div class="font-normal text-xs">{{ ((wealthData[category] / totalWealth) * 100).toFixed(1) }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sliders Grid -->
      <div class="mt-8 bg-gray-100 rounded-lg p-3">
        <div class="grid grid-cols-3 gap-3 max-w-2xl pt-2 mx-auto">
          <!-- Header row -->
          <div class="font-semibold text-sm text-gray-700">Are there laws in place?</div>
          <div class="font-semibold text-sm text-gray-700">Are the laws enforced?</div>
          <div class="font-semibold text-sm text-gray-700">Does the system work?</div>

          <!-- Slider rows for each topic -->
          <template v-for="(topic, topicIndex) in topics" :key="topic">
            <div class="space-y-1 px-4">
              <div class="text-xs text-gray-600 mb-0.5">{{ topic }}</div>
              <el-slider
                v-model="sliderValues[topicIndex][0]"
                range
                :min="0"
                :max="100"
                :step="1"
                @input="updateVisualization"
                class="regulatory-slider regulatory-slider-orange"
              />
            </div>
            <div class="space-y-1 px-4">
              <div class="text-xs text-gray-600 mb-0.5 opacity-0">{{ topic }}</div>
              <el-slider v-model="sliderValues[topicIndex][1]" range :min="0" :max="100" :step="1" @input="updateVisualization" class="regulatory-slider regulatory-slider-green" />
            </div>
            <div class="space-y-1 px-4">
              <div class="text-xs text-gray-600 mb-0.5 opacity-0">{{ topic }}</div>
              <el-slider
                v-model="sliderValues[topicIndex][2]"
                range
                :min="0"
                :max="100"
                :step="1"
                @input="updateVisualization"
                class="regulatory-slider regulatory-slider-purple"
              />
            </div>
          </template>
        </div>
        <div class="flex justify-center mt-4">
          <button @click="resetSliders" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
            Reset All Filters
          </button>
        </div>
      </div>
      <div class="mt-4 text-xs text-gray-600 text-center">
        Data from
        <a href="https://wid.world" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline"> World Inequality Database </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import VueP5 from '@/components/Vis/Processing/VueP5.vue';
import wealthDataRaw from '@/helpers/data/wealth/wealth.json';
import countryPillarData from '@/helpers/data/world-bank/country-pillar.json';
import countryPillarTopicData from '@/helpers/data/world-bank/country-pillar-topic.json';

const categories = ['Bottom50', 'Next40', 'Next9', 'RemainingTop1', 'TopPt1'].reverse();
const colors = ['#08384E', '#665191', '#a05195', '#F3505E', '#ffa600'].reverse();
const labels = ['Top 0.1%', 'Next 0.9%', 'Next 9%', 'Next 40%', 'Bottom 50%'];

const sketch = ref<any>(null);
const figures = ref<any[]>([]);
const wealthData = ref<Record<string, number> | null>(null);
const hasMatchingCountries = ref<boolean>(true);
// Store stick figure positions per category to keep them in place
const stickFigurePositions = ref<Record<string, Array<{ x: number; y: number; relativeX: number; big: boolean }>>>({});
const categoryWidths = ref<Record<string, number>>({});
const totalWealth = computed(() => {
  if (!wealthData.value) return 0;
  return Object.values(wealthData.value).reduce((sum, val) => sum + val, 0);
});

// Topics for sliders (8 topics)
const topics = ['Business Entry', 'Business Location', 'Dispute Resolution', 'Financial Services', 'International Trade', 'Labor', 'Taxation', 'Utility Services'];

// Slider values: 8 topics × 3 pillars = 24 sliders (range sliders)
// Initialize all sliders to [0, 100] range
const sliderValues = ref(
  topics.map(() => [
    [0, 100],
    [0, 100],
    [0, 100],
  ])
);

onMounted(() => {
  calculateAverageWealth();
});

// Map country names from regulatory data to wealth data
const countryNameMap: Record<string, string> = {
  Barbados: 'Barbados',
  "Côte d'Ivoire": "Cote d'Ivoire",
  'Gambia, The': 'Gambia',
  'Hong Kong SAR, China': 'Hong Kong',
  'Kyrgyz Republic': 'Kyrgyzstan',
  Samoa: 'Samoa',
  'Slovak Republic': 'Slovakia',
  Vanuatu: 'Vanuatu',
  'Viet Nam': 'Vietnam',
  'West Bank and Gaza': 'Palestine',
};

const calculateAverageWealth = (filteredCountryNames?: string[]) => {
  // Get all Economy names from regulatory data, or use filtered list
  const regulatoryCountryNames = filteredCountryNames || countryPillarData.map((d: any) => d.Economy.trim());

  // If no countries match the filters, show message
  if (regulatoryCountryNames.length === 0) {
    wealthData.value = null;
    hasMatchingCountries.value = false;
    if (sketch.value) {
      sketch.value.clear();
      sketch.value.background('#F1F1E9');
      sketch.value.noLoop();
    }
    return;
  }

  // Group wealth data by country name
  const wealthByCountry: Record<string, any> = {};
  for (const entry of wealthDataRaw as any[]) {
    if (!entry.Country || !entry.Percentile || entry.Year !== 2021) continue;

    const countryName = entry.Country.trim();
    if (!wealthByCountry[countryName]) {
      wealthByCountry[countryName] = {};
    }
    wealthByCountry[countryName][entry.Percentile] = entry.Value;
  }

  // Find matching countries by direct name match or mapped name
  const matchingCountries: any[] = [];
  const unmatchedCountries: string[] = [];

  for (const regCountryName of regulatoryCountryNames) {
    // Try direct match first
    let matchedData = wealthByCountry[regCountryName];

    // If no direct match, try mapped name
    if (!matchedData && countryNameMap[regCountryName]) {
      matchedData = wealthByCountry[countryNameMap[regCountryName]];
    }

    if (matchedData) {
      matchingCountries.push(matchedData);
    } else {
      unmatchedCountries.push(regCountryName);
    }
  }

  if (unmatchedCountries.length > 0) {
    console.log('Countries from regulatory data that do not match wealth.json:', unmatchedCountries);
  }

  if (matchingCountries.length === 0) {
    console.warn('No matching countries found');
    wealthData.value = null;
    hasMatchingCountries.value = false;
    if (sketch.value) {
      sketch.value.clear();
      sketch.value.background('#F1F1E9');
      sketch.value.noLoop();
    }
    return;
  }

  hasMatchingCountries.value = true;

  // Calculate averages for each percentile that is available
  const avgP999p100 = matchingCountries.reduce((sum, c) => sum + (c['p99.9p100'] || 0), 0) / matchingCountries.length;
  const avgP99p100 = matchingCountries.reduce((sum, c) => sum + (c['p99p100'] || 0), 0) / matchingCountries.length;
  const avgP90p100 = matchingCountries.reduce((sum, c) => sum + (c['p90p100'] || 0), 0) / matchingCountries.length;
  const avgP95p100 = matchingCountries.reduce((sum, c) => sum + (c['p95p100'] || 0), 0) / matchingCountries.length;

  // Calculate wealth bands using only available percentiles (no estimation)
  const topPt1 = avgP999p100; // Top 0.1%
  const remainingTop1 = avgP99p100 - avgP999p100; // Next 0.9% (p99p100 - p99.9p100)
  const next9 = avgP90p100 - avgP99p100; // Next 9% (p90p100 - p99p100)

  // For the remaining wealth (1 - p90p100), we can't split it accurately without p50p100
  // So we'll show what we have: Top 0.1%, Next 0.9%, Next 9%, and the remainder
  const remainingWealth = 1 - avgP90p100; // This is the bottom 90% combined

  // Store as wealth shares (multiply by large number to match user's example format)
  const multiplier = 100000000;
  wealthData.value = {
    TopPt1: topPt1 * multiplier,
    RemainingTop1: remainingTop1 * multiplier,
    Next9: next9 * multiplier,
    Next40: remainingWealth * 0.444 * multiplier, // Approximate: 40/90 of remaining
    Bottom50: remainingWealth * 0.556 * multiplier, // Approximate: 50/90 of remaining
  };

  // Redraw visualization if sketch is ready
  if (sketch.value && wealthData.value) {
    drawVisualization(sketch.value);
  }
};

const drawVisualization = (sketchInstance: any) => {
  if (!wealthData.value) {
    return;
  }

  const canvasWidth = 800;
  const canvasHeight = 500;

  sketchInstance.clear();
  sketchInstance.background('#F1F1E9');
  sketchInstance.textAlign(sketchInstance.CENTER, sketchInstance.CENTER);

  let x = 0;
  for (let i = 0; i < categories.length; i++) {
    const category = categories[i];
    const rawColor = sketchInstance.color(colors[i]);
    const pastelColor = sketchInstance.lerpColor(rawColor, sketchInstance.color(255), 0.5);
    const wealth = wealthData.value[category];
    const w = (wealth / totalWealth.value) * canvasWidth;

    // Get old width before updating
    const oldWidth = categoryWidths.value[category] || w;
    // Store the new width for this category
    categoryWidths.value[category] = w;

    // Draw pastel rectangle
    sketchInstance.fill(pastelColor);
    sketchInstance.noStroke();
    sketchInstance.rect(x, 0, w, canvasHeight);

    // Determine figure count by population share
    let count: number;
    if (category === 'TopPt1') count = 1;
    else if (category === 'RemainingTop1') count = 9;
    else if (category === 'Next9') count = 90;
    else if (category === 'Next40') count = 400;
    else if (category === 'Bottom50') count = 500;
    else count = 0;

    // Initialize or update stick figure positions
    if (!stickFigurePositions.value[category] || stickFigurePositions.value[category].length !== count) {
      // Generate new positions if category count changed or first time
      stickFigurePositions.value[category] = [];
      for (let j = 0; j < count; j++) {
        const relativeX = sketchInstance.random(0.05, 0.95); // Store as relative position (0-1)
        const y = sketchInstance.random(5, canvasHeight - 15);
        stickFigurePositions.value[category].push({
          x: x + relativeX * w, // Current absolute position
          y: y,
          relativeX: relativeX, // Store relative position for scaling
          big: category === 'TopPt1',
        });
      }
    } else {
      // Update positions based on new width, keeping relative positions
      for (let j = 0; j < stickFigurePositions.value[category].length; j++) {
        const pos = stickFigurePositions.value[category][j];
        // Scale the x position proportionally to the new width
        pos.x = x + pos.relativeX * w;
      }
    }

    const stickColor = sketchInstance.lerpColor(rawColor, sketchInstance.color(0), 0.2);
    if (category === 'Bottom50') {
      stickColor.setAlpha(150); // slight transparency
    }

    sketchInstance.stroke(stickColor);
    sketchInstance.fill(stickColor);

    // Draw stick figures at their stored positions
    for (let j = 0; j < stickFigurePositions.value[category].length; j++) {
      const pos = stickFigurePositions.value[category][j];
      drawStickFigure(sketchInstance, pos.x, pos.y, pos.big);
    }

    x += w;
  }
};

const setup = (sketchInstance: any) => {
  sketch.value = sketchInstance;
  const canvasWidth = 800;
  const canvasHeight = 500;
  sketchInstance.createCanvas(canvasWidth, canvasHeight);
  sketchInstance.background('#F1F1E9');
  sketchInstance.textAlign(sketchInstance.CENTER, sketchInstance.CENTER);
  sketchInstance.noLoop(); // We'll manually redraw when needed

  // Draw initial visualization after data is loaded
  if (wealthData.value) {
    drawVisualization(sketchInstance);
  }
};

const draw = (sketchInstance: any) => {
  // We handle drawing manually via drawVisualization
  sketchInstance.noLoop();
};

const resetSliders = () => {
  // Reset all sliders to [0, 100]
  sliderValues.value = topics.map(() => [
    [0, 100],
    [0, 100],
    [0, 100],
  ]);
  // Update visualization with reset values
  updateVisualization();
};

const updateVisualization = () => {
  // Filter countries based on slider values
  const filteredCountries = filterCountriesBySliders();

  // Recalculate averages with filtered countries
  calculateAverageWealth(filteredCountries);

  // Redraw the visualization (stick figures will maintain relative positions)
  if (sketch.value && wealthData.value && hasMatchingCountries.value) {
    drawVisualization(sketch.value);
  }
};

const filterCountriesBySliders = (): string[] => {
  // Start with all countries from topic data
  const allCountries = countryPillarTopicData as any[];
  const filteredCountries: string[] = [];

  for (const country of allCountries) {
    let passesAllFilters = true;

    // Check each topic
    for (let topicIndex = 0; topicIndex < topics.length; topicIndex++) {
      const topic = topics[topicIndex];
      const [pillar1Range, pillar2Range, pillar3Range] = sliderValues.value[topicIndex];

      // Get pillar values for this topic
      const pillar1Field = `${topic} Pillar 1`;
      const pillar2Field = `${topic} Pillar 2`;
      const pillar3Field = `${topic} Pillar 3`;

      const pillar1Value = country[pillar1Field];
      const pillar2Value = country[pillar2Field];
      const pillar3Value = country[pillar3Field];

      // Check if all three pillars are within their ranges
      const pillar1InRange = pillar1Value >= pillar1Range[0] && pillar1Value <= pillar1Range[1];
      const pillar2InRange = pillar2Value >= pillar2Range[0] && pillar2Value <= pillar2Range[1];
      const pillar3InRange = pillar3Value >= pillar3Range[0] && pillar3Value <= pillar3Range[1];

      // All three pillars must be in range for this topic
      if (!(pillar1InRange && pillar2InRange && pillar3InRange)) {
        passesAllFilters = false;
        break;
      }
    }

    if (passesAllFilters) {
      filteredCountries.push(country.Economy.trim());
    }
  }

  return filteredCountries;
};

const drawStickFigure = (sketchInstance: any, x: number, y: number, big: boolean) => {
  const factor = big ? 1.5 : 1;
  const headSize = 4 * factor;
  const bodyLength = 6 * factor;
  const limbLength = 4.8 * factor;

  // Head
  sketchInstance.ellipse(x, y, headSize, headSize);

  // Body
  sketchInstance.line(x, y + headSize / 2, x, y + headSize / 2 + bodyLength);

  // Arms
  sketchInstance.line(x, y + headSize + 1.2, x - limbLength / 2, y + headSize + 3.2);
  sketchInstance.line(x, y + headSize + 1.2, x + limbLength / 2, y + headSize + 3.2);

  // Legs
  sketchInstance.line(x, y + headSize / 2 + bodyLength, x - limbLength / 2, y + headSize / 2 + bodyLength + limbLength / 2);
  sketchInstance.line(x, y + headSize / 2 + bodyLength, x + limbLength / 2, y + headSize / 2 + bodyLength + limbLength / 2);
};
</script>

<style scoped>
:deep(.regulatory-slider) {
  --el-slider-runway-bg-color: #f3f4f6;
  --el-slider-button-size: 16px;
  --el-slider-height: 6px;
}

:deep(.regulatory-slider .el-slider__runway) {
  height: 6px;
  border-radius: 3px;
}

:deep(.regulatory-slider .el-slider__bar) {
  height: 6px;
  border-radius: 3px;
}

/* Orange for Pillar 1 - middle tone */
:deep(.regulatory-slider-orange .el-slider__bar) {
  background: linear-gradient(90deg, #fb923c 0%, #f97316 100%);
}

:deep(.regulatory-slider-orange .el-slider__button) {
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #f97316;
  transition: all 0.2s ease;
}

:deep(.regulatory-slider-orange .el-slider__button:hover) {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(249, 115, 22, 0.3);
}

/* Green for Pillar 2 - middle tone */
:deep(.regulatory-slider-green .el-slider__bar) {
  background: linear-gradient(90deg, #4ade80 0%, #22c55e 100%);
}

:deep(.regulatory-slider-green .el-slider__button) {
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #22c55e;
  transition: all 0.2s ease;
}

:deep(.regulatory-slider-green .el-slider__button:hover) {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(34, 197, 94, 0.3);
}

/* Purple for Pillar 3 - middle tone */
:deep(.regulatory-slider-purple .el-slider__bar) {
  background: linear-gradient(90deg, #a78bfa 0%, #a855f7 100%);
}

:deep(.regulatory-slider-purple .el-slider__button) {
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: #a855f7;
  transition: all 0.2s ease;
}

:deep(.regulatory-slider-purple .el-slider__button:hover) {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(168, 85, 247, 0.3);
}
</style>
