"""
Validate all deck JSON files in webapp/data/decks/*.json.

Checks:
- Valid JSON syntax in every deck file
- Every entry has non-empty string fields:
  english, pronunciation_uz, uzbek, pos, example_en, example_uz, category
- Zero duplicate English words across all general decks (freq + topic)
- Zero duplicate English words within each book deck
- Prints per-deck word counts and the grand total
- Exits with non-zero status on any validation error (or if general total < min_total)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"

REQUIRED_FIELDS: tuple[str, ...] = (
    "english",
    "pronunciation_uz",
    "uzbek",
    "pos",
    "example_en",
    "example_uz",
    "category",
)


def extract_words_list(payload: object, file_path: Path) -> list[dict[str, str]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("words"), list):
        return payload["words"]
    raise ValueError(f"{file_path.name}: JSON root must be a list of word objects or a dict with a 'words' list.")


def validate_all_decks(decks_dir: Path = DECKS_DIR, min_total: int = 5000) -> tuple[int, list[tuple[str, int]]]:
    if not decks_dir.is_dir():
        raise FileNotFoundError(f"Decks directory does not exist: {decks_dir}")

    deck_files = sorted(decks_dir.glob("*.json"))
    if not deck_files:
        raise ValueError(f"No deck JSON files found in {decks_dir}")

    seen_english_general: dict[str, tuple[str, int]] = {}
    seen_english_per_book: dict[str, dict[str, tuple[str, int]]] = {}
    deck_summaries: list[tuple[str, int, str]] = []
    errors: list[str] = []
    general_total = 0
    books_total = 0

    for deck_file in deck_files:
        try:
            raw_text = deck_file.read_text(encoding="utf-8")
            payload = json.loads(raw_text)
        except Exception as exc:
            errors.append(f"[BROKEN JSON] {deck_file.name}: {exc}")
            continue

        try:
            words = extract_words_list(payload, deck_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if len(words) == 0:
            errors.append(f"[EMPTY DECK] {deck_file.name}: contains 0 words.")
            continue

        is_book = deck_file.name.startswith("book-") or (isinstance(payload, dict) and payload.get("group") == "book")
        book_key = "general"
        if is_book:
            book_match = re.match(r"(book-\d+)", deck_file.name)
            book_key = book_match.group(1) if book_match else "book"
            if book_key not in seen_english_per_book:
                seen_english_per_book[book_key] = {}

        for idx, entry in enumerate(words, start=1):
            if not isinstance(entry, dict):
                errors.append(f"[{deck_file.name} #{idx}] Entry is not a JSON object.")
                continue

            for field in REQUIRED_FIELDS:
                val = entry.get(field)
                if not isinstance(val, str) or not val.strip():
                    errors.append(
                        f"[{deck_file.name} #{idx}] ({entry.get('english', '<unknown>')}) "
                        f"missing or empty field '{field}'."
                    )

            en_raw = entry.get("english", "")
            if isinstance(en_raw, str) and en_raw.strip():
                en_norm = en_raw.strip().lower()
                if is_book:
                    book_seen = seen_english_per_book[book_key]
                    if en_norm in book_seen:
                        prev_deck, prev_idx = book_seen[en_norm]
                        errors.append(
                            f"[DUPLICATE IN {book_key.upper()}] '{en_raw.strip()}' in {deck_file.name} (#{idx}) "
                            f"already exists in {prev_deck} (#{prev_idx})."
                        )
                    else:
                        book_seen[en_norm] = (deck_file.name, idx)
                else:
                    if en_norm in seen_english_general:
                        prev_deck, prev_idx = seen_english_general[en_norm]
                        errors.append(
                            f"[DUPLICATE] '{en_raw.strip()}' in {deck_file.name} (#{idx}) "
                            f"already exists in {prev_deck} (#{prev_idx})."
                        )
                    else:
                        seen_english_general[en_norm] = (deck_file.name, idx)

        count = len(words)
        grp_type = "book" if is_book else "general"
        deck_summaries.append((deck_file.name, count, grp_type))
        if is_book:
            books_total += count
        else:
            general_total += count

    print("=" * 72)
    print(f"{'DECK FILE':<44} | {'TYPE':<7} | {'WORDS':>6} | {'RUNNING':>8}")
    print("-" * 72)
    running = 0
    for name, count, grp_type in deck_summaries:
        running += count
        print(f"{name:<44} | {grp_type:<7} | {count:>6} | {running:>8}")
    print("=" * 72)
    print(f"Total Decks: {len(deck_summaries)}")
    print(f"General Unique Words (Hammasi): {general_total}")
    print(f"Book Words (Kitoblar 1-4): {books_total}")
    print(f"Grand Total Words: {general_total + books_total}")
    print("=" * 72)

    if errors:
        print(f"\nVALIDATION FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors[:50]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors.", file=sys.stderr)
        raise SystemExit(1)

    if general_total < min_total:
        print(
            f"\nVALIDATION FAILED: General total is {general_total} words, "
            f"which is below the required minimum of {min_total}.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print("STATUS: ALL CHECKS PASSED (0 duplicates, 0 empty fields, valid JSON).")
    return general_total, [(name, count) for name, count, _ in deck_summaries]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all vocabulary deck JSON files.")
    parser.add_argument(
        "--min-total",
        type=int,
        default=5000,
        help="Minimum required grand total of unique general words (default: 5000).",
    )
    args = parser.parse_args()
    validate_all_decks(DECKS_DIR, min_total=args.min_total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
