import { test } from "node:test";
import assert from "node:assert/strict";
import { analyticEnergy, classifyAudit, runVMC } from "../qmc.js";

test("harmonic-oscillator analytic variational bound", () => {
  assert.equal(analyticEnergy(1), 0.5);
  assert.ok(analyticEnergy(0.75) > 0.5);
});
test("zero-variance exact Gaussian ground state", () => {
  const v = runVMC({ alpha: 1, samples: 500, burnIn: 50, seed: 9 });
  assert.equal(v.energy, 0.5);
  assert.equal(v.standardError, 0);
  assert.equal(v.blockMeans.length, 10);
});
test("seed reproducibility and nontrivial MC estimate", () => {
  const p = { alpha: 0.8, samples: 20000, burnIn: 2000, seed: 20 };
  const a = runVMC(p);
  assert.deepEqual(runVMC(p), a);
  assert.ok(Math.abs(a.energy - a.analyticEnergy) < Math.max(0.03, 6 * a.standardError));
  assert.ok(a.acceptanceRate > 0 && a.acceptanceRate < 1);
});
test("reject nonfinite and abusive sampling parameters", () => {
  for (const param of [{ alpha: NaN }, { samples: 0 }, { samples: 1e8 },
                       { proposal: Infinity }, { seed: -1 }, { burnIn: -3 }]) {
    assert.throws(() => runVMC(param), RangeError);
  }
});
test("local audit threshold logic is bounded and explicit", () => {
  assert.equal(classifyAudit({ primary: 0, secondary: 0, critical: false, descriptor: "NOMINAL" }).total_alerts, 0);
  assert.equal(classifyAudit({ primary: 30, secondary: 13, critical: true, descriptor: "FAIL" }).total_alerts, 3);
  assert.throws(() => classifyAudit({ primary: NaN, secondary: 1, critical: false, descriptor: "" }), RangeError);
});
