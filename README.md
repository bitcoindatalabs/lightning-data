# lightning-data

The canonical data repository for **[lightning.bitcoindatalabs.org](https://lightning.bitcoindatalabs.org)** (PlebDashboard-LN) and the Bitcoin Data Labs Lightning Network intelligence suite.

Mirrors the architectural pattern established by `orange-dev-data`, serving as the curated source of truth for network profiles, rankings, graph topologies, and periodic snapshots.

---

## Directory Structure

```
lightning-data/
├── README.md
├── .gitignore
├── data/
│   ├── node_rank.parquet           # Precomputed PlebRank & centrality rankings
│   ├── node_profile.parquet        # Enriched node metrics, aliases, capacities, channels
│   ├── channel_profile.parquet     # Channel capacities, fee policies, age, endpoints
│   ├── node_feature.parquet        # Specialized node features and attributes
│   ├── ln_node_types.json          # Curated node entity and role classifications
│   ├── featured_node.json          # Featured spotlight nodes
│   ├── graph/                      # Network graph topology datasets (Sigma.js)
│   │   ├── gall.json               # Full network graph
│   │   ├── ghigh.json              # Highway + freeway subgraphs
│   │   └── gfree.json              # Freeway-only backbone subgraphs
│   └── weekly_snapshots/           # Historical & latest network summaries
│       ├── latest.json             # Most recent weekly snapshot
│       └── weekly_YYYYMMDD.json    # Weekly historical archive
├── scripts/                        # Data generation, ETL, and sync scripts
└── metadata/                       # Schema definitions and data dictionaries
```

---

## Datasets Overview

| Dataset | Format | Refresh Cadence | Purpose |
|---|---|---|---|
| `node_rank.parquet` | Parquet | Weekly | Power rankings, centrality scores, percentile distributions |
| `node_profile.parquet` | Parquet | Weekly | Node explorer, search index, comprehensive node metrics |
| `channel_profile.parquet` | Parquet | Weekly | Channel explorer, fee analysis, liquidity metrics |
| `node_feature.parquet` | Parquet | Weekly | Connectivity, clustering coefficients, operational flags |
| `ln_node_types.json` | JSON | Continuous / Manual | Entity tagging (Exchanges, LSPs, Wallets, Routing Nodes) |
| `featured_node.json` | JSON | Daily / Weekly | Curated spotlight nodes for the homepage |
| `graph/*.json` | JSON | Weekly | High-performance graph visualization payloads |
| `weekly_snapshots/` | JSON | Weekly | Weekly wrap reporting and historical trend telemetry |

---

## Data Pipeline & Sync Workflow

1. **Analysis & Ingestion:** `LightningDS` computes centrality metrics, rankings, and channel topologies from raw gossip data into `Lightning/Data/parquet/`.
2. **Staging:** Data is published and versioned in `lightning-data`.
3. **Distribution (Option B):** Automated sync tasks push updated datasets into `plebdashboard-ln/data/` for zero-latency, local client delivery.
