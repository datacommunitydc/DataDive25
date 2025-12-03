<template>
  <div class="w-full">
    <!-- AG Grid Component -->
    <section class="w-full mb-32">
      <div class="container max-w-4xl px-6 mb-12 mx-auto">
        <h2 class="font-serif text-3xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">The complete picture</h2>
        <p class="text-lg md:text-xl text-gray-700 leading-relaxed max-w-2xl">
          How does each country perform across the three pillars? The table below shows scores for all 50 countries—select a specific business topic to see detailed results.
        </p>
      </div>
      <div class="flex justify-center mb-8">
        <div class="inline-flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-2.5 border border-gray-200">
          <label class="text-xs font-semibold text-gray-700 uppercase tracking-wide">Topic</label>
          <client-only>
            <el-select v-model="selectedTopic" class="!w-80 font-sans scatterplot-select" size="large" @change="onTopicChange">
              <el-option-group label="Overview">
                <el-option label="Overall Performance" value="overall" />
              </el-option-group>
              <el-option-group label="Business Operations">
                <el-option label="Business Entry" value="Business Entry" />
                <el-option label="Business Location" value="Business Location" />
                <el-option label="Utility Services" value="Utility Services" />
              </el-option-group>
              <el-option-group label="Employment & Finance">
                <el-option label="Labor" value="Labor" />
                <el-option label="Financial Services" value="Financial Services" />
              </el-option-group>
              <el-option-group label="Trade & Compliance">
                <el-option label="International Trade" value="International Trade" />
                <el-option label="Taxation" value="Taxation" />
                <el-option label="Dispute Resolution" value="Dispute Resolution" />
              </el-option-group>
            </el-select>
            <template #fallback>
              <div class="w-80 h-10 border border-gray-300 rounded flex items-center px-3 text-gray-500">Overall Performance</div>
            </template>
          </client-only>
        </div>
      </div>
      <div class="w-full flex justify-center px-6">
        <div class="bg-white border border-gray-200 overflow-hidden mx-auto" style="width: 1000px; max-width: 100%">
          <ag-grid-vue
            class="w-full h-[600px] ag-theme-alpine ag-perthirtysix regulatory-jobs-grid"
            :headerHeight="53"
            :suppressCellSelection="true"
            :alwaysShowHorizontalScroll="true"
            :columnDefs="gridColumns"
            :key="selectedTopic"
            :rowData="gridData"
            :defaultColDef="{ sortable: true, filter: false }"
            @grid-ready="onGridReady"
          >
          </ag-grid-vue>
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 px-6 py-5 bg-gray-50 border-t border-gray-200">
            <div class="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs">
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-sm" style="background-color: #f97316"></div>
                <span class="text-gray-700 font-medium">Regulation Quality</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-sm" style="background-color: #22c55e"></div>
                <span class="text-gray-700 font-medium">Public Services</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-sm" style="background-color: #a855f7"></div>
                <span class="text-gray-700 font-medium">Operational Efficiency</span>
              </div>
            </div>
            <div class="text-xs text-gray-500">
              Source:
              <a href="https://www.worldbank.org/en/businessready" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-700 font-medium">
                World Bank B-READY 2024
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stick Figures Visualization -->
    <section class="mb-32">
      <RegulatoryJobsStickFigures />
    </section>

    <!-- Scatterplot Explorer -->
    <section class="w-full">
      <div class="container max-w-4xl px-6 mb-12">
        <h2 class="font-serif text-3xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">Finding patterns</h2>
        <p class="text-lg md:text-xl text-gray-700 leading-relaxed max-w-2xl">
          Compare any two metrics to discover relationships between regulatory performance and real-world outcomes. Hover over a country to see its detailed breakdown across all
          eight business topics.
        </p>
      </div>
      <ScatterplotExplorer />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { GridApi, GridReadyEvent } from 'ag-grid-community';
import RegulatoryJobsStickFigures from './RegulatoryJobsStickFigures.vue';
import ScatterplotExplorer from './ScatterplotExplorer.vue';
import countryPillarData from '@/helpers/data/world-bank/country-pillar.json';
import countryPillarTopicData from '@/helpers/data/world-bank/country-pillar-topic.json';
import type { CountryPillarData } from '@/helpers/data/world-bank/types';

// Topic selection
const selectedTopic = ref('overall');

// Grid data and columns
const gridApi = ref<GridApi | null>(null);
const gridData = ref<any[]>(countryPillarData as CountryPillarData[]);

// Get field names based on selected topic
const getPillarFields = (topic: string) => {
  if (topic === 'overall') {
    return {
      pillar1: 'Pillar 1 Regulatory Framework',
      pillar2: 'Pillar 2 Public Services',
      pillar3: 'Pillar 3 Operational Efficiency',
    };
  } else {
    return {
      pillar1: `${topic} Pillar 1`,
      pillar2: `${topic} Pillar 2`,
      pillar3: `${topic} Pillar 3`,
    };
  }
};

// Update grid data when topic changes
watch(selectedTopic, (newTopic) => {
  if (newTopic === 'overall') {
    gridData.value = countryPillarData as CountryPillarData[];
  } else {
    // Transform topic data to match the structure
    gridData.value = countryPillarTopicData.map((item: any) => ({
      Economy: item.Economy,
      'Economy Code': item['Economy Code'],
      [`${newTopic} Pillar 1`]: item[`${newTopic} Pillar 1`],
      [`${newTopic} Pillar 2`]: item[`${newTopic} Pillar 2`],
      [`${newTopic} Pillar 3`]: item[`${newTopic} Pillar 3`],
    }));
  }
});

const onTopicChange = () => {
  // Force grid to refresh
  if (gridApi.value) {
    gridApi.value.refreshCells();
  }
};

// Get current pillar field names
const pillarFields = computed(() => getPillarFields(selectedTopic.value));

// Calculate min/max for each numeric field for heatmap
const pillar1Values = computed(() => gridData.value.map((d: any) => d[pillarFields.value.pillar1]).filter((v): v is number => v != null));
const pillar1Min = computed(() => Math.min(...pillar1Values.value));
const pillar1Max = computed(() => Math.max(...pillar1Values.value));

const pillar2Values = computed(() => gridData.value.map((d: any) => d[pillarFields.value.pillar2]).filter((v): v is number => v != null));
const pillar2Min = computed(() => Math.min(...pillar2Values.value));
const pillar2Max = computed(() => Math.max(...pillar2Values.value));

const pillar3Values = computed(() => gridData.value.map((d: any) => d[pillarFields.value.pillar3]).filter((v): v is number => v != null));
const pillar3Min = computed(() => Math.min(...pillar3Values.value));
const pillar3Max = computed(() => Math.max(...pillar3Values.value));

// Function to get heatmap color based on value (generic)
const getHeatmapColor = (value: number | null, min: number, max: number, colorScheme: 'orange' | 'green' | 'purple' = 'purple'): string => {
  if (value === null || min === max) {
    return '#f9fafb'; // bg-gray-50
  }

  // Normalize value to 0-1 range
  const normalized = (value - min) / (max - min);
  const intensity = Math.max(0, Math.min(1, normalized));

  let r, g, b;

  if (colorScheme === 'orange') {
    // Orange scale: light orange (low) to #f97316 (high) - matches stick figures
    // #f97316 = rgb(249, 115, 22)
    r = Math.round(255 - 6 * intensity); // 255 -> 249
    g = Math.round(247 - 132 * intensity); // 247 -> 115
    b = Math.round(237 - 215 * intensity); // 237 -> 22
  } else if (colorScheme === 'green') {
    // Green scale: light green (low) to #22c55e (high) - matches stick figures
    // #22c55e = rgb(34, 197, 94)
    r = Math.round(240 - 206 * intensity); // 240 -> 34
    g = Math.round(253 - 56 * intensity); // 253 -> 197
    b = Math.round(244 - 150 * intensity); // 244 -> 94
  } else {
    // Purple scale: light purple (low) to #a855f7 (high) - matches stick figures
    // #a855f7 = rgb(168, 85, 247)
    r = Math.round(250 - 82 * intensity); // 250 -> 168
    g = Math.round(245 - 160 * intensity); // 245 -> 85
    b = Math.round(255 - 8 * intensity); // 255 -> 247
  }

  return `rgb(${r}, ${g}, ${b})`;
};

// Cell renderer for just the visualization
const vizCellRenderer = (params: any) => {
  const pillar1 = params.data[pillarFields.value.pillar1];
  const pillar2 = params.data[pillarFields.value.pillar2];
  const pillar3 = params.data[pillarFields.value.pillar3];

  if (pillar1 == null || pillar2 == null || pillar3 == null) {
    return `<div class="p-2"></div>`;
  }

  // Scale values to 0-100 for positioning
  const lineWidth = 180;
  const lineY = 12; // Y position of the line
  const containerHeight = 40; // Increased height to accommodate labels
  const dotSize = 10;

  // Position dots on line (0-100 scale)
  const pillar1Pos = (pillar1 / 100) * lineWidth;
  const pillar2Pos = (pillar2 / 100) * lineWidth;
  const pillar3Pos = (pillar3 / 100) * lineWidth;

  // Fixed colors: orange for pillar 1, green for pillar 2, purple for pillar 3 - matches stick figures
  const pillar1Color = '#f97316'; // orange - matches stick figures
  const pillar2Color = '#22c55e'; // green - matches stick figures
  const pillar3Color = '#a855f7'; // purple - matches stick figures

  return `
    <div class="p-2 flex items-center justify-center" style="height: 100%;">
      <div class="relative flex-shrink-0" style="width: ${lineWidth}px; height: ${containerHeight}px;">
        <!-- Line -->
        <div style="position: absolute; top: ${lineY}px; left: 0; width: ${lineWidth}px; height: 2px; background: #d1d5db; border-radius: 1px;"></div>
        <!-- Pillar 1 dot (Regulatory Framework) - vertically aligned -->
        <div style="position: absolute; top: ${lineY - dotSize / 2}px; left: ${pillar1Pos - dotSize / 2}px; width: ${dotSize}px; height: ${dotSize}px; background: ${pillar1Color}; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.15); z-index: 2;"></div>
        <!-- Pillar 1 label -->
        <div style="position: absolute; top: ${lineY + 8}px; left: ${pillar1Pos}px; transform: translateX(-50%); font-size: 9px; color: #6b7280; white-space: nowrap; line-height: 1;">${Math.round(pillar1)}</div>
        <!-- Pillar 2 dot (Public Services) - vertically aligned -->
        <div style="position: absolute; top: ${lineY - dotSize / 2}px; left: ${pillar2Pos - dotSize / 2}px; width: ${dotSize}px; height: ${dotSize}px; background: ${pillar2Color}; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.15); z-index: 2;"></div>
        <!-- Pillar 2 label -->
        <div style="position: absolute; top: ${lineY + 8}px; left: ${pillar2Pos}px; transform: translateX(-50%); font-size: 9px; color: #6b7280; white-space: nowrap; line-height: 1;">${Math.round(pillar2)}</div>
        <!-- Pillar 3 dot (Operational Efficiency) - vertically aligned -->
        <div style="position: absolute; top: ${lineY - dotSize / 2}px; left: ${pillar3Pos - dotSize / 2}px; width: ${dotSize}px; height: ${dotSize}px; background: ${pillar3Color}; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.15); z-index: 2;"></div>
        <!-- Pillar 3 label -->
        <div style="position: absolute; top: ${lineY + 8}px; left: ${pillar3Pos}px; transform: translateX(-50%); font-size: 9px; color: #6b7280; white-space: nowrap; line-height: 1;">${Math.round(pillar3)}</div>
      </div>
    </div>
  `;
};

const gridColumns = computed(() => {
  const fields = pillarFields.value;

  return [
    {
      headerName: ' ',
      field: 'Economy',
      width: 180,
      pinned: 'left',
      sortable: true,
      cellStyle: { textAlign: 'right' },
    },
    {
      headerName: 'Are there laws in place?',
      field: fields.pillar1,
      width: 180,
      headerTooltip:
        'Measures the quality of the regulatory framework. Are the rules clear? Are good laws in place? This pillar evaluates the strength of the legal framework and the quality of regulations.',
      valueFormatter: ({ value }: any) => (value != null ? value.toFixed(2) : ''),
      type: 'numericColumn',
      cellStyle: (params: any) => {
        const value = params.value;
        return {
          backgroundColor: getHeatmapColor(value, pillar1Min.value, pillar1Max.value, 'orange'),
          textAlign: 'center',
          color: value != null && value > 80 ? '#f3f4f6' : 'inherit',
        };
      },
    },
    {
      headerName: 'Are the laws enforced?',
      field: fields.pillar2,
      width: 200,
      headerTooltip:
        'Measures the quality of public services. Are services helpful? This pillar evaluates transparency, support, and how well the system assists businesses in practice.',
      valueFormatter: ({ value }: any) => (value != null ? value.toFixed(2) : ''),
      type: 'numericColumn',
      cellStyle: (params: any) => {
        const value = params.value;
        return {
          backgroundColor: getHeatmapColor(value, pillar2Min.value, pillar2Max.value, 'green'),
          textAlign: 'center',
          color: value != null && value > 80 ? '#f3f4f6' : 'inherit',
        };
      },
    },
    {
      headerName: 'Does the system work?',
      field: fields.pillar3,
      width: 200,
      headerTooltip:
        'Measures real-world efficiency and practical effectiveness. Does it work in practice? This pillar evaluates speed, predictability, and the practical ease of doing business.',
      valueFormatter: ({ value }: any) => (value != null ? value.toFixed(2) : ''),
      type: 'numericColumn',
      cellStyle: (params: any) => {
        const value = params.value;
        return {
          backgroundColor: getHeatmapColor(value, pillar3Min.value, pillar3Max.value, 'purple'),
          textAlign: 'center',
          color: value != null && value > 80 ? '#f3f4f6' : 'inherit',
        };
      },
    },
    {
      headerName: '',
      width: 200,
      cellRenderer: vizCellRenderer,
      sortable: false,
      suppressMovable: true,
    },
  ];
});

const onGridReady = (params: GridReadyEvent) => {
  gridApi.value = params.api;
};
</script>

<style scoped>
:deep(.regulatory-jobs-grid .ag-header-cell-label) {
  justify-content: center;
  align-items: center;
  margin-bottom: -15px;
}

:deep(.regulatory-jobs-grid .ag-header-cell) {
  padding-bottom: 0;
}

/* Remove gap between last column and pinned right column */
:deep(.regulatory-jobs-grid .ag-pinned-right-cols-container) {
  border-left: none !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
  left: 0 !important;
}

:deep(.regulatory-jobs-grid .ag-pinned-right-header) {
  border-left: none !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
  left: 0 !important;
}

:deep(.regulatory-jobs-grid .ag-pinned-right-cols-viewport) {
  margin-left: 0 !important;
  padding-left: 0 !important;
}

:deep(.regulatory-jobs-grid .ag-body-horizontal-scroll) {
  border-left: none;
}

:deep(.regulatory-jobs-grid .ag-body-viewport) {
  border-right: none;
}

:deep(.regulatory-jobs-grid .ag-center-cols-container) {
  border-right: none;
}

/* Remove border from last cell in center columns */
:deep(.regulatory-jobs-grid .ag-center-cols-container .ag-row .ag-cell:last-child) {
  border-right: none !important;
}

:deep(.regulatory-jobs-grid .ag-center-cols-container .ag-header-cell:last-child) {
  border-right: none !important;
  padding-right: 0 !important;
  margin-right: 0 !important;
}

/* Force light gray text for high values (above 80) */
:deep(.regulatory-jobs-grid .ag-cell[style*='color: #f3f4f6']) {
  color: #f3f4f6 !important;
}

:deep(.regulatory-jobs-grid .ag-cell[style*='color:#f3f4f6']) {
  color: #f3f4f6 !important;
}
</style>
