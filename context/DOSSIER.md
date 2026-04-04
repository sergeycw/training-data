# Athlete Training Dossier & Performance Roadmap

**Dossier Version:** v1.0
**Protocol Compatibility:** Section 11 v11.6+
**Date:** 2026-03-17
**Primary Source Systems:** Intervals.icu | Garmin

---

## 1. Athlete Overview

### Athlete Profile

| Field | Value |
|-------|-------|
| Name | Sergey |
| Age | 35-40 |
| Height | — |
| Current Weight | 70.0 kg |
| Target Weight | — |
| Location | — |

### Sport Focus

| Type | Description |
|------|-------------|
| Primary | Cycling (Road / Gravel) |
| Secondary | Trail Running / Ultra-Trail (опыт) |

### Training Background

Prior sport: running (6 days/week, 3 quality sessions). Structure: Wed threshold (ПАНО), Fri short intervals, Sat long with progression/inserts. All absorbed well. Transitioned to cycling — concentric load allows equal or higher quality session density. Data confirms: 3-4 hard days/week sustained in Build phase without recovery issues.

**Running achievements:** полумарафон — 1:19:45; успешный опыт трейлраннинга, ультратрейлов, спидхайкинг-марафона. Высокая аэробная база и выносливость, подтверждённые на длинных дистанциях. Учитывать при планировании: атлет хорошо переносит объём и длительную работу, имеет развитую аэробную систему от бегового бэкграунда.

### Goals

| Goal | Target Date |
|------|-------------|
| Reach 4+ W/kg | 2026 |
| Increase FTP from 263W to 280W+ | 2026 |
| Optimize weight (currently ~70 kg) | 2026 |

**Current Phase:** Build (threshold + VO2max development)
**Training Style:** High-volume polarized (~12h/week)

---

## 2. Equipment & Environment

### Indoor Training Setup

| Component | Details |
|-----------|---------|
| Platform | Zwift |
| Sensors | Smart trainer (power), HRM |

### Outdoor Setup

| Component | Details |
|-----------|---------|
| Bike | Gravel bike (no power meter) |
| HRM | Garmin |

**Note:** Outdoor rides use HR-based intensity guidance only (no power data).

---

## 3. Training Schedule & Framework

### Weekly Volume Target

**Baseline:** 12 hours/week (± 2 hours)
**Peak phases:** Up to 15 hours (requires RI ≥ 0.8, HRV within 10%)

### Microcycle Principles

- **Quality sessions:** 2-3 per week in Build phase (minimum 2, do not drop to 1 except taper/recovery)
- **Long ride:** 1 per week (Saturday), counts as quality when >3h or includes structured work
- **Hard:Easy ratio:** hard day → easy day or rest before next hard day
- **Athlete tolerance:** 3 hard days/week well-absorbed (confirmed by running background + cycling data)

### Normal Weekly Schedule

| Day | Primary Session | Duration |
|-----|-----------------|----------|
| Monday | Endurance Z2 (Zwift) | 1.5-2h |
| Tuesday | VO2max intervals (Zwift) | 1-1.5h |
| Wednesday | Endurance Z2 (Zwift) | 1.5-2h |
| Thursday | Threshold / Sweetspot (Zwift) | 1-1.5h |
| Friday | Recovery or Rest | 0-1h |
| Saturday | Long ride (outdoor gravel or Zwift) | 2.5-4h |
| Sunday | Endurance Z2 (Zwift or outdoor) | 1.5-2.5h |

### Session Details

| Session Type | Target Power/HR | Duration | Purpose |
|--------------|-----------------|----------|---------|
| VO2Max | 279-316W (106-120% FTP) | 1-1.5h | Aerobic capacity |
| Threshold | 239-276W (91-105% FTP) | 1-1.5h | FTP development |
| Sweetspot | 221-255W (84-97% FTP) | 1.5-2h | Time at intensity |
| Endurance | 148-197W (56-75% FTP) | 1.5-4h | Aerobic base |
| Recovery | <145W (<55% FTP) | 0.5-1h | Active recovery |

### Recovery Protocol

**Recovery Triggers (Auto-Deload):**
- HRV ↓ > 20% → Easy day, Z1-Z2 only
- RHR ↑ ≥ 5 bpm → Flag fatigue, reduce volume 30%
- Feel ≥ 4 → Reduce volume 30-40%
- Two+ triggers → Full rest day

---

## 4. Performance Metrics

### Current Power Zones (FTP = 263W)

| Zone | % of FTP | Power (W) | Notes |
|------|----------|-----------|-------|
| Z1 | 0-55% | 0-145 | Active Recovery |
| Z2 | 56-75% | 148-197 | Endurance (Base) |
| Z3 | 76-90% | 200-237 | Tempo |
| Z4 | 91-105% | 239-276 | Threshold |
| Z5 | 106-120% | 279-316 | VO2max |
| Z6 | 121-150% | 318-395 | Anaerobic |
| Z7 | 151%+ | 397+ | Neuromuscular |
| SS | 84-97% | 221-255 | Sweetspot |

**Current FTP:** 263W (Indoor: 263W)
**Max HR:** 176 bpm
**Threshold HR (LTHR):** 160 bpm
**Resting HR:** 44 bpm
**HRV:** 45
**eFTP:** 263W
**W':** 21.1 kJ
**P-max:** 799W

### Current Fitness Markers

Актуальные фитнес-метрики (CTL, ATL, TSB, ACWR, W/kg) → `data/latest.json` → `current_status` + `derived_metrics`

---

## 5. Nutrition / Fueling

*To be filled in*

---

## 6. Adaptation & Current Focus

### Current Adaptation Focus

- [ ] Raise FTP from 263W toward 280W+ (4+ W/kg target)
- [ ] Maintain polarized distribution (80/20)
- [ ] Improve VO2max power (target 290W+ intervals)
- [ ] Optimize weight from ~70 kg toward 67-68 kg (without compromising power)

### Next-Phase Options

Transition to outdoor season as weather improves. Use HR for outdoor intensity guidance since no outdoor power meter.

---

## 7. Outdoor Transition Plan

### General Rules

- Outdoor rides replace indoor 1:1
- HR < 136 bpm (~85% of LTHR) = aerobic
- Use HR to guide intensity (no outdoor power meter)
- Indoor power sessions remain on Zwift for structured work

---

## 8. Long-Term Performance Roadmap

### Primary Objective

Reach 4+ W/kg by end of 2026 season. Two levers: raise FTP (263W → 280W+) and optimize weight (~70 kg → 67-68 kg).

### Progression Overview

| Year | Focus | FTP Target | W/kg Target |
|------|-------|------------|-------------|
| 2026 | Threshold + VO2max development, weight optimization | 280W+ | 4.0+ |

---

## Data Mirror Configuration

### GitHub Connector

**Repo:** `sergeycw/training-data` (private, connected via GitHub integration)

Files: `data/latest.json`, `data/history.json`, `data/intervals.json`, `data/ftp_history.json`, `context/DOSSIER.md`, `context/SECTION_11.md`

---

## Protocol Reference

**Protocol Location:** `context/SECTION_11.md` (in this repo)

---

## Changelog

### v1.1 (2026-03-17)
- FTP updated: 243W → 263W (Ramp Test 17.03)
- Power zones recalculated for FTP 263W
- Fitness markers updated from latest.json
- Weight updated to 70.0 kg, W/kg = 3.76

### v1.0 (2026-03-15)
- Initial dossier creation
