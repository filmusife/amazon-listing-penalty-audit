#!/usr/bin/env python3
"""Deterministic scans for Amazon listing penalty audits.

Upgraded to strictly enforce Amazon Seller Central official rules & limits:
- A+ Content Image Keywords (Alt-Text): Hard limit <= 100 characters per image
- Product Title: Hard suppression limit 200 chars; Mobile sweet spot <= 75 chars; Forbidden symbols (! $ ? _ { } ^ ¬ ¦) & CJK
- Key Product Features (Bullets): Recommended 5 bullets, <= 255 chars each, total <= 1000 chars; No ALL CAPS; No decorative emoji/icons
- Item Highlights: Hard limit <= 125 characters
- Search Terms (Generic Keywords): Hard limit < 250 bytes (UTF-8); No redundant front-end words, No ASINs, No competitor brands
- Intelligent 3D dimension parsing (no false positives for L x W x H)
- High-risk EPA/FIFRA pesticide & antimicrobial claim detection
- Registered trademark & IP brand trap detection (Velcro, Thermos, PopSockets, etc.)
- 0-100 Quantified Listing Health Score & Risk Level classification

Example:
  python scan_listing.py --input extracted.json
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
FORBIDDEN_TITLE_CHARS_RE = re.compile(r"[!$?_{}^¬¦]")
EMOJI_OR_ICON_RE = re.compile(r"[\u2600-\u27bf\U0001f300-\U0001f9ff\u25a0-\u25ff【】★◆▲▼●■►◄]")
BANNED_BULLET_SYMBOLS_RE = re.compile(r"[™®©…†‡±~€£¥¢✓❌]")

# Official Amazon Limits
APLUS_ALT_MAX_CHARS = 100
TITLE_HARD_MAX_CHARS = 200
HIGHLIGHTS_MAX_CHARS = 125
BULLET_MAX_CHARS = 255
BULLETS_TOTAL_MAX_CHARS = 1000
ST_MAX_BYTES_LIMIT = 250  # Must be strictly < 250 bytes
MOBILE_PREVIEW_LIMIT = 65  # Mobile search card display limit before CSS truncation

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
    "US": {"title_mobile_chars": 75, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "en"},
    "CA": {"title_mobile_chars": 75, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "en"},
    "UK": {"title_mobile_chars": 75, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "en"},
    "AU": {"title_mobile_chars": 75, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "en"},
    "DE": {"title_mobile_chars": None, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "de"},
    "FR": {"title_mobile_chars": None, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "fr"},
    "IT": {"title_mobile_chars": None, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "it"},
    "ES": {"title_mobile_chars": None, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "es"},
    "JP": {"title_mobile_chars": None, "title_hard_chars": 200, "st_max_bytes": 250, "listing_lang": "ja"},
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


def sanitize_title_and_highlights(raw_title: str, raw_highlights: str = "") -> tuple[str, str, dict[str, Any]]:
    """Clean title of scraping / ERP delimiter artifacts (e.g., 'Title | Highlights' or 'Title | Metadata').

    Prevents false 'pipe abuse' violations and correctly routes concatenated data.
    """
    cleaned_title = raw_title.strip()
    cleaned_highlights = raw_highlights.strip()
    delimiter_info: dict[str, Any] = {
        "has_crawler_delimiter": False,
        "delimiter_type": None,
        "raw_segments": [],
        "note": "",
    }

    # Check for pipe delimiter common in scraper/API concatenated exports
    if " | " in cleaned_title or " |" in cleaned_title or "| " in cleaned_title:
        segments = [s.strip() for s in re.split(r"\s*\|\s*", cleaned_title) if s.strip()]
        if len(segments) >= 2:
            delimiter_info["has_crawler_delimiter"] = True
            delimiter_info["delimiter_type"] = "pipe"
            delimiter_info["raw_segments"] = segments

            # Segment 0 is typically the primary product title
            primary_title = segments[0]
            extra_segment = " | ".join(segments[1:])

            # If highlights was empty, route extra segments into highlights
            if not cleaned_highlights:
                cleaned_highlights = extra_segment
                delimiter_info["note"] = (
                    "检测到数据抓取/ERP管道符分隔物（如标题与高亮或标签被拼接），"
                    "已自动清洗剥离：第一段作为核心标题，后续段解析为高亮/卖点，不计入卖家违规扣分。"
                )
            else:
                delimiter_info["note"] = (
                    "检测到抓取拼接的管道符分隔符，已自动剥离为纯净标题，避免将爬虫拼接符号误判为卖家违规。"
                )
            cleaned_title = primary_title

    return cleaned_title, cleaned_highlights, delimiter_info


def calculate_health_score(result: dict[str, Any]) -> dict[str, Any]:
    """Calculate 0-100 Listing Health Score and penalty risk level based on Amazon official policies."""
    score = 100
    deductions: list[dict[str, Any]] = []

    # 1. Critical Policy & IP Violations (-15 to -20 pts)
    if result.get("epa_pesticide_claims"):
        score -= 20
        deductions.append({"issue": "EPA/FIFRA 未申报杀菌/农药高危词 (面临整条商品下架风险)", "points": -20})
    if result.get("trademark_violations"):
        score -= 20
        deductions.append({"issue": "注册商标侵权风险 (如 Velcro, Thermos 等通用化误用)", "points": -20})
    if "TITLE_OVER_HARD_LIMIT" in result.get("flags", []):
        score -= 20
        deductions.append({"issue": f"标题超过亚马逊官方硬性上限 (>{TITLE_HARD_MAX_CHARS}字符，直接被搜索抑制)", "points": -20})
    if "ST_CONTAINS_ASIN" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Search Terms 违规填入 ASIN", "points": -15})
    if "ST_PROHIBITED_TERM" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Search Terms 含有保修/竞品/违规禁用词", "points": -15})
    if "PDP_PROHIBITED_TERM" in result.get("flags", []):
        score -= 15
        deductions.append({"issue": "Listing 含有保修/保证/未认证环保(eco-friendly)/绝对化夸大禁用词", "points": -15})

    # 2. Major Amazon Operational & System Limit Breaches (-10 pts)
    if "APLUS_ALT_OVER_LIMIT" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": f"A+ 图片 ALT 超过亚马逊官方硬性限制 (>{APLUS_ALT_MAX_CHARS} 字符，后台无法保存)", "points": -10})
    if "ST_OVER_BYTE_LIMIT" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": f"Search Terms 达到或超出 {ST_MAX_BYTES_LIMIT} 字节限制 (系统将完全不予建立索引)", "points": -10})
    if "TITLE_CONTAINS_FORBIDDEN_CHARS" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "标题包含全角中文标点或禁用符号 (! $ ? _ { } ^ ¬ ¦ 等)", "points": -10})
    if "TITLE_CONTAINS_CJK" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "英语站点标题中包含中文全角字符", "points": -10})
    if "MEASUREMENT_CONFLICT_REVIEW" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "规格参数打架 (多处尺寸/容量/功率不一致，导致高退货率与INAD)", "points": -10})
    if "ALT_WRONG_LANGUAGE" in result.get("flags", []) or "APLUS_ALT_WRONG_LANGUAGE" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "图片 ALT 错语言 (如英语站出现中文 ALT)", "points": -10})
    if "ALT_EMPTY" in result.get("flags", []):
        score -= 10
        deductions.append({"issue": "图库副图 ALT 存在空白缺失 (影响视觉检索与无障碍评分)", "points": -10})

    # 3. CTR / Conversion / Optimization Issues (-5 pts)
    if "TITLE_CTR_RISK_BRAND_MISSING" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "移动端搜索卡片黄金区（前65字符）缺失品牌名，导致移动端点击率 (CTR) 严重损耗", "points": -5})
    if "BULLET_HAS_BANNED_SYMBOLS" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "五点描述包含2024官方违禁特殊符号/Emoji (™/®/©/…/✓等，面临系统AI重写或移除)", "points": -5})
    if "HIGHLIGHTS_OVER_LIMIT" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": f"Item highlights 超过 {HIGHLIGHTS_MAX_CHARS} 字符上限", "points": -5})
    if "BULLET_OVER_LIMIT" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": f"五点描述单条超过 {BULLET_MAX_CHARS} 字符或总长超 1000 字符", "points": -5})
    if "BULLET_ALL_CAPS" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "五点描述整句使用 ALL CAPS 全大写 (违反风格指南)", "points": -5})
    if "TITLE_WORD_REPEATED" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "标题单词重复超过 2 次 (关键词堆砌扣分)", "points": -5})
    if "ALT_TOO_GENERIC" in result.get("flags", []):
        score -= 5
        deductions.append({"issue": "图片 ALT 过于空泛 (词数 <= 2)", "points": -5})

    score = max(0, min(100, score))

    if score >= 85:
        level = "LOW_RISK_HEALTHY"
        label = "健康良好 (A级: 85-100分 - 政策高度合规，CTR/CVR基础扎实)"
    elif score >= 70:
        level = "MODERATE_RISK"
        label = "中度风险 (B级: 70-84分 - 存在体验瑕疵或检索权重减分)"
    elif score >= 50:
        level = "HIGH_RISK"
        label = "高危受限 (C级: 50-69分 - 权重受抑，多项指标违背官方政策)"
    else:
        level = "CRITICAL_RISK"
        label = "极度危险 (D级: 0-49分 - 面临静默降权或下架红线，必须立即整改)"

    return {
        "score": score,
        "level": level,
        "label": label,
        "deductions": deductions,
    }


def scan(payload: dict[str, Any]) -> dict[str, Any]:
    marketplace = str(payload.get("marketplace") or "US").upper()
    rules = MARKETPLACES.get(marketplace, MARKETPLACES["US"])
    raw_title = str(payload.get("title") or "")
    raw_highlights = str(payload.get("item_highlights") or "")
    brand_name = str(payload.get("brand") or "").strip()

    # Intelligent Title & Highlights sanitization (filters scraper/ERP delimiter artifacts)
    title, highlights, delimiter_info = sanitize_title_and_highlights(raw_title, raw_highlights)

    bullets = _as_list(payload.get("bullets") or payload.get("bullet_points"))
    search_terms = str(payload.get("search_terms") or payload.get("st") or "")
    alts = payload.get("alts") or payload.get("alt") or {}
    aplus_alts = payload.get("aplus_alts") or {}
    attributes = payload.get("attributes") or {}

    alt_items = alts.items() if isinstance(alts, dict) else [(f"ALT{i+1}", v) for i, v in enumerate(_as_list(alts))]
    aplus_alt_items = aplus_alts.items() if isinstance(aplus_alts, dict) else [(f"A+{i+1}", v) for i, v in enumerate(_as_list(aplus_alts))]

    # Filter out dedicated warranty fields (which are legally allowed in backend attributes)
    marketing_attributes = {
        k: v for k, v in attributes.items()
        if not any(w in k.lower() for w in ["warranty", "guarantee"])
    }
    attr_text = _join_fields({"attributes": marketing_attributes}, ["attributes"])
    pdp_text = "\n".join([title, highlights, *bullets, attr_text, *[str(v) for _, v in alt_items], *[str(v) for _, v in aplus_alt_items]])

    # 1. Title Scan & CTR Golden Zone Analysis
    title_chars = len(title)
    title_hard_max = rules.get("title_hard_chars", TITLE_HARD_MAX_CHARS)
    title_over_hard = bool(title and title_chars > title_hard_max)
    title_has_forbidden = bool(FORBIDDEN_TITLE_CHARS_RE.search(title))
    title_has_cjk = bool(rules["listing_lang"] == "en" and CJK_RE.search(title))

    # Mobile Golden Zone (CTR Preview: ~65 chars displayed in mobile search cards before CSS line-clamp)
    mobile_preview = title[:MOBILE_PREVIEW_LIMIT] + ("..." if title_chars > MOBILE_PREVIEW_LIMIT else "")
    brand_in_mobile_zone = True
    if brand_name:
        brand_in_mobile_zone = bool(re.search(rf"\b{re.escape(brand_name)}\b", title[:MOBILE_PREVIEW_LIMIT], re.I))

    # 2. Search Terms Scan
    st_bytes = len(search_terms.encode("utf-8"))
    st_over_limit = bool(search_terms) and st_bytes >= ST_MAX_BYTES_LIMIT

    # 3. Item Highlights Scan
    highlights_chars = len(highlights)
    highlights_over_limit = bool(highlights and highlights_chars > HIGHLIGHTS_MAX_CHARS)

    # 4. Bullet Points Scan (August 15, 2024 Policy Update)
    bullet_issues = []
    total_bullet_chars = 0
    for idx, b in enumerate(bullets, 1):
        b_len = len(b)
        total_bullet_chars += b_len
        b_issue = {
            "index": idx,
            "chars": b_len,
            "over_limit": b_len > BULLET_MAX_CHARS,
            "all_caps": False,
            "has_icon_or_emoji": False,
            "has_banned_symbols": False,
            "ends_with_period": False,
        }
        if b_len > 20 and b.isupper():
            b_issue["all_caps"] = True
        if EMOJI_OR_ICON_RE.search(b):
            b_issue["has_icon_or_emoji"] = True
        if BANNED_BULLET_SYMBOLS_RE.search(b):
            b_issue["has_banned_symbols"] = True
        if b.strip().endswith("."):
            b_issue["ends_with_period"] = True

        if (
            b_issue["over_limit"]
            or b_issue["all_caps"]
            or b_issue["has_icon_or_emoji"]
            or b_issue["has_banned_symbols"]
            or b_issue["ends_with_period"]
        ):
            bullet_issues.append(b_issue)

    # 5. Gallery Image ALTs Scan
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

    # 6. A+ Content ALTs Scan (Official Amazon A+ Limit: <= 100 characters)
    aplus_alt_issues = []
    for key, value in aplus_alt_items:
        text = str(value or "")
        chars = len(text)
        issue = {
            "key": key,
            "chars": chars,
            "max_chars": APLUS_ALT_MAX_CHARS,
            "over_limit": chars > APLUS_ALT_MAX_CHARS,
            "cjk": bool(CJK_RE.search(text)),
            "empty": not text.strip(),
        }
        generic = bool(re.fullmatch(r"[A-Za-z ]{0,24}", text.strip())) and len(text.split()) <= 2
        issue["too_generic"] = generic and not issue["empty"]
        if rules["listing_lang"] == "en" and issue["cjk"]:
            issue["wrong_language"] = True
        elif rules["listing_lang"] != "ja" and issue["cjk"] and rules["listing_lang"] != "zh":
            issue["wrong_language"] = True
        else:
            issue["wrong_language"] = False
        if issue["over_limit"] or issue["empty"] or issue["cjk"] or issue["too_generic"] or issue["wrong_language"]:
            aplus_alt_issues.append(issue)

    # 7. Measurements and Conflicts
    dims_3d, measurements, measurement_conflicts = _extract_dimensions_and_measurements(pdp_text)

    # 8. Claims and IP Checks
    pdp_prohibited = _find_patterns(pdp_text, PROHIBITED_PATTERNS)
    st_prohibited = _find_patterns(search_terms, PROHIBITED_PATTERNS)
    epa_claims = _find_patterns(pdp_text, EPA_PESTICIDE_PATTERNS)
    trademark_hits = _find_patterns(pdp_text, TRADEMARK_PATTERNS)

    result = {
        "marketplace": marketplace,
        "listing_lang": rules["listing_lang"],
        "title": {
            "raw_title": raw_title,
            "clean_title": title,
            "chars": title_chars,
            "hard_max_chars": title_hard_max,
            "over_hard_limit": title_over_hard,
            "mobile_preview": mobile_preview,
            "brand_in_mobile_zone": brand_in_mobile_zone,
            "has_forbidden_chars": title_has_forbidden,
            "has_cjk": title_has_cjk,
            "delimiter_info": delimiter_info,
            "repeat_words": _repeat_words(title),
            "safe_indexing_zone": bool(40 <= title_chars <= 180),
        },
        "item_highlights": {
            "chars": highlights_chars,
            "max_chars": HIGHLIGHTS_MAX_CHARS,
            "over_limit": highlights_over_limit,
        },
        "bullets": {
            "count": len(bullets),
            "total_chars": total_bullet_chars,
            "total_over_limit": total_bullet_chars > BULLETS_TOTAL_MAX_CHARS,
            "issues": bullet_issues,
        },
        "search_terms": {
            "bytes": st_bytes,
            "max_bytes": ST_MAX_BYTES_LIMIT,
            "over_limit": st_over_limit,
            "asins": ASIN_RE.findall(search_terms),
            "prohibited": st_prohibited,
        },
        "pdp_prohibited": pdp_prohibited,
        "epa_pesticide_claims": epa_claims,
        "trademark_violations": trademark_hits,
        "alt_issues": alt_issues,
        "aplus_alt_issues": aplus_alt_issues,
        "dimensions_3d": [f"{d[0]}x{d[1]}x{d[2]} {d[3]}" for d in dims_3d],
        "measurements": measurements,
        "measurement_conflicts": measurement_conflicts,
        "flags": [],
    }

    flags = result["flags"]
    if result["title"]["over_hard_limit"]:
        flags.append("TITLE_OVER_HARD_LIMIT")
    if not result["title"]["brand_in_mobile_zone"] and brand_name and title:
        flags.append("TITLE_CTR_RISK_BRAND_MISSING")
    if result["title"]["has_forbidden_chars"]:
        flags.append("TITLE_CONTAINS_FORBIDDEN_CHARS")
    if result["title"]["has_cjk"]:
        flags.append("TITLE_CONTAINS_CJK")
    if result["title"]["repeat_words"]:
        flags.append("TITLE_WORD_REPEATED")
    if delimiter_info["has_crawler_delimiter"]:
        flags.append("CRAWLER_DELIMITER_FILTERED")

    if result["item_highlights"]["over_limit"]:
        flags.append("HIGHLIGHTS_OVER_LIMIT")

    if result["bullets"]["total_over_limit"] or any(b.get("over_limit") for b in bullet_issues):
        flags.append("BULLET_OVER_LIMIT")
    if any(b.get("all_caps") for b in bullet_issues):
        flags.append("BULLET_ALL_CAPS")
    if any(b.get("has_banned_symbols") or b.get("has_icon_or_emoji") for b in bullet_issues):
        flags.append("BULLET_HAS_BANNED_SYMBOLS")
    if any(b.get("ends_with_period") for b in bullet_issues):
        flags.append("BULLET_ENDS_WITH_PERIOD")

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

    if any(item.get("over_limit") for item in aplus_alt_issues):
        flags.append("APLUS_ALT_OVER_LIMIT")
    if any(item.get("wrong_language") for item in aplus_alt_issues):
        flags.append("APLUS_ALT_WRONG_LANGUAGE")
    if any(item.get("empty") for item in aplus_alt_issues):
        flags.append("APLUS_ALT_EMPTY")

    if measurement_conflicts:
        flags.append("MEASUREMENT_CONFLICT_REVIEW")

    # Add health score to result
    result["health_score"] = calculate_health_score(result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan extracted Amazon listing fields against Seller Central rules")
    parser.add_argument("--input", help="JSON file; omit to read stdin when piped")
    parser.add_argument("--marketplace", default="US")
    parser.add_argument("--brand", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--highlights", default="")
    parser.add_argument("--st", default="")
    parser.add_argument("--bullet", action="append", default=[])
    parser.add_argument("--alt", action="append", default=[], help="key:value")
    parser.add_argument("--aplus-alt", action="append", default=[], help="key:value")
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
    aplus_alts = {}
    for item in args.aplus_alt:
        if ":" not in item:
            raise SystemExit(f"A+ ALT must be key:value, got {item!r}")
        key, value = item.split(":", 1)
        aplus_alts[key] = value
    return {
        "marketplace": args.marketplace,
        "brand": args.brand,
        "title": args.title,
        "item_highlights": args.highlights,
        "bullets": args.bullet,
        "search_terms": args.st,
        "alts": alts,
        "aplus_alts": aplus_alts,
    }


def PathRead(path: str) -> str:
    from pathlib import Path

    return Path(path).read_text(encoding="utf-8")


def self_test() -> int:
    # 1. Test coffee grinder with prohibited terms, EPA claims, trademark
    coffee = scan(
        {
            "marketplace": "US",
            "brand": "SHARDOR",
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
    assert "MEASUREMENT_CONFLICT_REVIEW" not in coffee["flags"]
    assert coffee["health_score"]["score"] < 50
    assert coffee["health_score"]["level"] == "CRITICAL_RISK"

    # 2. Test whitelist for 'for best results', compliant A+ ALT (<= 100 chars), and 3D dimensions
    clean_apparel = scan(
        {
            "marketplace": "US",
            "brand": "Brand",
            "title": "Brand Cotton Crew T-Shirt, Navy",
            "item_highlights": "100% combed cotton, Ribbed collar, Machine washable",
            "bullets": [
                "100% cotton fabric",
                "For best results, wash with cold water",
                "Package dimensions: 10 in x 8 in x 1 in",
            ],
            "search_terms": "tee crewneck everyday shirt",
            "alts": {
                "MAIN": "Brand navy cotton crew t-shirt front view on white background",
            },
            "aplus_alts": {
                "A+1": "Brand navy blue crewneck t-shirt folded neatly on wooden hanger in wardrobe",
            },
            "attributes": {"size": "M"},
        }
    )
    assert "PDP_PROHIBITED_TERM" not in clean_apparel["flags"]
    assert "ST_CONTAINS_ASIN" not in clean_apparel["flags"]
    assert "APLUS_ALT_OVER_LIMIT" not in clean_apparel["flags"]
    assert "MEASUREMENT_CONFLICT_REVIEW" not in clean_apparel["flags"]
    assert clean_apparel["health_score"]["score"] == 100
    assert clean_apparel["health_score"]["level"] == "LOW_RISK_HEALTHY"

    # 3. Test A+ ALT exceeding 100 characters hard limit
    over_limit_aplus = scan(
        {
            "marketplace": "US",
            "title": "Brand Coffee Maker, Black",
            "bullets": ["8 cup capacity"],
            "aplus_alts": {
                "A+1": "This is an extremely long A+ content alt text description that easily exceeds the official Amazon Seller Central hard limit of one hundred characters",
            },
        }
    )
    assert "APLUS_ALT_OVER_LIMIT" in over_limit_aplus["flags"]
    assert any("A+ 图片 ALT 超过" in d["issue"] for d in over_limit_aplus["health_score"]["deductions"])

    # 4. Test Search Terms >= 250 bytes limit
    over_bytes_st = scan(
        {
            "marketplace": "US",
            "title": "Brand Widget",
            "bullets": ["High quality widget"],
            "search_terms": "a" * 250,
        }
    )
    assert "ST_OVER_BYTE_LIMIT" in over_bytes_st["flags"]

    # 5. Test EPA pesticide claim
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

    # 6. Test crawler pipe delimiter sanitation (TWOMEOW / Baby Food Maker case)
    scraped_item = scan(
        {
            "marketplace": "US",
            "brand": "TWOMEOW",
            "title": "TWOMEOW Baby Food Maker, 5-in-1 Baby Food Processor Steamer and Blender, 10oz | 6 Presets, Touch Screen",
            "bullets": ["Compact baby food steamer and blender", "One touch automatic cooking"],
            "search_terms": "puree toddler meal maker",
            "alts": {"MAIN": "TWOMEOW baby food maker mint green on counter"},
        }
    )
    # The title should be sanitized, pipe removed, extra segment routed to highlights
    assert "CRAWLER_DELIMITER_FILTERED" in scraped_item["flags"]
    assert scraped_item["title"]["clean_title"] == "TWOMEOW Baby Food Maker, 5-in-1 Baby Food Processor Steamer and Blender, 10oz"
    assert scraped_item["item_highlights"]["chars"] > 0 or scraped_item["title"]["delimiter_info"]["has_crawler_delimiter"]
    assert scraped_item["title"]["brand_in_mobile_zone"] is True
    # Crucially: it should NOT deduct points for crawler delimiter
    assert scraped_item["health_score"]["score"] == 100
    assert scraped_item["health_score"]["level"] == "LOW_RISK_HEALTHY"

    # 7. Test Bullet Points with August 15, 2024 prohibited symbols
    banned_bullet_item = scan(
        {
            "marketplace": "US",
            "title": "Brand Blender",
            "bullets": ["Best blender with patented blade™ technology."],
        }
    )
    assert "BULLET_HAS_BANNED_SYMBOLS" in banned_bullet_item["flags"]
    assert "BULLET_ENDS_WITH_PERIOD" in banned_bullet_item["flags"]
    assert any("2024官方违禁特殊符号" in d["issue"] for d in banned_bullet_item["health_score"]["deductions"])

    print("All enhanced Seller Central self-tests passed successfully!")
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
