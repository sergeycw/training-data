"""Push gym sessions from data/gym_garmin.json to Garmin Connect.

Each entry becomes a native Garmin strength workout (exercise, sets, reps,
weight, rest) and is scheduled on its date, so the watch (Forerunner 965)
guides the session and counts reps. Intervals.icu cannot do this: its
WeightTraining events reach Garmin without strength steps.

The full card (technique, video links, fallbacks) stays in the Intervals.icu
event with the same external_id; Garmin gets only the structure plus a short
cue per step.

Upsert: every workout we create carries "[<external_id>]" in its description.
Before upload, workouts with that marker are deleted (with their calendar
entries), so re-running the script replaces a session instead of duplicating it.

Needs tokens from scripts/garmin_login.py. Run:
    .venv-garmin/bin/python scripts/push_gym_garmin.py [--dry-run] [--from YYYY-MM-DD]
"""

import argparse
import json
from datetime import date
from pathlib import Path

from garminconnect import Garmin
from garminconnect.exercises import resolve
from garminconnect.workout import (
    StrengthWorkout,
    WorkoutSegment,
    create_strength_set,
    create_strength_timed_set,
    create_warmup_step,
)

TOKENSTORE = str(Path("~/.garminconnect").expanduser())
GYM_FILE = Path(__file__).resolve().parent.parent / "data" / "gym_garmin.json"
STRENGTH_SPORT = {"sportTypeId": 5, "sportTypeKey": "strength_training", "displayOrder": 5}
# Garmin has no field for this link; the marker in the description is the link.
CARD_HINT = "Полная карточка с техникой и видео - в Intervals.icu."


def marker(external_id: str) -> str:
    return f"[{external_id}]"


def build_steps(steps: list[dict]) -> list:
    out = []
    order = 1
    for s in steps:
        if "warmup_s" in s:
            step = create_warmup_step(s["warmup_s"], step_order=order)
            # The library builder takes no note; the step model has the field.
            step.description = s.get("note")
            out.append(step)
            order += 1
            continue

        entry = resolve(s["ex"])
        if entry is None:
            raise SystemExit(f"Нет в каталоге Garmin: {s['ex']!r} (смотри garminconnect.exercises.find)")
        common = dict(
            category=entry["category"],
            step_order=order,
            sets=s["sets"],
            rest_seconds=s["rest_s"],
            exercise_name=entry["exercise"],
            # kg 0 is a real prescription ("empty platform"); omit kg = bodyweight.
            weight_kg=s.get("kg"),
            description=s.get("note"),
        )
        if "time_s" in s:
            out.append(create_strength_timed_set(duration_seconds=s["time_s"], **common))
        else:
            out.append(create_strength_set(reps=s["reps"], **common))
        # A set block is a repeat group with two inner steps: 3 orders per block.
        order += 3
    return out


def estimate_seconds(steps: list[dict]) -> int:
    # Rough: 3 s per rep, rest after every set. Garmin shows it as plan time only.
    total = 0
    for s in steps:
        if "warmup_s" in s:
            total += s["warmup_s"]
            continue
        work = s.get("time_s", s.get("reps", 0) * 3)
        total += s["sets"] * (work + s["rest_s"])
    return total


def build_workout(entry: dict) -> StrengthWorkout:
    return StrengthWorkout(
        workoutName=entry["name"],
        estimatedDurationInSecs=estimate_seconds(entry["steps"]),
        description=f"{CARD_HINT} {marker(entry['external_id'])}",
        workoutSegments=[
            WorkoutSegment(
                segmentOrder=1,
                sportType=STRENGTH_SPORT,
                workoutSteps=build_steps(entry["steps"]),
            )
        ],
    )


def delete_previous(api: Garmin, external_id: str) -> int:
    tag = marker(external_id)
    old = [
        w for w in api.get_workouts(0, 200, sport_type_keys=["strength_training"])
        if tag in (w.get("description") or "")
    ]
    for w in old:
        api.delete_workout(w["workoutId"])
    return len(old)


def has_exercises(workout: dict) -> bool:
    def walk(steps: list[dict]) -> bool:
        return any(walk(s["workoutSteps"]) if "workoutSteps" in s else bool(s.get("exerciseName"))
                   for s in steps)
    return any(walk(seg.get("workoutSteps") or []) for seg in workout.get("workoutSegments") or [])


def unschedule_intervals_copies(api: Garmin, day: str, external_id: str) -> int:
    # Intervals.icu syncs its WeightTraining event to Garmin as a strength
    # workout with one empty "other" step: on the watch it is a second, useless
    # gym session. Take such copies off this day's calendar; the workout itself
    # stays in the library, Intervals.icu owns it. If push_plan.py runs after
    # this script, Intervals.icu can schedule the copy again: re-run this script.
    removed = 0
    for item in api.get_scheduled_workouts_by_period(day, day):
        w = item["workout"]
        if w["sportType"]["sportTypeKey"] != "strength_training":
            continue
        if marker(external_id) in (w.get("description") or "") or has_exercises(w):
            continue
        api.unschedule_workout(item["workoutScheduleId"])
        removed += 1
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="data/gym_garmin.json -> Garmin Connect")
    parser.add_argument("--dry-run", action="store_true", help="Собрать и показать, не отправлять")
    parser.add_argument("--from", dest="from_date", default=date.today().isoformat(),
                        help="Отправлять сессии с этой даты (по умолчанию сегодня)")
    args = parser.parse_args()

    entries = [e for e in json.loads(GYM_FILE.read_text()) if e["date"] >= args.from_date]
    if not entries:
        print(f"Нет сессий с {args.from_date}")
        return

    workouts = [(e, build_workout(e)) for e in entries]
    if args.dry_run:
        for e, w in workouts:
            print(f"{e['date']}  {e['name']}  ~{w.estimatedDurationInSecs // 60} мин")
            print(json.dumps(w.to_dict(), ensure_ascii=False, indent=1)[:2000])
        return

    api = Garmin()
    api.login(TOKENSTORE)
    for e, w in workouts:
        removed = delete_previous(api, e["external_id"])
        created = api.upload_strength_workout(w)
        api.schedule_workout(created["workoutId"], e["date"])
        copies = unschedule_intervals_copies(api, e["date"], e["external_id"])
        note = f", заменил {removed}" if removed else ""
        note += f", снял пустую копию Intervals.icu: {copies}" if copies else ""
        print(f"✅ {e['date']}  {e['name']}  workoutId {created['workoutId']}{note}")


if __name__ == "__main__":
    main()
