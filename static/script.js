function addListeners() {
  for (const li of document.querySelectorAll("ul#sauna-dates li")) {
    li.addEventListener("click", drawTempDayChart);
  }
  for (const li of document.querySelectorAll("ul#pool-dates li")) {
    li.addEventListener("click", drawVibraDayChart);
  }
  document.getElementById("temp-now").addEventListener("click", updateTemp);
  document.getElementById("temp-seven-days").addEventListener("click", drawTempWeekChart);
  document.getElementById("vibra-now").addEventListener("click", updateVibra);
  document.getElementById("vibra-seven-days").addEventListener("click", drawVibraWeekChart);
}

async function updateTemp() {
  document.getElementById("temp-now").innerText = "...";
  const resp = await fetch("/api/sauna/now");
  const latestTemp = await resp.json();
  document.getElementById("temp-now").innerText = latestTemp;
}

async function updateVibra() {
  document.getElementById("vibra-now").innerText = "...";
  const resp = await fetch("/api/pool/now");
  const latestVibra = await resp.json();
  document.getElementById("vibra-now").innerText = latestVibra
    ? "In Benutzung"
    : "Nicht in Benutzung";
}

function drawTempChart(labels, temperatures) {
  resetCanvas("temp-chart");
  var ctx = document.getElementById("temp-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: temperatures,
          backgroundColor: ["rgba(255, 99, 132, 0.2)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      responsive: true,
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      legend: {
        display: false,
      },
    },
  });
}

function drawVibraChart(labels, vibrations) {
  resetCanvas("vibra-chart");
  var ctx = document.getElementById("vibra-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          data: vibrations,
          backgroundColor: ["rgba(255, 99, 132, 0.2)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      responsive: true,
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      legend: {
        display: false,
      },
    },
  });
}

async function drawTempWeekChart() {
  const result = await fetch("/api/sauna/week");
  const rawData = await result.json();
  const [times, temps] = groupAndAggregate({
    dataList: rawData,
    windowSize: 30 * 60,
    aggregation: "avg",
  });

  drawTempChart(times, temps);
}

async function drawVibraWeekChart() {
  const result = await fetch("/api/pool/week");
  const rawData = await result.json();
  const [times, vibrations] = groupAndAggregate({
    dataList: rawData,
    windowSize: 30 * 60,
    aggregation: "min",
  });
  drawVibraChart(times, vibrations);
}

function resetCanvas(id) {
  document.getElementById(id).remove(); // this is my <canvas> element
  document.getElementById(id + "-container").innerHTML = `<canvas id="${id}"></canvas>`;
}

async function drawTempDayChart(event) {
  const day = event.target.innerText;
  const result = await fetch(`/api/sauna/day?day=${day}`);
  const rawData = await result.json();
  const [times, temps] = groupAndAggregate({
    dataList: rawData,
    windowSize: 6 * 60,
    aggregation: "avg",
  });
  drawTempChart(times, temps);
}

async function drawVibraDayChart(event) {
  const day = event.target.innerText;
  const result = await fetch(`/api/pool/day?day=${day}`);
  const rawData = await result.json();
  const [times, vibrations] = groupAndAggregate({
    dataList: rawData,
    windowSize: 6 * 60,
    aggregation: "min",
  });
  drawVibraChart(times, vibrations);
}

async function fillTempInfo(data) {
  document.getElementById("temp-now").innerText = data.last_temperature;

  let listContent = "";
  for (const saunaDate of data.sauna_dates) {
    listContent += `<li><span class="hover-button">${saunaDate}</span></li>`;
  }
  if (listContent !== "") {
    document.getElementById("sauna-dates").innerHTML = listContent;
  }
}

async function fillVibraInfo(data) {
  document.getElementById("vibra-now").innerText = data.last_vibration
    ? "In Benutzung"
    : "Nicht in Benutzung";

  let listContent = "";
  for (const poolDate of data.pool_dates) {
    listContent += `<li><span class="hover-button">${poolDate}</span></li>`;
  }
  if (listContent !== "") {
    document.getElementById("pool-dates").innerHTML = listContent;
  }
}

async function main() {
  const result = await fetch("/api/doehlen-info");
  const data = await result.json();
  await fillTempInfo(data);
  await fillVibraInfo(data);
  addListeners();

  try {
    await drawTempWeekChart();
    await drawVibraWeekChart();
  } catch (error) {
    console.error(error);
  }
}

main();
