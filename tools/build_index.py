"""
Build webapp/data/index.json manifest from all deck files in webapp/data/decks/*.json.

Supports:
- Separate Book Decks ("Kitob 1..4", "1.1-bob", "1.2-bob", etc.)
- General Frequency Decks ("freq-*.json")
- General Topic Decks ("topic-*.json")
- "Hammasi" mode strictly contains only general decks (7,226 words), as requested.
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

BOOK_PALETTES = [
    {"accentIndex": 4, "badge": "K1"}, # Violet
    {"accentIndex": 6, "badge": "K2"}, # Emerald
    {"accentIndex": 2, "badge": "K3"}, # Amber
    {"accentIndex": 3, "badge": "K4"}, # Rose
]


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
            inferred_grp = str(grp) if grp else ("book" if slug.startswith("book-") else ("freq" if slug.startswith(("freq-", "top-")) else "topic"))
            return (
                format_uzbek_apostrophes(title),
                str(cat or title).strip(),
                inferred_grp,
            )

    first_cat = words[0].get("category", "").strip() if words else ""
    if slug.startswith("book-"):
        group = "book"
    elif slug.startswith(("freq-", "top-")):
        group = "freq"
    else:
        group = "topic"

    title = format_uzbek_apostrophes(first_cat) if first_cat else humanize_slug(slug)
    category = first_cat if first_cat else humanize_slug(slug)
    return title, category, group


def build_index() -> dict[str, Any]:
    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    deck_files = sorted(DECKS_DIR.glob("*.json"))

    general_decks_manifest: list[dict[str, Any]] = []
    book_decks_manifest: list[dict[str, Any]] = []

    freq_file_names: list[str] = []
    topic_file_names: list[str] = []
    general_words_count = 0
    book_words_count = 0

    for idx, deck_file in enumerate(deck_files):
        raw = json.loads(deck_file.read_text(encoding="utf-8"))
        words: list[dict[str, str]] = raw if isinstance(raw, list) else raw.get("words", [])
        if not words:
            continue

        slug = deck_file.stem
        title_uz, category_label, group = infer_deck_metadata(slug, raw, words)
        count = len(words)
        rel_file = f"data/decks/{deck_file.name}"

        if group == "book":
            book_words_count += count
            # Determine badge: e.g. "book-01-unit-01" -> "1.1"
            m = re.match(r"book-0?(\d+)-unit-0?(\d+)", slug)
            badge = f"{m.group(1)}.{m.group(2)}" if m else "KITOB"
            b_idx = int(m.group(1)) - 1 if m else 0
            accent_idx = BOOK_PALETTES[b_idx % len(BOOK_PALETTES)]["accentIndex"]

            book_decks_manifest.append(
                {
                    "id": slug,
                    "title": title_uz,
                    "category": category_label,
                    "group": "book",
                    "badge": badge,
                    "wordCount": count,
                    "accentIndex": accent_idx,
                    "files": [rel_file],
                }
            )
        else:
            general_words_count += count
            if group == "freq":
                freq_file_names.append(rel_file)
            else:
                topic_file_names.append(rel_file)

            general_decks_manifest.append(
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

    # General files for "Hammasi" mode (books are strictly excluded from Hammasi)
    ordered_general_files = freq_file_names + topic_file_names

    # Book composite presets (Kitob 1..4 Barcha boblar)
    book_presets: list[dict[str, Any]] = []
    for b_num in (1, 2, 3, 4):
        b_units = [d for d in book_decks_manifest if d["id"].startswith(f"book-0{b_num}-")]
        if not b_units:
            continue
        total_b_words = sum(u["wordCount"] for u in b_units)
        b_files = [u["files"][0] for u in b_units]
        accent_idx = BOOK_PALETTES[(b_num - 1) % len(BOOK_PALETTES)]["accentIndex"]
        book_presets.append(
            {
                "id": f"book-0{b_num}-all",
                "title": f"Kitob {b_num} — Barcha boblar",
                "category": f"1500 Essential English Words {b_num}",
                "group": "book",
                "badge": f"K{b_num}",
                "wordCount": total_b_words,
                "accentIndex": accent_idx,
                "files": b_files,
                "isBookSummary": True,
            }
        )
        # Add unit decks for this book right after the book summary
        for u in b_units:
            book_presets.append(u)

    # Frequency Milestone Decks ("Top 500", "Top 1000", "Top 2000", "Top 3000", "Top 5000")
    file_word_counts = {d["files"][0]: d["wordCount"] for d in general_decks_manifest}
    milestone_presets: list[dict[str, Any]] = []
    milestones = [
        ("top-500", "Top 500 — Eng kerakli soʻzlar", "Most Frequent 500 Words", 500, 0),
        ("top-1000", "Top 1000 — Asosiy kundalik soʻzlar", "Most Frequent 1,000 Words", 1000, 1),
        ("top-2000", "Top 2000 — Kundalik va oʻrta daraja", "Most Frequent 2,000 Words", 2000, 2),
        ("top-3000", "Top 3000 — Kengaytirilgan faol lugʻat", "Most Frequent 3,000 Words", 3000, 5),
        ("top-5000", "Top 5000 — Toʻliq faol va akademik bazasi", "Most Frequent 5,000 Words", 5000, 6),
    ]

    for m_id, m_title, m_cat, target_count, accent_idx in milestones:
        effective_count = min(target_count, general_words_count)
        needed_files: list[str] = []
        acc = 0
        for fpath in ordered_general_files:
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

    all_selectable_decks = book_presets + milestone_presets + general_decks_manifest

    manifest = {
        "version": 3,
        "totalWords": general_words_count,
        "bookWords": book_words_count,
        "totalDeckFiles": len(general_decks_manifest),
        "totalBookFiles": len(book_decks_manifest),
        "allFiles": ordered_general_files,
        "decks": all_selectable_decks,
    }

    INDEX_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_JSON_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    size_kb = INDEX_JSON_PATH.stat().st_size / 1024.0
    print(f"Generated {INDEX_JSON_PATH} ({size_kb:.1f} KB)")
    print(f"General Decks: {len(general_decks_manifest)} | General Words (Hammasi): {general_words_count}")
    print(f"Book Decks: {len(book_decks_manifest)} | Book Words (Kitoblar 1-4): {book_words_count}")
    print(f"Total Selectable Decks in manifest: {len(manifest['decks'])}")
    return manifest


if __name__ == "__main__":
    build_index()
