import { runVMC, classifyAudit } from "./qmc.js";

const byId = (id) => document.getElementById(id);
const form = byId("vmc-form");
const status = byId("vmc-status");
const button = byId("vmc-run");
const number = (id) => Number(byId(id).value);
const fmt = (x, decimals = 6) => x.toFixed(decimals);

function lineGraph(means, reference) {
  const svg = byId("energy-chart");
  svg.replaceChildren();
  const NS = "http://www.w3.org/2000/svg";
  function make(tag, attrs) {
    const node = document.createElementNS(NS, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
    svg.append(node);
    return node;
  }
  const values = [...means, reference, 0.5];
  const min = Math.min(...values), max = Math.max(...values);
  const pad = Math.max(0.01, (max - min) * 0.2);
  const low = min - pad, high = max + pad;
  const y = (v) => 210 - (v - low) / (high - low) * 180;
  make("line", { x1: 42, x2: 675, y1: 210, y2: 210, stroke: "#53627d" });
  make("line", { x1: 42, x2: 42, y1: 22, y2: 210, stroke: "#53627d" });
  make("line", { x1: 42, x2: 675, y1: y(reference), y2: y(reference), stroke: "#f4b76b", "stroke-dasharray": "7 5" });
  make("line", { x1: 42, x2: 675, y1: y(0.5), y2: y(0.5), stroke: "#8a98af", "stroke-dasharray": "3 5" });
  const points = means.map((v, i) => {
    const x = 42 + i * 633 / Math.max(1, means.length - 1);
    return x + "," + y(v);
  }).join(" ");
  make("polyline", { points, fill: "none", stroke: "#4bd4b2", "stroke-width": 2.8, "stroke-linejoin": "round" });
  const label = make("text", { x: 45, y: 16, fill: "#c8d2e2", "font-size": 13 });
  label.textContent = "Energy by consecutive sample block";
  const lower = make("text", { x: 10, y: 220, fill: "#9babc3", "font-size": 11 });
  lower.textContent = fmt(low, 2);
  const upper = make("text", { x: 10, y: 29, fill: "#9babc3", "font-size": 11 });
  upper.textContent = fmt(high, 2);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  button.disabled = true;
  status.textContent = "Computing locally…";
  // Allow the browser to draw the loading indicator before the synchronous sampler.
  setTimeout(() => {
    try {
      const output = runVMC({
        alpha: number("alpha"), samples: number("samples"),
        burnIn: number("burn-in"), proposal: number("proposal"), seed: number("seed")
      });
      byId("energy").textContent = fmt(output.energy);
      byId("uncertainty").textContent = "± " + fmt(output.standardError);
      byId("analytical").textContent = fmt(output.analyticEnergy);
      byId("acceptance").textContent = fmt(output.acceptanceRate * 100, 1) + "%";
      byId("x2").textContent = fmt(output.meanXSquared);
      byId("deviation").textContent = fmt(output.energy - output.analyticEnergy);
      byId("results").hidden = false;
      byId("download").disabled = false;
      byId("download").onclick = () => {
        const result = { ...output };
        const file = new Blob([JSON.stringify(result, null, 2) + "\n"], { type: "application/json" });
        const url = URL.createObjectURL(file);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = "vmc-results.json";
        anchor.click();
        setTimeout(() => URL.revokeObjectURL(url), 3000);
      };
      lineGraph(output.blockMeans, output.analyticEnergy);
      status.textContent = "Completed locally · reproducible seed " + output.seed;
    } catch (error) {
      byId("results").hidden = true;
      byId("download").disabled = true;
      status.textContent = "Input error: " + error.message;
    } finally {
      button.disabled = false;
    }
  }, 0);
});

byId("audit-form").addEventListener("submit", (event) => {
  event.preventDefault();
  try {
    const output = classifyAudit({
      primary: number("audit-primary"),
      secondary: number("audit-secondary"),
      critical: byId("audit-critical").checked,
      descriptor: byId("audit-descriptor").value
    });
    byId("audit-output").textContent = JSON.stringify(output, null, 2);
  } catch (error) {
    byId("audit-output").textContent = "Input error: " + error.message;
  }
});
