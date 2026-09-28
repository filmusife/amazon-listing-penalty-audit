#!/usr/bin/env python3
"""Deterministic scans for Amazon listing penalty audits.

Upgraded with:
- Intelligent 3D dimension parsing (no false positives for L x W x H)
- Context-aware prohibited word filtering (whitelisting 'for best results', etc.)
- High-risk EPA/FIFRA pesticide & antimicrobial claim detection
- Registered trademark & IP brand trap detection (Velcro, Thermos, PopSockets, etc.)
- 0-100 Quantified Listing Health Score & Risk Level classification

Example:
  python scan_listing.py --input extracted.json
  python scan_listing.py --title "Brand Widget, Navy" --st "widget mill kitchen"
  python scan_listing.py --self-test
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

# 3D Dimensions: e.g., 4.7"L x 4.7"W x 6.77"H or 10 x 5 x 2 inches
DIMENSION_3D_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:\"|in|inch|inches|cm|mm)?\s*[L|l|W|w|H|h|D|d]?\s*(?:x|×|\*)\s*"
    r"(\d+(?:\.\d+)?)\s*(?:\"|in|inch|inches|cm|mm)?\s*[L|l|W|w|H|h|D|d]?\s*(?:x|×|\*)\s*"
    r"(\d+(?:\.\d+)?)\s*(?:\"|in|inch|inches|cm|mm)?\s*[L|l|W|w|H|h|D|d]?\s*"
    r"(\"|in|inch|inches|cm|mm)?",
    re.I,
)

# Scalar measurements:
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

# General prohibited marketing claims with context awareness
# 'best' is whitelisted for phrases like 'for best results', 'best before', 'best practices'
PROHIBITED_PATTERNS = [
    (r"\bwarranty\b", "warranty"),
    (r"\bguarantee(?:d|s)?\b", "guarantee"),
    (r"money[-\s]?back", "money-back"),
    (r"(?<!for\s)(?<!at\sits\s)\bbest\b(?!\s+(?:results|before|practices|served|paired|use|effort))", "best"),
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
]

# High-risk EPA/FIFRA pesticide / antimicrobial claims (automatic suppression risk in US)
EPA_PESTICIDE_PATTERNS = [
    (r"\banti-?microbial\b", "anti-microbial (EPA pesticide claim trigger)"),
    (r"\banti-?bacterial\b", "anti-bacterial (EPA pesticide claim trigger)"),
    (r"\bmold-?resistant\b", "mold-resistant (EPA pesticide claim trigger)"),
    (r"\bmildew-?resistant\b", "mildew-resistant (EPA pesticide claim trigger)"),
    (r"\bdisinfect(?:ing|ant|s)?\b", "disinfectant (EPA pesticide claim trigger)"),
    (r"\bfungicidal\b", "fungicidal (EPA pesticide claim trigger)"),
    (r"\bgermicidal\b", "germicidal (EPA pesticide claim trigger)"),
    (r"\binsect-?repell(?:ent|ing|er|ents)?\b", "insect-repellent (EPA pesticide claim trigger)"),
    (r"\brepels?\s+(?:insects?|bugs?|mosquitoes?|pests?)\b", "repels pests (EPA pesticide claim trigger)"),
    (r"\bpesticide(?:s)?\b", "pesticide (EPA pesticide claim trigger)"),
    (r"\bsteriliz(?:e|ing|er|ation)\b", "sterilizer (EPA/medical claim trigger)"),
]

# High-risk registered trademark traps that cause automated IP infringement takedowns
TRADEMARK_PATTERNS = [
    (r"\bvelcro\b", "Velcro (use 'hook and loop' instead)"),
    (r"\bthermos\b", "Thermos (use 'insulated tumbler/bottle' instead)"),
    (r"\bpopsockets?\b", "PopSockets (use 'expandable phone grip' instead)"),
    (r"\bpost-?its?\b", "Post-it (use 'sticky notes' instead)"),
    (r"\bgore-?tex\b", "Gore-Tex (use 'waterproof breathable membrane' instead)"),
    (r"\bband-?aids?\b", "Band-Aid (use 'adhesive bandage' instead)"),
    (r"\brollerblades?\b", "Rollerblade (use 'inline skates' instead)"),
    (r"\bfrisbees?\b", "Frisbee (use 'flying disc' instead)"),
    (r"\bchapsticks?\b", "ChapStick (use 'lip balm' instead)"),
    (r"\bcrock-?pots?\b", "Crock-Pot (use 'slow cooker' instead)"),
    (r"\bziplocs?\b", "Ziploc (use 'zipper storage bag' instead)"),
    (r"\bq-?tips?\b", "Q-tips (use 'cotton swabs' instead)"),
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
    "\"": "in",
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


def _find_patterns(text: str, patterns: list[tuple[str, str]]) -> list[dict[str, str]]:
    hits = []
    for pattern, label in patterns:
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


def _extract_dimensions_and_measurements(text: str) -> tuple[list[tuple[float, float, float, str]], dict[str, list[float]], dict[str, Any]]:
    """Extract 3D dimensions without mistaking L x W x H as scalar conflicts."""
    dimensions_3d: list[tuple[float, float, float, str]] = []
    mask_spans: list[tuple[int, int]] = []

    for match in DIMENSION_3D_RE.finditer(text):
        d1, d2, d3, unit = match.groups()
        normalized_unit = UNIT_ALIASES.get((unit or "in").lower(), "in")
        dims = (float(d1), float(d2), float(d3), normalized_unit)
        dimensions_3d.append(dims)
        mask_spans.append(match.span())

    # Create masked text so 3D dimension numbers are not re-extracted as scalar conflicts
    text_chars = list(text)
    for start, end in mask_spans:
        for i in range(start, end):
            text_chars[i] = " "
    masked_text = "".join(text_chars)

    grouped_scalars: dict[str, set[float]] = defaultdict(set)
    for value, unit in MEASURE_RE.findall(masked_text):
        normalized_unit = UNIT_ALIASES.get(unit.lower(), unit.lower())
        grouped_scalars[normalized_unit].add(float(value))

    scalar_measurements = {unit: sorted(values) for unit, values in grouped_scalars.items()}

    # Conflict check
    conflicts: dict[str, Any] = {}
    
    # 3D dimension conflicts (if multiple distinct 3D dimensions exist)
    if len(dimensions_3d) >= 2:
        # Normalize by sorting the 3 dimensions (ignoring axis order discrepancies like 5x10x5 vs 10x5x5)
        canonical_dims = {
            tuple(sorted([d[0], d[1], d[2]])) + (d[3],) for d in dimensions_3d
        }
        if len(canonical_dims) > 1:
            conflicts["3D_dimensions"] = [
                f"{d[0]}x{d[1]}x{d[2]} {d[3]}" for d in dimensions_3d
            ]

    # Scalar conflicts (e.g. 12 cups vs 3 cups, 60 dB vs 63 dB, 70g vs 100g)
    for unit, values in scalar_measurements.items():
        if len(values) >= 2:
            conflicts[unit] = values

    return dimensions_3d, scalar_measurements, conflicts


def calculate_health_score(result: dict[str, Any]) -> dict[str, Any]:
    """Calculate 0-100 Listing Health Score and penalty risk level."""
    score = 100
    deductions: list[dict[str, Any]] = []

    # 1. Critical Policy & IP Violations (-15 to -20 pts)
    if result.get("epa_pesticide_claims"):
        score -= 20
        deductions.append({"issue": "EPA/FIFRA 未申报杀菌/农药高危词 (可能直接下架)", "points": -20})
    if result.get("trademark_violations"):
        score -= 20
        deductions.append({"issue": "注册商标侵权风险 (如 Velcro, Thermos 等通用化误用)", "points": -20})
    if "ST_CONTAINS_ASIN" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Search Terms 违规填入 ASIN", "points": -15})
    if "ST_PROHIBITED_TERM" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Search Terms 含有保修/竞品/违禁词", "points": -15})
    if "PDP_PROHIBITED_TERM" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Listing 含有保修/保证/绝对化夸大禁用词", "points": -15})

    # 2. Major Consistency & Operational Issues (-10 pts)
    if "TITLE_OVER_LIMIT" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "标题超出站点字符数限制 (美国站推荐 <=75 字符)", "points": -10})
    if "ST_OVER_BYTE_LIMIT" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "Search Terms 超出 250 字节限制", "points": -10})
    if "MEASUREMENT_CONFLICT_REVIEW" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "规格参数打架 (多处尺寸/容量/功率不一致)", "points": -10})
    if "ALT_WRONG_LANGUAGE" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "图片 ALT 错语言 (如英语站出现中文 ALT)", "points": -10})
    if "ALT_EMPTY" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "图片 ALT 存在空白缺失", "points": -10})

    # 3. Minor / Warning Issues (-5 pts)
    if "TITLE_WORD_REPEATED" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "标题单词重复超过 2 次", "points": -5})
    if "ALT_TOO_GENERIC" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "图片 ALT 过于空泛 (词数 <= 2)", "points": -5})

    score = max(0, min(100, score))

    if score >= 85:
        level = "LOW_RISK_HEALTHY"
        label = "健康良好 (A级: 85-100分 - 政策合规，仅需做发现层优化)"
    elif score >= 70:
        level = "MODERATE_RISK"
        label = "中度风险 (B级: 70-84分 - 存在体验瑕疵或检索权重减分)"
    elif score >= 50:
        level = "HIGH_RISK"
        label = "高危受限 (C级: 50-69分 - 权重受抑，多项指标违背政策)"
    else:
        level = "CRITICAL_RISK"
        label = "极度危险 (D级: 0-49分 - 面临静默降权或下架红线，立即整改)"

    return {
        "score": score,
        "level": level,
        "label": label,
        "deductions": deductions,
    }


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
    # Filter out dedicated warranty fields (which are legally allowed in backend attributes)
    marketing_attributes = {
        k: v for k, v in attributes.items()
        if not any(w in k.lower() for w in ["warranty", "guarantee"])
    }
    attr_text = _join_fields({"attributes": marketing_attributes}, ["attributes"])
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

    dims_3d, measurements, measurement_conflicts = _extract_dimensions_and_measurements(pdp_text)

    pdp_prohibited = _find_patterns(pdp_text, PROHIBITED_PATTERNS)
    st_prohibited = _find_patterns(search_terms, PROHIBITED_PATTERNS)
    epa_claims = _find_patterns(pdp_text, EPA_PESTICIDE_PATTERNS)
    trademark_hits = _find_patterns(pdp_text, TRADEMARK_PATTERNS)

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
            "prohibited": st_prohibited,
        },
        "pdp_prohibited": pdp_prohibited,
        "epa_pesticide_claims": epa_claims,
        "trademark_violations": trademark_hits,
        "alt_issues": alt_issues,
        "dimensions_3d": [f"{d[0]}x{d[1]}x{d[2]} {d[3]}" for d in dims_3d],
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
    if result["epa_pesticide_claims"]:
        flags.append("EPA_PESTICIDE_CLAIM")
    if result["trademark_violations"]:
        flags.append("TRADEMARK_VIOLATION")
    if any(item.get("wrong_language") for item in alt_issues):
        flags.append("ALT_WRONG_LANGUAGE")
    if any(item.get("empty") for item in alt_issues):
        flags.append("ALT_EMPTY")
    if any(item.get("too_generic") for item in alt_issues):
        flags.append("ALT_TOO_GENERIC")
    if measurement_conflicts:
        flags.append("MEASUREMENT_CONFLICT_REVIEW")

    # Add health score to result
    result["health_score"] = calculate_health_score(result)
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
    # 1. Test coffee grinder with prohibited terms, EPA claims, trademark
    coffee = scan(
        {
            "marketplace": "US",
            "title": "SHARDOR Super Silent Coffee Grinder, 2-Year Warranty, Black",
            "bullets": ["12 cups capacity", "63 dB quiet motor", "Features Velcro cord strap"],
            "search_terms": "burr mill B0FG6TJJGN best",
            "alts": {"MAIN": "咖啡研磨机", "IMG2": "coffee grinder"},
            "attributes": {"item_dimensions": "4.7 in x 4.7 in x 6.77 in"},
        }
    )
    assert "PDP_PROHIBITED_TERM" in coffee["flags"]
    assert "ST_CONTAINS_ASIN" in coffee["flags"]
    assert "ALT_WRONG_LANGUAGE" in coffee["flags"]
    assert "TRADEMARK_VIOLATION" in coffee["flags"]
    # 4.7 x 4.7 x 6.77 in should NOT trigger MEASUREMENT_CONFLICT_REVIEW
    assert "MEASUREMENT_CONFLICT_REVIEW" not in coffee["flags"], f"Unexpected conflict: {coffee['measurement_conflicts']}"
    assert coffee["health_score"]["score"] < 50
    assert coffee["health_score"]["level"] == "CRITICAL_RISK"

    # 2. Test whitelist for 'for best results' and 3D dimensions
    clean_apparel = scan(
        {
            "marketplace": "US",
            "title": "Brand Cotton Crew T-Shirt, Navy",
            "bullets": [
                "100% cotton fabric",
                "For best results, wash with cold water",
                "Package dimensions: 10 in x 8 in x 1 in",
            ],
            "search_terms": "tee crewneck everyday shirt",
            "alts": {
                "MAIN": "Brand navy cotton crew t-shirt front view on white background",
            },
            "attributes": {"size": "M"},
        }
    )
    assert "PDP_PROHIBITED_TERM" not in clean_apparel["flags"], f"False positive prohibited term: {clean_apparel['pdp_prohibited']}"
    assert "ST_CONTAINS_ASIN" not in clean_apparel["flags"]
    assert "MEASUREMENT_CONFLICT_REVIEW" not in clean_apparel["flags"]
    assert clean_apparel["health_score"]["score"] == 100
    assert clean_apparel["health_score"]["level"] == "LOW_RISK_HEALTHY"

    # 3. Test EPA pesticide claim
    pesticide_item = scan(
        {
            "marketplace": "US",
            "title": "Brand Cutting Board with Anti-microbial Surface, Gray",
            "bullets": ["Mold-resistant kitchen board"],
            "alts": {"MAIN": "Brand gray cutting board"},
        }
    )
    assert "EPA_PESTICIDE_CLAIM" in pesticide_item["flags"]
    assert len(pesticide_item["epa_pesticide_claims"]) >= 2
    assert pesticide_item["health_score"]["score"] <= 80

    # 4. Test real measurement conflict
    conflicted_item = scan(
        {
            "marketplace": "US",
            "title": "Brand Grinder",
            "bullets": ["12 cups capacity bowl"],
            "attributes": {"capacity": "3 cups"},
        }
    )
    assert "MEASUREMENT_CONFLICT_REVIEW" in conflicted_item["flags"]
    assert "cup" in conflicted_item["measurement_conflicts"]

    print("All enhanced self-tests passed successfully!")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    if args.self_test:
        return self_test()
    payload = payload_from_args(args)
    json.dump(scan(payload), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
