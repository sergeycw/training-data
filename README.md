[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

# Training Data Pipeline

![Sync Status](https://github.com/sergeycw/training-data/actions/workflows/auto-sync.yml/badge.svg)

**Last successful sync:** 2026-04-12 03:49:41 UTC

Automated training data pipeline from [Intervals.icu](https://intervals.icu) for AI coaching analysis.
Built on the [Section 11 Protocol](https://github.com/CrankAddict/section-11).

## Structure

| Directory | Contents |
|-----------|----------|
| `context/` | AI context: protocol, athlete profile, training plan |
| `data/` | JSON data: snapshots, metrics, intervals |
| `scripts/` | Automation: sync, plan push |

## Data URLs

| File | Description | Link |
|------|-------------|------|
| `data/latest.json` | Current 7-day snapshot + derived metrics | [View](https://raw.githubusercontent.com/sergeycw/training-data/main/data/latest.json) |
| `data/history.json` | Longitudinal data (daily/weekly/monthly) | [View](https://raw.githubusercontent.com/sergeycw/training-data/main/data/history.json) |
| `data/intervals.json` | Per-interval data for structured sessions | [View](https://raw.githubusercontent.com/sergeycw/training-data/main/data/intervals.json) |

## Auto-Sync

Data syncs daily at 03:00 UTC (07:00 Tbilisi) via GitHub Actions. The pipeline pulls activities, wellness, and planned workouts from the Intervals.icu API, calculates derived metrics (ACWR, monotony, polarization, phase detection), and generates graduated alerts.

## AI Analysis

```
Analyze my training using these data files:
- Current: https://raw.githubusercontent.com/sergeycw/training-data/main/data/latest.json
- History: https://raw.githubusercontent.com/sergeycw/training-data/main/data/history.json
- Intervals: https://raw.githubusercontent.com/sergeycw/training-data/main/data/intervals.json
```

For best results, pair with the [Section 11 instruction set](https://github.com/CrankAddict/section-11).

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free for personal and non-commercial use. Attribution required.
