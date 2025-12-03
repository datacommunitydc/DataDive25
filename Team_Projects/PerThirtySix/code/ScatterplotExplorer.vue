<template>
  <div class="w-full">
    <!-- Controls Section -->
    <div class="container max-w-6xl px-6 mb-10">
      <div class="bg-gray-50 border border-gray-200 p-6 md:p-8">
        <div class="flex flex-col lg:flex-row items-stretch gap-5">
          <!-- X-axis -->
          <div class="flex flex-col gap-2 flex-1">
            <label class="text-xs font-bold text-gray-900 uppercase tracking-wider">Horizontal →</label>
            <el-select v-model="selectedXVariable" filterable placeholder="Choose a metric..." size="large" class="w-full scatterplot-select">
              <el-option-group v-for="group in groupedVariables" :key="group.label" :label="group.label">
                <el-option v-for="variable in group.options" :key="variable.key" :label="variable.label" :value="variable.key">
                  <div class="flex items-center justify-between gap-3 py-0.5">
                    <span class="text-sm">{{ variable.label }}</span>
                    <span v-if="variable.topic" class="text-xs text-gray-400">{{ variable.topic }}</span>
                  </div>
                </el-option>
              </el-option-group>
            </el-select>
          </div>

          <!-- Visual separator -->
          <div class="hidden lg:flex items-center justify-center text-gray-300">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>

          <!-- Y-axis -->
          <div class="flex flex-col gap-2 flex-1">
            <label class="text-xs font-bold text-gray-900 uppercase tracking-wider">Vertical ↑</label>
            <el-select v-model="selectedYVariable" filterable placeholder="Choose a metric..." size="large" class="w-full scatterplot-select">
              <el-option-group v-for="group in groupedVariables" :key="group.label" :label="group.label">
                <el-option v-for="variable in group.options" :key="variable.key" :label="variable.label" :value="variable.key">
                  <div class="flex items-center justify-between gap-3 py-0.5">
                    <span class="text-sm">{{ variable.label }}</span>
                    <span v-if="variable.topic" class="text-xs text-gray-400">{{ variable.topic }}</span>
                  </div>
                </el-option>
              </el-option-group>
            </el-select>
          </div>
        </div>
      </div>
    </div>

    <!-- Scatterplot Card -->
    <div class="container max-w-6xl px-6 mb-10">
      <div ref="chartContainer" class="bg-white border border-gray-200">
        <ScatterplotWrapper
          v-if="scatterplotData.length > 0 && chartWidth > 0"
          :key="chartKey"
          :data="scatterplotData"
          :xFeature="xFeature"
          :yFeature="yFeature"
          :colorAccessor="colorAccessor"
          :pointHtml="pointHtml"
          :pointHoverTooltip="pointHoverTooltip"
          :width="chartWidth"
          :height="500"
          :showExport="false"
        />
      </div>
    </div>

    <!-- Legend with integrated color control -->
    <div class="container max-w-6xl px-6">
      <div class="flex flex-col gap-6">
        <div class="inline-flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-2.5 border border-gray-200 self-center">
          <label class="text-xs font-bold text-gray-900 uppercase tracking-wide">Color by</label>
        <el-select v-model="colorBy" size="large" style="width: 240px" class="scatterplot-select-small">
          <el-option label="Region" value="region">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span class="text-sm">Geographic Region</span>
            </div>
          </el-option>
          <el-option label="Income Group" value="incomeGroup">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span class="text-sm">Income Level</span>
            </div>
          </el-option>
        </el-select>
      </div>

        <div v-if="colorBy === 'region'" class="flex flex-wrap justify-center gap-x-5 gap-y-2.5 py-4">
          <div v-for="region in uniqueRegions" :key="region" class="flex items-center gap-1.5">
            <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: regionColorScale(region) }"></div>
            <span class="text-xs text-gray-700">{{ region }}</span>
          </div>
        </div>

        <div v-if="colorBy === 'incomeGroup'" class="flex flex-wrap justify-center gap-x-5 gap-y-2.5 py-4">
          <div v-for="group in uniqueIncomeGroups" :key="group" class="flex items-center gap-1.5">
            <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: incomeColorScale(group) }"></div>
            <span class="text-xs text-gray-700">{{ group }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import * as d3 from 'd3';
import ScatterplotWrapper from '@/components/Vis/D3/Charts/ScatterplotWrapper.vue';
import { combinedCountryData } from '@/helpers/data/world-bank/combined-data';
import { groupedScatterplotVariables } from '@/helpers/data/world-bank/scatterplot-variables';
import type { CombinedCountryData } from '@/helpers/data/world-bank/combined-data';
import type { IBaseDatum, IFeature } from '@/components/Vis/D3/Charts/Scatterplot';
import DrawRadarChart from '@/components/Vis/D3/Charts/radar-chart.js';

interface ScatterplotDatum extends IBaseDatum {
  country: CombinedCountryData;
}

// Group variables by category
const groupedVariables = groupedScatterplotVariables;

// Chart container ref and responsive width
const chartContainer = ref<HTMLElement | null>(null);
const chartWidth = ref(0);

// Selected variables
const selectedXVariable = ref<keyof CombinedCountryData>('bready_overall_score');
const selectedYVariable = ref<keyof CombinedCountryData>('gdp_per_capita_ppp');
const colorBy = ref<'region' | 'incomeGroup'>('region');

// Chart key to force re-render when variables change
const chartKey = computed(() => `${selectedXVariable.value}-${selectedYVariable.value}-${colorBy.value}`);

// Get unique regions and income groups
const uniqueRegions = computed(() => {
  const regions = new Set(combinedCountryData.map((d) => d.region));
  return Array.from(regions).sort();
});

const uniqueIncomeGroups = computed(() => {
  const groups = new Set(combinedCountryData.map((d) => d.incomeGroup));
  // Order from low to high income
  const orderedGroups = ['Low Income', 'Lower Middle Income', 'Upper Middle Income', 'High Income'];
  return orderedGroups.filter((g) => groups.has(g));
});

// Color scales
const regionColorScale = d3
  .scaleOrdinal<string>()
  .domain(['East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa', 'North America', 'South Asia', 'Sub-Saharan Africa'])
  .range(['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444', '#6366f1']);

const incomeColorScale = d3
  .scaleOrdinal<string>()
  .domain(['Low Income', 'Lower Middle Income', 'Upper Middle Income', 'High Income'])
  .range(['#dc2626', '#f97316', '#eab308', '#22c55e']); // red → orange → yellow → green gradient

// Prepare data for scatterplot
const scatterplotData = computed<ScatterplotDatum[]>(() => {
  return combinedCountryData
    .filter((country) => {
      const xVal = country[selectedXVariable.value];
      const yVal = country[selectedYVariable.value];
      return typeof xVal === 'number' && typeof yVal === 'number' && !isNaN(xVal as number) && !isNaN(yVal as number);
    })
    .map((country) => ({
      id: country.code,
      country,
    }));
});

// X and Y features for scatterplot
const xFeature = computed<IFeature<ScatterplotDatum>>(() => {
  const config = groupedScatterplotVariables
    .flatMap((g) => g.options)
    .find((v) => v.key === selectedXVariable.value);

  return {
    label: config?.label || 'X',
    valueAccessor: (d: ScatterplotDatum) => {
      const val = d.country[selectedXVariable.value];
      return typeof val === 'number' ? val : 0;
    },
  };
});

const yFeature = computed<IFeature<ScatterplotDatum>>(() => {
  const config = groupedScatterplotVariables
    .flatMap((g) => g.options)
    .find((v) => v.key === selectedYVariable.value);

  return {
    label: config?.label || 'Y',
    valueAccessor: (d: ScatterplotDatum) => {
      const val = d.country[selectedYVariable.value];
      return typeof val === 'number' ? val : 0;
    },
  };
});

// Color accessor
const colorAccessor = (d: ScatterplotDatum) => {
  if (colorBy.value === 'region') {
    return regionColorScale(d.country.region);
  } else {
    return incomeColorScale(d.country.incomeGroup);
  }
};

// Point HTML - show country code with colored text
const pointHtml = (d: ScatterplotDatum) => {
  const color = colorAccessor(d);
  return `
    <g class="point-group">
      <!-- Invisible larger circle for better hover target -->
      <circle r="8" fill="transparent" pointer-events="all"></circle>
      <!-- Text with white outline for readability -->
      <text
        dy="0.35em"
        text-anchor="middle"
        font-size="9"
        font-weight="600"
        fill="#fff"
        stroke="#fff"
        stroke-width="3"
        paint-order="stroke"
        pointer-events="none"
      >${d.country.code}</text>
      <!-- Colored text -->
      <text
        dy="0.35em"
        text-anchor="middle"
        font-size="9"
        font-weight="600"
        fill="${color}"
        pointer-events="none"
      >${d.country.code}</text>
    </g>
  `;
};

// Tooltip with radar chart - minimal high-tech aesthetic
const pointHoverTooltip = (tooltip: d3.Selection<HTMLDivElement, any, any, any>, d: ScatterplotDatum) => {
  tooltip.html('');
  tooltip.style('width', '320px');
  tooltip.style('background', 'rgba(17, 24, 39, 0.95)'); // dark with slight transparency
  tooltip.style('border', '1px solid rgba(156, 163, 175, 0.2)'); // subtle border

  const country = d.country;
  const chartColor = colorBy.value === 'region' ? regionColorScale(country.region) : incomeColorScale(country.incomeGroup);

  // Header with country name - minimal design
  const header = tooltip.append('div').attr('class', 'px-4 pt-4 pb-3');
  header.append('div').attr('class', 'text-xs font-medium tracking-wide uppercase').style('color', 'rgba(156, 163, 175, 0.8)').text(country.code);
  header.append('div').attr('class', 'text-base font-semibold mt-1').style('color', chartColor).text(country.name);

  // Legend for the three pillars
  const legend = tooltip.append('div').attr('class', 'px-4 py-2 flex justify-center gap-3').style('border-top', '1px solid rgba(156, 163, 175, 0.1)');

  // Add legend items
  const legendItems = [
    { name: 'Regulatory Framework', color: '#60a5fa' },
    { name: 'Public Services', color: '#34d399' },
    { name: 'Operational Efficiency', color: '#f59e0b' },
  ];

  legendItems.forEach((item) => {
    const legendItem = legend.append('div').attr('class', 'flex items-center gap-1.5');
    legendItem.append('div').style('width', '8px').style('height', '8px').style('background', item.color).style('border-radius', '1px');
    legendItem.append('span').attr('class', 'text-xs').style('color', 'rgba(229, 231, 235, 0.8)').style('font-size', '9px').text(item.name.replace(' ', ' '));
  });

  // Radar chart container
  const chartContainer = tooltip.append('div').attr('class', 'px-2 pb-2');

  // Radar chart - 3 series (one per pillar), 8 data points (one per topic)
  // Use distinct colors that are easily distinguishable
  const radarData = [
    {
      name: 'Regulatory Framework',
      id: 'pillar1',
      color: '#60a5fa', // bright blue
      opacity: 0.25,
      values: [
        { axis: 'Business Entry', value: country.businessEntryP1 },
        { axis: 'Business Location', value: country.businessLocationP1 },
        { axis: 'Utility Services', value: country.utilityServicesP1 },
        { axis: 'Labor', value: country.laborP1 },
        { axis: 'Financial Services', value: country.financialServicesP1 },
        { axis: 'International Trade', value: country.internationalTradeP1 },
        { axis: 'Taxation', value: country.taxationP1 },
        { axis: 'Dispute Resolution', value: country.disputeResolutionP1 },
      ],
    },
    {
      name: 'Public Services',
      id: 'pillar2',
      color: '#34d399', // bright green
      opacity: 0.3,
      values: [
        { axis: 'Business Entry', value: country.businessEntryP2 },
        { axis: 'Business Location', value: country.businessLocationP2 },
        { axis: 'Utility Services', value: country.utilityServicesP2 },
        { axis: 'Labor', value: country.laborP2 },
        { axis: 'Financial Services', value: country.financialServicesP2 },
        { axis: 'International Trade', value: country.internationalTradeP2 },
        { axis: 'Taxation', value: country.taxationP2 },
        { axis: 'Dispute Resolution', value: country.disputeResolutionP2 },
      ],
    },
    {
      name: 'Operational Efficiency',
      id: 'pillar3',
      color: '#f59e0b', // bright amber
      opacity: 0.25,
      values: [
        { axis: 'Business Entry', value: country.businessEntryP3 },
        { axis: 'Business Location', value: country.businessLocationP3 },
        { axis: 'Utility Services', value: country.utilityServicesP3 },
        { axis: 'Labor', value: country.laborP3 },
        { axis: 'Financial Services', value: country.financialServicesP3 },
        { axis: 'International Trade', value: country.internationalTradeP3 },
        { axis: 'Taxation', value: country.taxationP3 },
        { axis: 'Dispute Resolution', value: country.disputeResolutionP3 },
      ],
    },
  ];

  DrawRadarChart(chartContainer, radarData, {
    w: 200,
    h: 200,
    maxValue: 100,
    margin: { top: 45, left: 65, right: 65, bottom: 45 },
    dotRadius: 2.5,
    showOutline: true,
    strokeWidth: 2.5,
    color: (d: any) => d.color,
    labelFactor: 1.28, // Bring labels closer to reduce cutoff
  });

  // Style the radar chart text labels to be lighter and smaller
  chartContainer.selectAll('.legend').style('fill', 'rgba(229, 231, 235, 0.9)').style('font-size', '9px').style('font-weight', '500');
  chartContainer.selectAll('.line').style('stroke', 'rgba(156, 163, 175, 0.15)');
};

// Responsive chart width
const updateChartWidth = () => {
  if (chartContainer.value) {
    chartWidth.value = chartContainer.value.offsetWidth;
  }
};

onMounted(() => {
  updateChartWidth();
  window.addEventListener('resize', updateChartWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateChartWidth);
});
</script>

<style scoped>
/* Enhance select appearance */
:deep(.scatterplot-select .el-input__wrapper) {
  transition: all 0.2s ease;
  border: 1px solid rgb(229, 231, 235);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

:deep(.scatterplot-select .el-input__wrapper:hover) {
  border-color: rgb(209, 213, 219);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.06);
}

:deep(.scatterplot-select.is-focused .el-input__wrapper) {
  border-color: rgb(99, 102, 241);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

:deep(.scatterplot-select-small .el-input__wrapper) {
  transition: all 0.2s ease;
  border: 1px solid rgb(229, 231, 235);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

:deep(.scatterplot-select-small .el-input__wrapper:hover) {
  border-color: rgb(209, 213, 219);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.06);
}

:deep(.scatterplot-select-small.is-focused .el-input__wrapper) {
  border-color: rgb(99, 102, 241);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
</style>
