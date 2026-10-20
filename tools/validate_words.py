"""
Validate all deck JSON files in webapp/data/decks/*.json.

Checks:
- Valid JSON syntax in every deck file
- Every entry has non-empty string fields:
  english, pronunciation_uz, uzbek, pos, example_en, example_uz, category
- Zero duplicate English words (case-insensitive) within a deck or across all decks
- Prints per-deck word counts and the grand total
- Exits with non-zero status on any validation error (or if total < min_total)
"""

from __future__ import annotations

import argparse
import json
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

    seen_english: dict[str, tuple[str, int]] = {}
    deck_summaries: list[tuple[str, int]] = []
    errors: list[str] = []
    grand_total = 0

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
                if en_norm in seen_english:
                    prev_deck, prev_idx = seen_english[en_norm]
                    errors.append(
                        f"[DUPLICATE] '{en_raw.strip()}' in {deck_file.name} (#{idx}) "
                        f"already exists in {prev_deck} (#{prev_idx})."
                    )
                else:
                    seen_english[en_norm] = (deck_file.name, idx)

        count = len(words)
        deck_summaries.append((deck_file.name, count))
        grand_total += count

    print("=" * 68)
    print(f"{'DECK FILE':<44} | {'WORDS':>8} | {'RUNNING':>10}")
    print("-" * 68)
    running = 0
    for name, count in deck_summaries:
        running += count
        print(f"{name:<44} | {count:>8} | {running:>10}")
    print("=" * 68)
    print(f"Total Decks: {len(deck_summaries)}")
    print(f"Grand Total Unique Words: {grand_total}")
    print("=" * 68)

    if errors:
        print(f"\nVALIDATION FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors[:50]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors.", file=sys.stderr)
        raise SystemExit(1)

    if grand_total < min_total:
        print(
            f"\nVALIDATION FAILED: Grand total is {grand_total} words, "
            f"which is below the required minimum of {min_total}.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print("STATUS: ALL CHECKS PASSED (0 duplicates, 0 empty fields, valid JSON).")
    return grand_total, deck_summaries


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all vocabulary deck JSON files.")
    parser.add_argument(
        "--min-total",
        type=int,
        default=5000,
        help="Minimum required grand total of unique words (default: 5000).",
    )
    args = parser.parse_args()
    validate_all_decks(DECKS_DIR, min_total=args.min_total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
