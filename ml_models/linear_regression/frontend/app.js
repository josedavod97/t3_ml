const form = document.querySelector("#prediction-form");
const areaInput = document.querySelector("#area");
const areaSlider = document.querySelector("#area-slider");
const sliderMin = document.querySelector("#slider-min");
const sliderMax = document.querySelector("#slider-max");
const sliderValue = document.querySelector("#slider-value");
const submitButton = document.querySelector("#submit-button");
const errorMessage = document.querySelector("#form-error");
const chartError = document.querySelector("#chart-error");
const result = document.querySelector("#result");
const resultPrice = document.querySelector("#result-price");
const resultArea = document.querySelector("#result-area");
const chart = document.querySelector("#model-chart");
const apiBaseUrl = window.CASAVALOR_API_URL;
const apiDocsLink = document.querySelector("#api-docs-link");

if (apiDocsLink) {
  apiDocsLink.href = `${apiBaseUrl}/docs`;
}
const currencyFormatter = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});
const areaFormatter = new Intl.NumberFormat("es-CO", {
  maximumFractionDigits: 1,
});
let chartData;

function formatBillions(value) {
  return new Intl.NumberFormat("es-CO", { maximumFractionDigits: 1 }).format(
    value / 1_000_000_000,
  );
}

function renderChart(selectedArea, selectedPrice) {
  if (!chartData) {
    return;
  }

  const points = chartData.points;
  const areas = points.map((point) => point.area_m2);
  const prices = points.map((point) => point.price_cop);
  const hasSelection = Number.isFinite(selectedArea) && selectedArea > 0;
  const predictedPrice = hasSelection
    ? selectedPrice ??
      chartData.slope_cop_per_m2 * selectedArea + chartData.intercept_cop
    : null;

  const trainingMinArea = Math.min(...areas);
  const trainingMaxArea = Math.max(...areas);
  let xMin = hasSelection
    ? Math.min(trainingMinArea, selectedArea)
    : trainingMinArea;
  let xMax = hasSelection
    ? Math.max(trainingMaxArea, selectedArea)
    : trainingMaxArea;
  const xPadding = Math.max((xMax - xMin) * 0.08, 2);
  if (hasSelection && selectedArea < trainingMinArea) {
    xMin -= xPadding;
  }
  if (hasSelection && selectedArea > trainingMaxArea) {
    xMax += xPadding;
  }

  const yValues = [
    ...prices,
    chartData.slope_cop_per_m2 * xMin + chartData.intercept_cop,
    chartData.slope_cop_per_m2 * xMax + chartData.intercept_cop,
  ];
  if (hasSelection) {
    yValues.push(predictedPrice);
  }
  let yMin = Math.min(...yValues);
  let yMax = Math.max(...yValues);
  const yPadding = Math.max((yMax - yMin) * 0.1, 50_000_000);
  yMin = Math.min(0, yMin - yPadding);
  yMax += yPadding;

  const width = 640;
  const height = 420;
  const margin = { top: 42, right: 24, bottom: 64, left: 82 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const x = (value) => margin.left + ((value - xMin) / (xMax - xMin)) * plotWidth;
  const y = (value) =>
    margin.top + ((yMax - value) / (yMax - yMin)) * plotHeight;
  const xTicks = Array.from({ length: 5 }, (_, index) =>
    xMin + ((xMax - xMin) * index) / 4,
  );
  const yTicks = Array.from({ length: 5 }, (_, index) =>
    yMax - ((yMax - yMin) * index) / 4,
  );
  const svg = [
    "<title>Área y precio de vivienda</title>",
    "<desc>Los puntos muestran los datos observados y la línea el ajuste de regresión.</desc>",
    `<rect width="${width}" height="${height}" fill="#ffffff"/>`,
    `<text class="svg-title" x="${width / 2}" y="22" text-anchor="middle">Precio de vivienda según su área</text>`,
  ];

  for (const tick of yTicks) {
    const position = y(tick);
    svg.push(
      `<line class="svg-grid" x1="${margin.left}" y1="${position}" x2="${width - margin.right}" y2="${position}"/>`,
      `<text class="svg-tick" x="${margin.left - 10}" y="${position + 4}" text-anchor="end">${formatBillions(tick)}</text>`,
    );
  }

  for (const tick of xTicks) {
    const position = x(tick);
    svg.push(
      `<line class="svg-grid" x1="${position}" y1="${margin.top}" x2="${position}" y2="${height - margin.bottom}"/>`,
      `<text class="svg-tick" x="${position}" y="${height - margin.bottom + 20}" text-anchor="middle">${areaFormatter.format(tick)}</text>`,
    );
  }

  svg.push(
    `<line class="svg-axis" x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${height - margin.bottom}"/>`,
    `<line class="svg-axis" x1="${margin.left}" y1="${height - margin.bottom}" x2="${width - margin.right}" y2="${height - margin.bottom}"/>`,
    `<text class="svg-axis-title" x="${margin.left + plotWidth / 2}" y="${height - 13}" text-anchor="middle">Área (m²)</text>`,
    `<text class="svg-axis-title" transform="translate(20 ${margin.top + plotHeight / 2}) rotate(-90)" text-anchor="middle">Precio (miles de millones COP)</text>`,
    `<line class="svg-regression" x1="${x(xMin)}" y1="${y(chartData.slope_cop_per_m2 * xMin + chartData.intercept_cop)}" x2="${x(xMax)}" y2="${y(chartData.slope_cop_per_m2 * xMax + chartData.intercept_cop)}"/>`,
  );

  for (const point of points) {
    svg.push(
      `<circle class="svg-observation" cx="${x(point.area_m2)}" cy="${y(point.price_cop)}" r="5"><title>${areaFormatter.format(point.area_m2)} m²: ${currencyFormatter.format(point.price_cop)}</title></circle>`,
    );
  }

  if (hasSelection) {
    const selectedX = x(selectedArea);
    const selectedY = y(predictedPrice);
    const labelX =
      selectedX > margin.left + plotWidth * 0.66
        ? selectedX - 204
        : selectedX + 10;
    const labelY = Math.max(margin.top + 6, selectedY - 34);
    const label = `${areaFormatter.format(selectedArea)} m² · ${currencyFormatter.format(predictedPrice)}`;
    svg.push(
      `<line class="svg-crosshair" x1="${selectedX}" y1="${selectedY}" x2="${selectedX}" y2="${height - margin.bottom}"/>`,
      `<line class="svg-crosshair" x1="${margin.left}" y1="${selectedY}" x2="${selectedX}" y2="${selectedY}"/>`,
      `<rect class="svg-selection-label" x="${labelX}" y="${labelY}" width="194" height="24" rx="6"/>`,
      `<text class="svg-selection-text" x="${labelX + 8}" y="${labelY + 16}">${label}</text>`,
      `<circle class="svg-selection" cx="${selectedX}" cy="${selectedY}" r="8"/>`,
    );
  }

  chart.innerHTML = svg.join("");
}

function updateSlider(area) {
  const min = Math.max(1, Math.min(70, Math.floor(area / 10) * 10));
  const max = Math.max(150, Math.ceil(area / 10) * 10);
  areaSlider.min = String(min);
  areaSlider.max = String(max);
  areaSlider.value = String(area);
  sliderMin.textContent = `${areaFormatter.format(min)} m²`;
  sliderMax.textContent = `${areaFormatter.format(max)} m²`;
  sliderValue.textContent = `${areaFormatter.format(area)} m²`;
}

function updateEstimate(area, price) {
  resultPrice.textContent = currencyFormatter.format(Math.round(price));
  resultArea.textContent = `Para una vivienda de ${areaFormatter.format(area)} m²`;
  result.hidden = false;
  renderChart(area, price);
}

function updateFromAreaInput() {
  const area = Number(areaInput.value);
  if (!Number.isFinite(area) || area <= 0) {
    result.hidden = true;
    renderChart(null, null);
    return;
  }

  updateSlider(area);
  if (chartData) {
    const price =
      chartData.slope_cop_per_m2 * area + chartData.intercept_cop;
    updateEstimate(area, price);
  }
}

areaInput.addEventListener("input", updateFromAreaInput);
areaSlider.addEventListener("input", () => {
  areaInput.value = areaSlider.value;
  updateFromAreaInput();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.hidden = true;
  errorMessage.textContent = "";

  if (!form.reportValidity()) {
    return;
  }

  submitButton.disabled = true;
  submitButton.querySelector("span").textContent = "Calculando...";

  try {
    const area = Number(areaInput.value);
    const response = await fetch(`${apiBaseUrl}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ area_m2: area }),
    });
    const data = await response.json();

    if (!response.ok) {
      const details = Array.isArray(data.detail)
        ? data.detail.map((error) => error.msg).join(" ")
        : data.detail;
      throw new Error(details || "No se pudo calcular la estimación.");
    }

    updateSlider(data.area_m2);
    updateEstimate(data.area_m2, data.estimated_price_cop);
  } catch (error) {
    errorMessage.textContent =
      error instanceof TypeError
        ? "No fue posible conectar con el servidor. Inténtalo de nuevo."
        : error.message;
    errorMessage.hidden = false;
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span").textContent = "Calcular estimación";
  }
});

async function loadChartData() {
  try {
    const response = await fetch(`${apiBaseUrl}/chart-data`);
    if (!response.ok) {
      throw new Error("No se pudieron cargar los datos de la gráfica.");
    }
    chartData = await response.json();
    chartError.hidden = true;
    updateFromAreaInput();
  } catch (error) {
    chartError.textContent =
      error instanceof TypeError
        ? "No fue posible conectar con el servidor para cargar la gráfica."
        : error.message;
    chartError.hidden = false;
  }
}

loadChartData();
