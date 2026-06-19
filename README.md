# kazi-mcp

[![kazi-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/kazi-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/kazi-mcp)


[![PyPI](https://img.shields.io/pypi/v/kazi-mcp)](https://pypi.org/project/kazi-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCP server for Kenya labor market coordination — job matching, wage benchmarks,
skills gap analysis, informal sector registration, contract templates, and Kenya
Employment Act rights. Part of the East Africa coordination infrastructure suite.

**kazi** (Kiswahili) = work, job, task

## Tools (6)

| Tool | Description |
|------|-------------|
| `job_match` | Match worker skills to available job categories |
| `wage_benchmark` | Monthly wage ranges (entry/mid/senior) by job and county |
| `skills_gap_analysis` | Gap analysis + training pathways for target roles |
| `informal_sector_registry` | Register/lookup jua kali and informal workers |
| `contract_template` | Employment Act 2007-aligned contract templates |
| `labor_rights_query` | Kenya Employment Act rights by topic |

> **All data is DEMO (synthetic estimates).**

## Installation

```bash
pip install kazi-mcp
```

## Usage

```bash
kazi-mcp
```

### Claude Desktop

```json
{
  "mcpServers": {
    "kazi-mcp": {
      "command": "kazi-mcp"
    }
  }
}
```

## Coordination Infrastructure Suite

| Tool | Domain |
|------|--------|
| [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) | Payments |
| [bima-mcp](https://github.com/gabrielmahia/bima-mcp) | Insurance |
| [mkopo-mcp](https://github.com/gabrielmahia/mkopo-mcp) | Credit |
| [soko-mcp](https://github.com/gabrielmahia/soko-mcp) | Markets |
| [sifa-mcp](https://github.com/gabrielmahia/sifa-mcp) | Reputation |
| **kazi-mcp** | **Labor** |
| [wapimaji-mcp](https://github.com/gabrielmahia/wapimaji-mcp) | Water/Drought |

## License — MIT

> Not legal advice. All data is synthetic demonstration data only.
