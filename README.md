# Quantum Monte Carlo QMC Agent

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Quantum Monte Carlo QMC Agent is an enterprise-grade analytical platform that combines post-quantary cryptography with zero-knowledge architecture. It provides:

- **Multi-Agent Consensus System**: Three specialized workers (InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker) evaluate tasks and produce consensus dossiers
- **Quantum Monte Carlo Simulation**: Variational & Diffusion Monte Carlo engine for computational physics applications
- **Financial Option Pricing**: Quantum amplitude estimation for option pricing and portfolio risk analysis
- **Tamper-Evident Audit Trail**: HMAC-SHA256 chained cryptographic audit logs
- **Zero-PHI Outbound Guard**: Active inspection blocking sensitive identifiers (SSNs, MRNs, phone numbers)

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Enrichment Suite**: Financial option pricing, portfolio risk analysis, and testing engines.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/quantum-monte-carlo-qmc-agent.git
cd quantum-monte-carlo-qmc-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# For development
pip install -e .
```

---

## 💻 CLI Quickstart & Usage

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task identifier | `TASK-2026-001` |
| `--target` | Target entity identifier | `KEY-TARGET-01` |
| `--primary` | Primary measurement value (float) | `28.5` |
| `--secondary` | Secondary metric value (float) | `14.2` |
| `--critical` | Flag for critical escalation | `False` |
| `--status` | Status descriptor | `DISCORDANT` |

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Parameter / observation metric | Required |
| `target_identifier` | Parameter / observation metric | Required |
| `primary_metric` | Parameter / observation metric | Required |
| `secondary_metric` | Parameter / observation metric | Optional |
| `is_critical_flag` | Parameter / observation metric | Optional |
| `status_descriptor` | Parameter / observation metric | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable in production to use a persistent HMAC key:

```bash
export AUDIT_SECRET_KEY="your-secure-random-key-here"
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

```bash
docker build -t quantum-monte-carlo-qmc-agent .
docker run -p 8000:8000 quantum-monte-carlo-qmc-agent
```

---

## 📁 Project Structure

```
quantum-monte-carlo-qmc-agent/
├── agents/                  # Core agent system
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── learning.py         # Bayesian calibration engine
│   ├── llm_factory.py      # LLM provider factory
│   ├── metrics.py          # Prometheus metrics collector
│   ├── models.py           # Pydantic data models
│   ├── streamer.py         # WebSocket telemetry streamer
│   ├── supervisor.py       # Multi-agent orchestrator
│   └── workers.py          # Specialized worker agents
├── qmc_simulator/          # QMC simulation engine
│   ├── agents.py           # QMC sub-agents
│   ├── cli.py              # QMC CLI interface
│   ├── engine.py           # Core QMC algorithms
│   ├── models.py           # QMC data models
│   └── server.py           # QMC FastAPI server
├── tests/                  # Test suite
├── web/                    # Web dashboard
├── cli.py                  # Main CLI entry point
├── simulator.py            # High-throughput simulator
├── enrichment.py           # Financial enrichment engines
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container definition
└── docker-compose.yml      # Multi-service orchestration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
