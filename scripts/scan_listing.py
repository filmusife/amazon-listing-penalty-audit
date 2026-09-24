#!/usr/bin/env python3
"""Deterministic scans for Amazon listing penalty audits.

Use after extracting title, bullets, ALTs, and search terms.
Do not treat this as a category overlay: it only counts length, language,
universal prohibited marketing terms, ASINs, and repeated measurements.

Example:
  python scan_listing.py --input extracted.json
  python scan_listing.py --title "Brand Widget, Navy" --st "widget mill kitchen"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from typing import Any

ASIN_RE = re.compile(r"\bB0[0-9A-Z]{8}\b", re.I)
CJK_RE = re.compile(r"[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]")
WORD_RE = re.compile(r"[A-Za-z0-9']+")
MEASURE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(inches?|inch|in|cm|mm|lbs?|oz|kg|g|watts?|w|volts?|v|db|cups?|ml|l)\b",
    re.I,
)

STOP_REPEAT = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "for",
    "to",
    "of",
    "with",
    "in",
    "on",
    "by",
}

PROHIBITED_PATTERNS = [
    (r"\bwarranty\b", "warranty"),
    (r"\bguarantee(?:d|s)?\b", "guarantee"),
    (r"money[-\s]?back", "money-back"),
    (r"\bbest\b", "best"),
    (r"#\s*1\b", "#1"),
    (r"\bnumber\s+one\b", "number one"),
    (r"super\s+silent", "super silent"),
    (r"ultra\s+quiet", "ultra quiet"),
    (r"100\s*%\s*(quality|guaranteed|satisfaction)", "100% guarantee"),
    (r"free\s+shipping", "free shipping"),
    (r"hot\s+item", "hot item"),
    (r"best\s+sellers?", "best seller"),
    (r"\bcoupon\b", "coupon"),
    (r"limited\s+time", "limited time"),
    (r"eco-friendly", "eco-friendly"),
    (r"environmentally\s+friendly", "environmentally friendly"),
    (r"anti-microbial", "anti-microbial"),
    (r"anti-bacterial", "anti-bacterial"),
]

MARKETPLACES = {
    "US": {"title_max_chars": 75, "st_max_bytes": 250, "listing_lang": "en"},
    "CA": {"title_max_chars": 75, "st_max_bytes": 250, "listing_lang": "en"},
    "UK": {"title_max_chars": 75, "st_max_bytes": 250, "listing_lang": "en"},
    "AU": {"title_max_chars": 75, "st_max_bytes": 250, "listing_lang": "en"},
    "DE": {"title_max_chars": None, "st_max_bytes": 250, "listing_lang": "de"},
    "FR": {"title_max_chars": None, "st_max_bytes": 250, "listing_lang": "fr"},
    "IT": {"title_max_chars": None, "st_max_bytes": 250, "listing_lang": "it"},
    "ES": {"title_max_chars": None, "st_max_bytes": 250, "listing_lang": "es"},
    "JP": {"title_max_chars": None, "st_max_bytes": 250, "listing_lang": "ja"},
}

UNIT_ALIASES = {
    "inch": "in",
    "inches": "in",
    "in": "in",
    "cm": "cm",
    "mm": "mm",
    "lb": "lb",
    "lbs": "lb",
    "oz": "oz",
    "kg": "kg",
    "g": "g",
    "watt": "w",
    "watts": "w",
    "w": "w",
    "volt": "v",
    "volts": "v",
    "v": "v",
    "db": "db",
    "cup": "cup",
    "cups": "cup",
    "ml": "ml",
    "l": "l",
}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items() if v is not None]
    return [str(value)]


def _join_fields(payload: dict[str, Any], keys: list[str]) -> str:
    parts: list[str] = []
    for key in keys:
        parts.extend(_as_list(payload.get(key)))
    return "\n".join(parts)


def _find_prohibited(text: str) -> list[dict[str, str]]:
    hits = []
    for pattern, label in PROHIBITED_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.I):
            hits.append({"term": label, "span": match.group(0)})
    return hits


def _repeat_words(title: str) -> list[dict[str, Any]]:
    counts: dict[str, int] = defaultdict(int)
    for word in WORD_RE.findall(title.lower()):
        if word in STOP_REPEAT:
            continue
        counts[word] += 1
    return [{"word": word, "count": count} for word, count in sorted(counts.items()) if count > 2]


def _measurements(text: str) -> dict[str, list[float]]:
    grouped: dict[str, set[float]] = defaultdict(set)
    for value, unit in MEASURE_RE.findall(text):
        grouped[UNIT_ALIASES.get(unit.lower(), unit.lower())].add(float(value))
    return {unit: sorted(values) for unit, values in grouped.items()}


def scan(payload: dict[str, Any]) -> dict[str, Any]:
    marketplace = str(payload.get("marketplace") or "US").upper()
    rules = MARKETPLACES.get(marketplace, MARKETPLACES["US"])
    title = str(payload.get("title") or "")
    bullets = _as_list(payload.get("bullets") or payload.get("bullet_points"))
    highlights = str(payload.get("item_highlights") or "")
    search_terms = str(payload.get("search_terms") or payload.get("st") or "")
    alts = payload.get("alts") or payload.get("alt") or {}
    attributes = payload.get("attributes") or {}

    alt_items = alts.items() if isinstance(alts, dict) else [(f"ALT{i+1}", v) for i, v in enumerate(_as_list(alts))]
    attr_text = _join_fields({"attributes": attributes}, ["attributes"])
    pdp_text = "\n".join([title, highlights, *bullets, attr_text, *[str(v) for _, v in alt_items]])

    title_chars = len(title)
    title_max = rules["title_max_chars"]
    st_bytes = len(search_terms.encode("utf-8"))
    st_max = rules["st_max_bytes"]

    alt_issues = []
    for key, value in alt_items:
        text = str(value or "")
        issue = {"key": key, "chars": len(text), "cjk": bool(CJK_RE.search(text)), "empty": not text.strip()}
        generic = bool(re.fullmatch(r"[A-Za-z ]{0,24}", text.strip())) and len(text.split()) <= 2
        issue["too_generic"] = generic and not issue["empty"]
        if rules["listing_lang"] == "en" and issue["cjk"]:
            issue["wrong_language"] = True
        elif rules["listing_lang"] != "ja" and issue["cjk"] and rules["listing_lang"] != "zh":
            issue["wrong_language"] = True
        else:
            issue["wrong_language"] = False
        if issue["empty"] or issue["cjk"] or issue["too_generic"] or issue["wrong_language"]:
            alt_issues.append(issue)

    measurements = _measurements(pdp_text)
    measurement_conflicts = {
        unit: values for unit, values in measurements.items() if len(values) >= 2
    }

    result = {
        "marketplace": marketplace,
        "listing_lang": rules["listing_lang"],
        "title": {
            "chars": title_chars,
            "max_chars": title_max,
            "over_limit": bool(title_max and title and title_chars > title_max),
            "repeat_words": _repeat_words(title),
        },
        "search_terms": {
            "bytes": st_bytes,
            "max_bytes": st_max,
            "over_limit": bool(search_terms) and st_bytes >= st_max,
            "asins": ASIN_RE.findall(search_terms),
            "prohibited": _find_prohibited(search_terms),
        },
        "pdp_prohibited": _find_prohibited(pdp_text),
        "alt_issues": alt_issues,
        "measurements": measurements,
        "measurement_conflicts": measurement_conflicts,
        "flags": [],
    }

    flags = result["flags"]
    if result["title"]["over_limit"]:
        flags.append("TITLE_OVER_LIMIT")
    if result["title"]["repeat_words"]:
        flags.append("TITLE_WORD_REPEATED")
    if result["search_terms"]["over_limit"]:
        flags.append("ST_OVER_BYTE_LIMIT")
    if result["search_terms"]["asins"]:
        flags.append("ST_CONTAINS_ASIN")
    if result["search_terms"]["prohibited"]:
        flags.append("ST_PROHIBITED_TERM")
    if result["pdp_prohibited"]:
        flags.append("PDP_PROHIBITED_TERM")
    if any(item.get("wrong_language") for item in alt_issues):
        flags.append("ALT_WRONG_LANGUAGE")
    if any(item.get("empty") for item in alt_issues):
        flags.append("ALT_EMPTY")
    if any(item.get("too_generic") for item in alt_issues):
        flags.append("ALT_TOO_GENERIC")
    if measurement_conflicts:
        flags.append("MEASUREMENT_CONFLICT_REVIEW")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan extracted Amazon listing fields")
    parser.add_argument("--input", help="JSON file; omit to read stdin when piped")
    parser.add_argument("--marketplace", default="US")
    parser.add_argument("--title", default="")
    parser.add_argument("--highlights", default="")
    parser.add_argument("--st", default="")
    parser.add_argument("--bullet", action="append", default=[])
    parser.add_argument("--alt", action="append", default=[], help="key:value")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input:
        return json.loads(PathRead(args.input))
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            return json.loads(raw)
    alts = {}
    for item in args.alt:
        if ":" not in item:
            raise SystemExit(f"ALT must be key:value, got {item!r}")
        key, value = item.split(":", 1)
        alts[key] = value
    return {
        "marketplace": args.marketplace,
        "title": args.title,
        "item_highlights": args.highlights,
        "bullets": args.bullet,
        "search_terms": args.st,
        "alts": alts,
    }


def PathRead(path: str) -> str:
    from pathlib import Path

    return Path(path).read_text(encoding="utf-8")


def self_test() -> int:
    coffee = scan(
        {
            "marketplace": "US",
            "title": "SHARDOR Super Silent Coffee Grinder, 2-Year Warranty, Black",
            "bullets": ["12 cups capacity", "63 dB quiet motor"],
            "search_terms": "burr mill B0FG6TJJGN best",
            "alts": {"MAIN": "咖啡研磨机", "IMG2": "coffee grinder"},
            "attributes": {"item_dimensions": "5 in x 10 in x 5 in"},
        }
    )
    assert "PDP_PROHIBITED_TERM" in coffee["flags"]
    assert "ST_CONTAINS_ASIN" in coffee["flags"]
    assert "ALT_WRONG_LANGUAGE" in coffee["flags"]
    assert coffee["title"]["over_limit"] is False

    apparel = scan(
        {
            "marketplace": "US",
            "title": "Brand Cotton Crew T-Shirt, Navy",
            "bullets": ["Chest 40 in", "100% cotton", "Machine wash cold"],
            "search_terms": "tee crewneck everyday shirt",
            "alts": {
                "MAIN": "Brand navy cotton crew t-shirt on white background",
            },
            "attributes": {"size": "M"},
        }
    )
    assert "PDP_PROHIBITED_TERM" not in apparel["flags"]
    assert "ST_CONTAINS_ASIN" not in apparel["flags"]
    assert apparel["search_terms"]["over_limit"] is False

    jp = scan(
        {
            "marketplace": "JP",
            "title": "ブランド Tシャツ ネイビー",
            "alts": {"MAIN": "ネイビーのコットンTシャツ"},
        }
    )
    assert "ALT_WRONG_LANGUAGE" not in jp["flags"]
    print("self-test passed")
    return 0


def main() -> int:
    args = parse_args()
    if args.self_test:
        return self_test()
    payload = payload_from_args(args)
    json.dump(scan(payload), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
