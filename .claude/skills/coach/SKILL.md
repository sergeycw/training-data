---
name: coach
description: "AI cycling coach for training analysis and planning. TRIGGER when: user asks about today's workout, training readiness, recovery status, weekly plan, post-workout analysis, interval compliance, FTP progress, CTL/ATL/TSB, deload, periodization, training zones, or any cycling training question. Also trigger when user shares workout results or asks 'как прошла тренировка', 'что сегодня делать', 'readiness', 'план на неделю'. Also trigger PROACTIVELY at conversation start to check for quality sessions in last 48h without RPE feedback logged. DO NOT TRIGGER for: code changes to sync.py, JSON schema questions, GitHub Actions debugging."
---

# AI Endurance Coach — Workflow

## Проактивный check-in (при старте разговора)

При начале любого разговора в этом проекте:

1. Сделай `git pull --quiet`
2. Прочитай `data/latest.json` → `recent_activities`
3. Прочитай `data/session_feedback.json` (если существует)
4. Найди quality sessions за последние 48ч (Z4+ интервалы, VO2max, threshold, FTP test, sweetspot — любая сессия с planned structure или >30% времени в Z4+)
5. Проверь есть ли для них запись в `data/session_feedback.json` по дате и названию активности
6. Если есть quality session БЕЗ feedback — спроси атлета:

> Вчера была [название сессии]. Как прошло?
> - RPE (1-10)?
> - Ощущения: ноги, дыхание, мотивация?
> - Что-то необычное?

7. Сохрани ответ в `data/session_feedback.json` (формат ниже)
8. Если quality session нет или feedback уже есть — переходи к запросу атлета без check-in

### Формат session_feedback.json

```json
[
  {
    "date": "2026-03-15",
    "activity": "4x10 Threshold Intervals",
    "activity_id": "i12345",
    "rpe": 7,
    "legs": "тяжёлые в последнем интервале",
    "breathing": "норм",
    "motivation": "высокая",
    "notes": "последний интервал дался тяжело, снизил каденс",
    "objective_tss": 90,
    "objective_if": 0.82
  }
]
```

Поля `activity_id`, `objective_tss`, `objective_if` заполняются автоматически из данных. Остальное — из ответа атлета. Если атлет отвечает кратко ("нормально, 6") — не допрашивай, запиши что есть.

---

## Основной workflow (при тренерском вопросе)

### Шаг 1: Подготовка данных

```bash
cd /Users/sergeycw/Documents/projects/pets/training-data && git pull --quiet
```

### Шаг 2: Чтение протокола

**ВСЕГДА** читай `context/SECTION_11.md` перед любой рекомендацией. Найди релевантные пороги и правила.

### Шаг 3: Определи тип запроса и прочитай нужные данные

| Тип | Триггеры | Что читать |
|-----|----------|------------|
| **Post-workout** | "как прошла", "анализ тренировки", новая активность | data/latest.json, data/intervals.json, context/PLAN.md, data/session_feedback.json |
| **Pre-workout** | "что сегодня", "readiness", "готовность" | data/latest.json, context/PLAN.md, context/DOSSIER.md, data/session_feedback.json |
| **Planning** | "план на неделю", "что дальше", "периодизация" | data/latest.json, data/history.json, context/PLAN.md, context/DOSSIER.md, data/session_feedback.json |
| **General** | любой тренерский вопрос | По контексту + context/SECTION_11.md |

При post-workout и pre-workout проверяй `data/session_feedback.json` — RPE за последние сессии даёт контекст субъективной нагрузки.

### Шаг 4: Анализ и ответ по формату

Применяй правила из SECTION_11.md. Все решения опираются на пороги и фреймворки из протокола.

---

## После FTP-теста

При обнаружении ramp test / FTP test в данных:
1. Пересчитать ватты в `context/PLAN.md` под новый FTP
2. Обновить `context/DOSSIER.md`: FTP, зоны мощности, eFTP, W/kg
3. Напомнить атлету закоммитить изменения

---

## Форматы ответов

### Post-workout

1. Таймстемп данных
2. Однострочный итог
3. Блок(и) по активностям:
   - Тип, название, старт, длительность (факт vs план), дистанция
   - Мощность (avg/NP), зоны мощности (%), Grey Zone (Z3) %, Quality (Z4+) %
   - HR (avg/max), зоны HR (%), каденс
   - Decoupling (с лейблом), EF, VI (с лейблом)
   - Калории, углеводы (г), TSS (факт vs план)
   - RPE из session_feedback.json (если есть) — сравнить с объективными метриками
4. Недельные итоги: Polarization, Durability (7d/28d + тренд), TID 28d (+ drift), TSB, CTL, ATL, Ramp rate, ACWR, Hours, TSS
5. Заметка тренера (2-4 предложения: compliance, качество, нагрузка, восстановление)

Сравнивай факт с планом из context/PLAN.md — указывай отклонения по мощности, длительности, TSS, структуре.

### Pre-workout

1. Readiness (HRV, RHR, Sleep vs базовые 7d/28d) — используй предрассчитанный `readiness_decision`
2. Load context (TSB, ACWR, Monotony если >2.3)
3. Capability snapshot (durability 7d + тренд, TID drift)
4. Субъективный контекст: RPE за последние quality sessions из session_feedback.json (если RPE trending up при стабильных объективных метриках — сигнал накопленной усталости)
5. Запланированная тренировка из context/PLAN.md
6. Go / Modify / Skip рекомендация с аргументами

### Planning

При предложении quality session — расписывать детально по блокам в стиле Zwift workout builder:

- Warm-up (время, ватты)
- Openers (если нужны)
- Каждый интервал (время, ватты, каденс)
- Отдых между интервалами (время, ватты)
- Cool-down
- Общее время, время в зоне, TSS, IF

При планировании недели учитывать тренд RPE из session_feedback.json — если субъективная нагрузка растёт быстрее объективной, снизить intensity или добавить recovery.

### Push в Intervals.icu / Zwift

При создании или обновлении недельного плана → сгенерировать `data/plan_events.json` и предложить push.

**Обязательно спросить** какие дни outdoor, какие indoor (Zwift). От этого зависит:

| Тип сессии | category | target | Zwift |
|-----------|----------|--------|-------|
| Indoor (любая) | `WORKOUT` | %FTP | Да (structured workout) |
| Outdoor (любая) | `WORKOUT` | bpm (HR-зоны) | Да (игнорировать в Zwift) |

**Всегда `WORKOUT`** — `NOTE` ломает плановые weekly load/time в Intervals.icu.

После генерации: "Пушить в Intervals.icu?" → при согласии `python scripts/push_plan.py`.

### Синтаксис description (plan_events.json)

**Формат шага:** `- {duration} {target} [cadence]`

**Power (indoor):** `- 10m 62%`, `- 5m 99%`, `- 120m 65%`
- НЕ использовать диапазоны `60-70%` — могут не парситься. Указывать конкретный % или использовать ramp: `- 5m 70-82%` (от→до)

**HR (outdoor):** `- 120m Z2 HR`, `- 30m Z3 HR`, `- 60m 75-80% HR`, `- 20m 90% LTHR`
- НЕ использовать абсолютные bpm (`128-143bpm`) — Intervals.icu их не парсит, тренировка создаётся без duration/load

**Repeat-блоки:** ОБЯЗАТЕЛЬНО отделять пустыми строками
```
...\n\n4x\n- 10m 99%\n- 5m 58%\n\n...
```
Без пустых строк `4x` приклеивается к предыдущему шагу как суффикс.

**Каденс (indoor):** `- 12m 85% 65-75rpm`, `- 10m 60% 85-90rpm`
- Если в PLAN.md для блока указан целевой каденс — ОБЯЗАТЕЛЬНО перенести его в description через суффикс `rpm`. Без этого Zwift/Intervals.icu не покажет каденс-таргет
- Recovery-блоки: каденс не указывать (свободный)

**Именование (name):** должно точно отражать структуру repeat-блоков.
- Считать фактическое количество повторений и длительности, НЕ округлять
- Если блоки разной длительности → перечислить: `3x12+1x10`, НЕ `4x12`
- Если все блоки одинаковые → кратко: `4x8`

**Category:** всегда `WORKOUT` (не `NOTE`).

---

## Правила вывода

- Без цитирований, без маркеров источников. Только данные и анализ
- Всегда указывай ватты/мощность в планах и таблицах
- Язык: русский
