/**
 * 1D variational Monte Carlo for H = -1/2 d²/dx² + x²/2 (oscillator units).
 * Trial wavefunction: psi_alpha(x) = exp(-alpha*x²/2).
 * Metropolis target: |psi|²; local energy: alpha/2 + (1-alpha²)*x²/2.
 * Not diffusion Monte Carlo or a quantum-computer simulation.
 */
export function analyticEnergy(alpha) {
  if (!Number.isFinite(alpha) || alpha <= 0) throw new RangeError("alpha must be positive and finite");
  return (alpha + 1 / alpha) / 4;
}

function randomGenerator(seed) {
  let state = seed >>> 0;
  return function () {
    state = (state + 0x6D2B79F5) >>> 0;
    let t = state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function runVMC({ alpha = 0.85, samples = 10000, burnIn = 1000, proposal = 1.5, seed = 42 } = {}) {
  if (![alpha, proposal].every(Number.isFinite) || alpha <= 0 || alpha > 10 || proposal <= 0 || proposal > 10) {
    throw new RangeError("alpha and proposal must be finite numbers in (0, 10]");
  }
  if (!Number.isInteger(samples) || samples < 100 || samples > 1000000 ||
      !Number.isInteger(burnIn) || burnIn < 0 || burnIn > 1000000 ||
      !Number.isInteger(seed) || seed < 0 || seed > 0xffffffff) {
    throw new RangeError("Use 100–1,000,000 samples, 0–1,000,000 burn-in steps, and a 32-bit unsigned seed");
  }

  const random = randomGenerator(seed);
  const batches = Math.min(20, Math.floor(samples / 50));
  const batchSize = Math.floor(samples / batches);
  const blockMeans = [];
  let position = 0, accepted = 0, sumEnergy = 0, sumX2 = 0, blockSum = 0;
  for (let i = 0; i < burnIn + samples; i++) {
    const candidate = position + (random() * 2 - 1) * proposal;
    const logRatio = -alpha * (candidate * candidate - position * position);
    if (logRatio >= 0 || random() < Math.exp(logRatio)) {
      position = candidate;
      accepted++;
    }
    if (i < burnIn) continue;
    const index = i - burnIn;
    const x2 = position * position;
    const localEnergy = alpha / 2 + (1 - alpha * alpha) * x2 / 2;
    sumEnergy += localEnergy;
    sumX2 += x2;
    if (index < batches * batchSize) {
      blockSum += localEnergy;
      if ((index + 1) % batchSize === 0) {
        blockMeans.push(blockSum / batchSize);
        blockSum = 0;
      }
    }
  }
  const blockAverage = blockMeans.reduce((a, v) => a + v, 0) / batches;
  const varianceOfBlocks = blockMeans.reduce((a, v) => a + (v - blockAverage) ** 2, 0) / (batches - 1);

  return {
    alpha, samples, burnIn, proposal, seed,
    energy: sumEnergy / samples,
    standardError: Math.sqrt(varianceOfBlocks / batches),
    analyticEnergy: analyticEnergy(alpha),
    groundEnergy: 0.5,
    acceptanceRate: accepted / (burnIn + samples),
    meanXSquared: sumX2 / samples,
    blockMeans
  };
}

/** Local-only illustrative classification matching the legacy audit thresholds. */
export function classifyAudit({ primary, secondary, critical, descriptor }) {
  if (!Number.isFinite(primary) || !Number.isFinite(secondary)) throw new RangeError("Metrics must be finite");
  const alerts = [];
  if (primary > 25) alerts.push("Primary measurement exceeds 25");
  if (secondary > 12 || critical) alerts.push("Secondary measurement exceeds 12 or critical flag is active");
  if (/(DISCORDANT|ANOMALY|MUTANT|VIOLATION|FAIL|REJECT)/i.test(descriptor)) {
    alerts.push("Anomaly keyword detected in descriptor");
  }
  return {
    overall_urgency: critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE",
    total_alerts: alerts.length,
    alerts,
    mode: "Browser-only threshold demonstration; not a signed server dossier"
  };
}
