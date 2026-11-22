#!/usr/bin/env python3
"""Deterministic Etsy opportunity scoring; scores are not proof of sales."""
import json
import math
import sys

WEIGHTS = {
    "buyer_demand": 25,
    "competition_opportunity": 20,
    "profit_potential": 20,
    "trend_sustainability": 10,
    "differentiation": 10,
    "production_feasibility": 10,
    "strategic_fit": 5,
}

def score(ratings):
    if not isinstance(ratings, dict):
        raise ValueError("ratings must be an object")
    missing = set(WEIGHTS) - set(ratings)
    if missing:
        raise ValueError(f"Missing factors: {sorted(missing)}")
    for key in WEIGHTS:
        value = ratings[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 10:
            raise ValueError(f"{key} must be a finite number from 0 to 10")
    return round(sum(ratings[k] * weight / 10 for k, weight in WEIGHTS.items()), 2)

def decision(value, compliant=True):
    if not isinstance(compliant, bool):
        raise ValueError("compliant must be a boolean")
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError("score must be a finite number from 0 to 100")
    if not compliant:
        return "SKIP: compliance gate"
    return "PRIORITIZE VALIDATION" if value >= 80 else "TEST" if value >= 65 else "WATCH" if value >= 50 else "SKIP"

def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("Usage: python scripts/score_opportunities.py input.json")
    with open(args[0], encoding="utf-8") as handle:
        data = json.load(handle, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"Invalid JSON number: {x}")))
    records = data if isinstance(data, list) else data.get("opportunities") if isinstance(data, dict) else None
    if not isinstance(records, list):
        raise ValueError("Input must be a list or an object with an opportunities list")
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("Each opportunity must be an object")
        value = score(item.get("ratings"))
        print(json.dumps({"name": item.get("name"), "score": value, "decision": decision(value, item.get("compliant", True))}, allow_nan=False))

if __name__ == "__main__":
    main()
