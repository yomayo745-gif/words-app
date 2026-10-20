"""
Build webapp/data/index.json manifest from all deck files in webapp/data/decks/*.json.

Adding new words later:
1. Drop any new <deck-slug>.json file into webapp/data/decks/
2. Run: python tools/build_index.py
No code changes required.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"
INDEX_JSON_PATH = PROJECT_ROOT / "webapp" / "data" / "index.json"

# Known Uzbek titles for deck slugs (fallback humanizes any new custom slug automatically)
KNOWN_DECK_TITLES: dict[str, tuple[str, str, str]] = {
    # slug -> (Uzbek Title, English Subtitle / Category, Group: 'freq' | 'topic')
    "freq-top-01": ("Top 1–200: Eng koʻp ishlatiladigan soʻzlar", "Top 500 • Part 1", "freq"),
    "freq-top-02": ("Top 201–400: Eng koʻp ishlatiladigan soʻzlar", "Top 500 • Part 2", "freq"),
    "freq-top-03": ("Top 401–600: Kundalik asosiy soʻzlar", "Top 1000 • Part 1", "freq"),
    "freq-top-04": ("Top 601–800: Kundalik asosiy soʻzlar", "Top 1000 • Part 2", "freq"),
    "freq-top-05": ("Top 801–1000: Kundalik asosiy soʻzlar", "Top 1000 • Part 3", "freq"),
    "freq-top-06": ("Top 1001–1200: Oʻrta daraja (B1) soʻzlari", "Top 2000 • Part 1", "freq"),
    "freq-top-07": ("Top 1201–1400: Oʻrta daraja (B1) soʻzlari", "Top 2000 • Part 2", "freq"),
    "freq-top-08": ("Top 1401–1600: Oʻrta daraja (B1) soʻzlari", "Top 2000 • Part 3", "freq"),
    "freq-top-09": ("Top 1601–1800: Oʻrta daraja (B1) soʻzlari", "Top 2000 • Part 4", "freq"),
    "freq-top-10": ("Top 1801–2000: Oʻrta daraja (B1) soʻzlari", "Top 2000 • Part 5", "freq"),
    "freq-top-11": ("Top 2001–2200: Kengaytirilgan lugʻat (B1+)", "Top 3000 • Part 1", "freq"),
    "freq-top-12": ("Top 2201–2400: Kengaytirilgan lugʻat (B1+)", "Top 3000 • Part 2", "freq"),
    "freq-top-13": ("Top 2401–2600: Kengaytirilgan lugʻat (B1+)", "Top 3000 • Part 3", "freq"),
    "freq-top-14": ("Top 2601–2800: Kengaytirilgan lugʻat (B1+)", "Top 3000 • Part 4", "freq"),
    "freq-top-15": ("Top 2801–3000: Kengaytirilgan lugʻat (B1+)", "Top 3000 • Part 5", "freq"),
    "freq-top-16": ("Top 3001–3200: Yuqori bosqich soʻzlari (B2)", "Top 5000 • Part 1", "freq"),
    "freq-top-17": ("Top 3201–3400: Yuqori bosqich soʻzlari (B2)", "Top 5000 • Part 2", "freq"),
    "freq-top-18": ("Top 3401–3600: Yuqori bosqich soʻzlari (B2)", "Top 5000 • Part 3", "freq"),
    "freq-top-19": ("Top 3601–3800: Yuqori bosqich soʻzlari (B2)", "Top 5000 • Part 4", "freq"),
    "freq-top-20": ("Top 3801–4000: Yuqori bosqich soʻzlari (B2)", "Top 5000 • Part 5", "freq"),
}


def format_uzbek_apostrophes(text: str) -> str:
    res = re.sub(r"([oOgG])['’ʼʻ`]", lambda m: f"{m.group(1)}\u02bb", text.strip())
    res = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\u2019", res)
    return res


def humanize_slug(slug: str) -> str:
    cleaned = re.sub(r"^\d+[-_]", "", slug)
    return cleaned.replace("-", " ").replace("_", " ").title()


def infer_deck_metadata(
    slug: str,
    payload: Any,
    words: list[dict[str, str]],
) -> tuple[str, str, str]:
    """Return (title_uz, category_label, group) for a deck file."""
    if isinstance(payload, dict):
        title = payload.get("title")
        cat = payload.get("category")
        grp = payload.get("group")
        if isinstance(title, str) and title.strip():
            return (
                format_uzbek_apostrophes(title),
                str(cat or title).strip(),
                str(grp or ("freq" if slug.startswith(("freq-", "top-")) else "topic")),
            )

    if slug in KNOWN_DECK_TITLES:
        return KNOWN_DECK_TITLES[slug]

    first_cat = words[0].get("category", "").strip() if words else ""
    group = "freq" if slug.startswith(("freq-", "top-")) else "topic"
    title = format_uzbek_apostrophes(first_cat) if first_cat else humanize_slug(slug)
    category = first_cat if first_cat else humanize_slug(slug)
    return title, category, group


def build_index() -> dict[str, Any]:
    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    deck_files = sorted(DECKS_DIR.glob("*.json"))

    decks_manifest: list[dict[str, Any]] = []
    all_file_names: list[str] = []
    freq_file_names: list[str] = []
    topic_file_names: list[str] = []
    total_words = 0

    for idx, deck_file in enumerate(deck_files):
        raw = json.loads(deck_file.read_text(encoding="utf-8"))
        words: list[dict[str, str]] = raw if isinstance(raw, list) else raw.get("words", [])
        if not words:
            continue

        # Normalize Uzbek typography in-place to ensure clean apostrophes
        modified = False
        for w in words:
            for k in ("pronunciation_uz", "uzbek", "example_uz", "category"):
                if k in w and isinstance(w[k], str):
                    norm_val = format_uzbek_apostrophes(w[k])
                    if norm_val != w[k]:
                        w[k] = norm_val
                        modified = True

        if modified:
            if isinstance(raw, list):
                deck_file.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            else:
                raw["words"] = words
                deck_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        slug = deck_file.stem
        title_uz, category_label, group = infer_deck_metadata(slug, raw, words)
        count = len(words)
        total_words += count

        rel_file = f"data/decks/{deck_file.name}"
        all_file_names.append(rel_file)
        if group == "freq":
            freq_file_names.append(rel_file)
        else:
            topic_file_names.append(rel_file)

        decks_manifest.append(
            {
                "id": slug,
                "title": title_uz,
                "category": category_label,
                "group": group,
                "wordCount": count,
                "accentIndex": idx % 10,
                "files": [rel_file],
            }
        )

    # Order files so frequency files come first, then topic files
    ordered_all_files = freq_file_names + topic_file_names

    # Build cumulative Frequency Milestone Decks ("Top 500", "Top 1000", "Top 2000", "Top 3000", "Top 5000")
    # at the top of the "Eng kerakli so'zlar" group
    milestone_presets: list[dict[str, Any]] = []
    milestones = [
        ("top-500", "Top 500 — Eng kerakli soʻzlar", "Most Frequent 500 Words", 500, 0),
        ("top-1000", "Top 1000 — Asosiy kundalik soʻzlar", "Most Frequent 1,000 Words", 1000, 1),
        ("top-2000", "Top 2000 — Kundalik va oʻrta daraja", "Most Frequent 2,000 Words", 2000, 2),
        ("top-3000", "Top 3000 — Kengaytirilgan faol lugʻat", "Most Frequent 3,000 Words", 3000, 5),
        ("top-5000", "Top 5000 — Toʻliq faol va akademik bazasi", "Most Frequent 5,000 Words", 5000, 6),
    ]

    # Map each file to its word count for fast slice calculation
    file_word_counts = {d["files"][0]: d["wordCount"] for d in decks_manifest}

    for m_id, m_title, m_cat, target_count, accent_idx in milestones:
        effective_count = min(target_count, total_words)
        if effective_count <= 0:
            continue
        needed_files: list[str] = []
        acc = 0
        for fpath in ordered_all_files:
            needed_files.append(fpath)
            acc += file_word_counts.get(fpath, 0)
            if acc >= effective_count:
                break
        milestone_presets.append(
            {
                "id": m_id,
                "title": m_title,
                "category": m_cat,
                "group": "freq",
                "wordCount": effective_count,
                "limit": effective_count,
                "accentIndex": accent_idx,
                "files": needed_files,
                "isMilestone": True,
            }
        )

    manifest = {
        "version": 2,
        "totalWords": total_words,
        "totalDeckFiles": len(decks_manifest),
        "allFiles": ordered_all_files,
        "decks": milestone_presets + decks_manifest,
    }

    INDEX_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_JSON_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    size_kb = INDEX_JSON_PATH.stat().st_size / 1024.0
    print(f"Generated {INDEX_JSON_PATH} ({size_kb:.1f} KB)")
    print(f"Physical deck files: {len(decks_manifest)} | Total unique words: {total_words}")
    print(f"Total selectable decks in manifest (including Top 500..5000 presets): {len(manifest['decks'])}")
    return manifest


if __name__ == "__main__":
    build_index()
