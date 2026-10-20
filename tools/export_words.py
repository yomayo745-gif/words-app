"""
Export vocabulary dataset from flashcards/data/words.py into:
1. webapp/data/decks/01-freq-core-1.json .. 03-freq-core-3.json (merged into deck architecture, deduplicated)
2. webapp/data/words.json (backward-compatible export)
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")

REQUIRED_FIELDS = (
    "english",
    "pronunciation_uz",
    "uzbek",
    "pos",
    "example_en",
    "example_uz",
    "category",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEBAPP_DATA_JSON = PROJECT_ROOT / "webapp" / "data" / "words.json"
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"


def format_uzbek_apostrophes(text: str) -> str:
    res = re.sub(r"([oOgG])['’ʼʻ`]", lambda m: f"{m.group(1)}\u02bb", text.strip())
    res = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\u2019", res)
    return res


def find_words_py() -> Path:
    candidates = [
        PROJECT_ROOT.parent / "flashcards" / "data" / "words.py",
        Path.home() / ".gemini" / "antigravity" / "scratch" / "flashcards" / "data" / "words.py",
        Path.home() / "Desktop" / "flashcards" / "data" / "words.py",
    ]
    for path in candidates:
        if path.is_file():
            return path
    for found in Path.home().rglob("words.py"):
        if found.parent.name == "data":
            return found
    raise FileNotFoundError("Could not find flashcards/data/words.py on this machine.")


def load_words_from_module(words_py_path: Path) -> list[dict[str, str]]:
    spec = importlib.util.spec_from_file_location("flashcards_words", str(words_py_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module spec from {words_py_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["flashcards_words"] = module
    spec.loader.exec_module(module)
    return list(module.WORDS)


def main() -> int:
    source_path = find_words_py()
    raw_words = load_words_from_module(source_path)

    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    target_deck_files = {"freq-01-top-150.json", "freq-02-top-300.json", "freq-03-top-450.json"}

    # Collect existing words in other deck files so we never create duplicates across decks
    existing_other_decks: set[str] = set()
    for deck_file in DECKS_DIR.glob("*.json"):
        if deck_file.name in target_deck_files:
            continue
        try:
            payload = json.loads(deck_file.read_text(encoding="utf-8"))
            wlist = payload if isinstance(payload, list) else payload.get("words", [])
            for item in wlist:
                en = item.get("english", "").strip().lower()
                if en:
                    existing_other_decks.add(en)
        except Exception:
            pass

    seen_in_source: set[str] = set()
    cleaned_all: list[dict[str, Any]] = []
    cleaned_for_decks: list[dict[str, str]] = []

    for idx, item in enumerate(raw_words, start=1):
        for field in REQUIRED_FIELDS:
            val = item.get(field)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"Entry #{idx} has empty or missing field '{field}'.")

        en_norm = item["english"].strip().lower()
        if en_norm in seen_in_source:
            continue
        seen_in_source.add(en_norm)

        entry = {
            "english": item["english"].strip(),
            "pronunciation_uz": format_uzbek_apostrophes(item["pronunciation_uz"]),
            "uzbek": format_uzbek_apostrophes(item["uzbek"]),
            "pos": item["pos"].strip().lower(),
            "example_en": item["example_en"].strip(),
            "example_uz": format_uzbek_apostrophes(item["example_uz"]),
            "category": format_uzbek_apostrophes(item["category"]),
        }
        cleaned_all.append({"id": len(cleaned_all) + 1, **entry})
        if en_norm not in existing_other_decks:
            cleaned_for_decks.append(entry)

    WEBAPP_DATA_JSON.parent.mkdir(parents=True, exist_ok=True)
    WEBAPP_DATA_JSON.write_text(json.dumps(cleaned_all, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Split the 450 core A1-B1 words into 3 frequency-foundation decks of 150 words each
    batches = [
        ("freq-01-top-150.json", "Eng koʻp ishlatiladigan 1–150 soʻzlar (A1)", "Top 500 • 1–150", cleaned_for_decks[0:150]),
        ("freq-02-top-300.json", "Eng koʻp ishlatiladigan 151–300 soʻzlar (A1–A2)", "Top 500 • 151–300", cleaned_for_decks[150:300]),
        ("freq-03-top-450.json", "Eng koʻp ishlatiladigan 301–450 soʻzlar (A2)", "Top 500 • 301–450", cleaned_for_decks[300:450]),
    ]

    for fname, title_uz, cat_en, chunk in batches:
        if not chunk:
            continue
        out_path = DECKS_DIR / fname
        deck_obj = {
            "title": title_uz,
            "category": cat_en,
            "group": "freq",
            "words": chunk,
        }
        out_path.write_text(json.dumps(deck_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Exported {len(cleaned_all)} words from {source_path} into {WEBAPP_DATA_JSON} and 3 core deck files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
