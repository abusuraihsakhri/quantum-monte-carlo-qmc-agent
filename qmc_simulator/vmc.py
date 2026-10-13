"""One-dimensional variational Monte Carlo for the harmonic oscillator.

In oscillator units (hbar = mass = omega = 1), the Gaussian trial state
psi_alpha(x) = exp(-alpha*x*x/2) produces
E_local(x) = alpha/2 + (1-alpha**2)*x*x/2.
Metropolis proposals target |psi_alpha|**2. This is VMC, not diffusion QMC.
"""
import math
import random
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class VMCResult:
    alpha: float
    samples: int
    burn_in: int
    proposal: float
    seed: int
    energy: float
    standard_error: float
    analytic_energy: float
    ground_energy: float
    acceptance_rate: float
    mean_x_squared: float


def run_vmc(
    alpha: float = 0.85,
    samples: int = 10_000,
    burn_in: int = 1_000,
    proposal: float = 1.5,
    seed: int = 42,
) -> VMCResult:
    """Estimate variational energy by a seeded random-walk Metropolis sampler.

    Standard error uses 20 (or fewer) non-overlapping contiguous batch means.
    These error bars are only indicative if batches remain autocorrelated.
    """
    if not all(math.isfinite(v) for v in (alpha, proposal)):
        raise ValueError("alpha and proposal must be finite")
    if not (0 < alpha <= 10 and 0 < proposal <= 10):
        raise ValueError("alpha and proposal must be in (0, 10]")
    if (type(samples) is not int or not 100 <= samples <= 1_000_000
            or type(burn_in) is not int or not 0 <= burn_in <= 1_000_000
            or type(seed) is not int or not 0 <= seed <= 0xFFFFFFFF):
        raise ValueError("invalid samples, burn_in or seed")

    rng = random.Random(seed)
    position = 0.0
    accepted = 0
    energy_sum = 0.0
    x2_sum = 0.0
    batch_count = min(20, samples // 50)
    batch_size = samples // batch_count
    batch_means = []
    batch_sum = 0.0

    for i in range(burn_in + samples):
        proposed = position + (rng.random() * 2 - 1) * proposal
        log_ratio = -alpha * (proposed * proposed - position * position)
        if log_ratio >= 0 or rng.random() < math.exp(log_ratio):
            position = proposed
            accepted += 1
        if i < burn_in:
            continue
        j = i - burn_in
        x2 = position * position
        local_energy = alpha / 2 + (1 - alpha * alpha) * x2 / 2
        energy_sum += local_energy
        x2_sum += x2
        if j < batch_count * batch_size:
            batch_sum += local_energy
            if (j + 1) % batch_size == 0:
                batch_means.append(batch_sum / batch_size)
                batch_sum = 0.0

    batch_avg = sum(batch_means) / batch_count
    batch_var = sum((v - batch_avg) ** 2 for v in batch_means) / (batch_count - 1)
    return VMCResult(
        alpha=alpha,
        samples=samples,
        burn_in=burn_in,
        proposal=proposal,
        seed=seed,
        energy=energy_sum / samples,
        standard_error=math.sqrt(batch_var / batch_count),
        analytic_energy=(alpha + 1 / alpha) / 4,
        ground_energy=0.5,
        acceptance_rate=accepted / (burn_in + samples),
        mean_x_squared=x2_sum / samples,
    )
