"""
Generate rich, diverse Math decks for flashcard practice:
1. math-01-multiplication-table.json (80 cards: 2..9 karra ketma-ket)
2. math-02-advanced-multiplication.json (1,000 cards: katta sonlar, aqliy hisob)
3. math-03-division.json (1,000 cards: bo'lish amallari, qoldiqsiz)
4. math-04-addition.json (1,000 cards: 2 va 3 xonali aqliy qo'shish)
5. math-05-subtraction.json (1,000 cards: 2 va 3 xonali aqliy ayirish)

Total: 4,080 high-quality cards.
"""

from __future__ import annotations
import json
import random
from pathlib import Path

ONES = ["", "bir", "ikki", "uch", "toʻrt", "besh", "olti", "yetti", "sakkiz", "toʻqqiz"]
TENS = ["", "oʻn", "yigirma", "oʻttiz", "qirq", "ellik", "oltmish", "yetmish", "sakson", "toʻqson"]

def uz_num(n: int) -> str:
    if n == 0:
        return "nol"
    if n < 0:
        return "minus " + uz_num(-n)
    parts = []
    if n >= 1000000:
        mil = n // 1000000
        n %= 1000000
        parts.append("bir million" if mil == 1 else uz_num(mil) + " million")
    if n >= 1000:
        th = n // 1000
        n %= 1000
        parts.append("ming" if th == 1 else uz_num(th) + " ming")
    if n >= 100:
        h = n // 100
        n %= 100
        parts.append("yuz" if h == 1 else ONES[h] + " yuz")
    if n >= 10:
        t = n // 10
        n %= 10
        parts.append(TENS[t])
    if n > 0:
        parts.append(ONES[n])
    return " ".join(p for p in parts if p)


def build_card(expression: str, answer: int, pron_uz: str, pos_label: str, category_label: str) -> dict[str, str]:
    ans_str = str(answer)
    ans_uz = uz_num(answer)
    return {
        "english": f"{expression} = ?",
        "ipa": "",
        "pronunciation_uz": pron_uz,
        "uzbek": ans_str,
        "pos": pos_label,
        "example_en": f"{expression} = {ans_str}",
        "example_uz": f"{expression} = {ans_str} ({pron_uz.capitalize()} — {ans_uz})",
        "category": category_label,
    }


def generate_deck_1_table() -> dict:
    """Karra jadvali 2 dan 9 gacha ketma-ket (80 ta misol)."""
    words = []
    for a in range(2, 10):
        for b in range(1, 11):
            expr = f"{a} × {b}"
            ans = a * b
            pron = f"{uz_num(a)} karra {uz_num(b)}"
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=pron,
                    pos_label=f"Koʻpaytirish • {a} karra",
                    category_label="Karra jadvali",
                )
            )
    return {
        "title": "Karra jadvali (2 dan 9 gacha)",
        "category": "Karra jadvali (2 dan 9 gacha)",
        "group": "math",
        "badge": "2-9",
        "words": words,
    }


def generate_deck_2_advanced_mult(target_count: int = 1000) -> dict:
    """Murakkab koʻpaytirish (1,000 ta misol)."""
    words = []
    seen = set()

    # User's explicit examples first
    priority_pairs = [
        (2, 35), (6, 889), (3, 45), (4, 25), (5, 64), (7, 35), (8, 125),
        (12, 15), (15, 15), (25, 25), (16, 25), (14, 50), (4, 125), (8, 25), (9, 75)
    ]
    for a, b in priority_pairs:
        expr = f"{a} × {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a * b,
                    pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                    pos_label="Murakkab karra • Aqliy hisob",
                    category_label="Murakkab karra",
                )
            )

    # 1. Squares: 11..50
    for s in range(11, 51):
        expr = f"{s} × {s}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=s * s,
                    pron_uz=f"{uz_num(s)} karra {uz_num(s)} (kvadrat)",
                    pos_label="Kvadrat sonlar",
                    category_label="Murakkab karra",
                )
            )

    # 2. 1-digit x 2-digit (2..9 x 11..99)
    for a in range(2, 10):
        for b in range(11, 100):
            expr = f"{a} × {b}"
            if expr not in seen and len(words) < target_count:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=a * b,
                        pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                        pos_label="Murakkab karra • 2 xonali",
                        category_label="Murakkab karra",
                    )
                )

    # 3. 2-digit x 2-digit practical pairs (ending in 0, 5, or easy mental math)
    two_digit_bases = [12, 14, 15, 16, 18, 20, 22, 24, 25, 28, 30, 32, 35, 40, 45, 50, 60, 75]
    for a in two_digit_bases:
        for b in range(11, 51):
            if len(words) >= target_count:
                break
            expr = f"{a} × {b}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=a * b,
                        pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                        pos_label="Murakkab karra • 2 xonali",
                        category_label="Murakkab karra",
                    )
                )

    # 4. 1-digit x 3-digit (like user's 6 x 889)
    rng = random.Random(12345)
    while len(words) < target_count:
        a = rng.randint(2, 9)
        b = rng.randint(101, 999)
        expr = f"{a} × {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a * b,
                    pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                    pos_label="Katta sonlar • 3 xonali",
                    category_label="Murakkab karra",
                )
            )

    return {
        "title": "Murakkab koʻpaytirish (Katta sonlar)",
        "category": "Murakkab karra (Katta sonlar)",
        "group": "math",
        "badge": "×+",
        "words": words[:target_count],
    }


def generate_deck_3_division(target_count: int = 1000) -> dict:
    """Bo'lish: jadval va aqliy hisoblash (1,000 ta misol)."""
    words = []
    seen = set()

    # 1. Multiplication table division (2..12)
    for divisor in range(2, 13):
        for quot in range(1, 21):
            dividend = divisor * quot
            expr = f"{dividend} ÷ {divisor}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=quot,
                        pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                        pos_label=f"Boʻlish • {divisor} ga boʻlish",
                        category_label="Boʻlish",
                    )
                )

    # 2. 2-digit and 3-digit by 2..20
    for divisor in range(2, 21):
        for quot in range(11, 60):
            if len(words) >= target_count:
                break
            dividend = divisor * quot
            expr = f"{dividend} ÷ {divisor}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=quot,
                        pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                        pos_label="Aqliy boʻlish amali",
                        category_label="Boʻlish",
                    )
                )

    # 3. Dividing round numbers and practical dividends
    divisors_pool = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 250]
    rng = random.Random(54321)
    while len(words) < target_count:
        divisor = rng.choice(divisors_pool)
        quot = rng.randint(5, 250)
        dividend = divisor * quot
        expr = f"{dividend} ÷ {divisor}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=quot,
                    pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                    pos_label="Aqliy boʻlish amali",
                    category_label="Boʻlish",
                )
            )

    return {
        "title": "Boʻlish (Jadval & Aqliy hisoblash)",
        "category": "Boʻlish (Jadval & Aqliy hisoblash)",
        "group": "math",
        "badge": "÷",
        "words": words[:target_count],
    }


def generate_deck_4_addition(target_count: int = 1000) -> dict:
    """Qo'shish: tezkor aqliy hisoblash (1,000 ta misol)."""
    words = []
    seen = set()

    # 1. 2-digit + 2-digit with carryover
    for a in range(15, 95, 2):
        for b in range(16, 96, 3):
            if len(words) >= 400:
                break
            expr = f"{a} + {b}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=a + b,
                        pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                        pos_label="Qoʻshish • 2 xonali",
                        category_label="Qoʻshish",
                    )
                )

    # 2. 3-digit + 2-digit
    for a in range(105, 980, 15):
        for b in range(15, 95, 7):
            if len(words) >= 700:
                break
            expr = f"{a} + {b}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=a + b,
                        pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                        pos_label="Qoʻshish • 3 xonali",
                        category_label="Qoʻshish",
                    )
                )

    # 3. 3-digit + 3-digit (various sums up to 2000)
    rng = random.Random(67890)
    while len(words) < target_count:
        a = rng.randint(110, 890)
        b = rng.randint(110, 890)
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a + b,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="Qoʻshish • Katta sonlar",
                    category_label="Qoʻshish",
                )
            )

    return {
        "title": "Qoʻshish (Tezkor aqliy hisoblash)",
        "category": "Qoʻshish (Tezkor aqliy hisoblash)",
        "group": "math",
        "badge": "+",
        "words": words[:target_count],
    }


def generate_deck_5_subtraction(target_count: int = 1000) -> dict:
    """Ayirish: tezkor aqliy hisoblash (1,000 ta misol)."""
    words = []
    seen = set()

    # 1. Subtracting from 100, 200, 500, 1000
    round_bases = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000]
    for base in round_bases:
        for subt in range(15, min(base, 100), 3):
            if len(words) >= 250:
                break
            expr = f"{base} − {subt}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=base - subt,
                        pron_uz=f"{uz_num(base)} ayiruv {uz_num(subt)}",
                        pos_label="Ayirish • Yaxlit sonlar",
                        category_label="Ayirish",
                    )
                )

    # 2. 2-digit - 2-digit with borrow
    for a in range(35, 100):
        for b in range(16, a - 5, 2):
            if len(words) >= 550:
                break
            expr = f"{a} − {b}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=a - b,
                        pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                        pos_label="Ayirish • 2 xonali",
                        category_label="Ayirish",
                    )
                )

    # 3. 3-digit - 2-digit and 3-digit - 3-digit
    rng = random.Random(13579)
    while len(words) < target_count:
        a = rng.randint(150, 1200)
        b = rng.randint(25, a - 10)
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a - b,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="Ayirish • Katta sonlar",
                    category_label="Ayirish",
                )
            )

    return {
        "title": "Ayirish (Tezkor aqliy hisoblash)",
        "category": "Ayirish (Tezkor aqliy hisoblash)",
        "group": "math",
        "badge": "−",
        "words": words[:target_count],
    }


def main():
    root = Path(__file__).resolve().parent.parent
    decks_dir = root / "webapp" / "data" / "decks"
    decks_dir.mkdir(parents=True, exist_ok=True)

    deck1 = generate_deck_1_table()
    deck2 = generate_deck_2_advanced_mult(1000)
    deck3 = generate_deck_3_division(1000)
    deck4 = generate_deck_4_addition(1000)
    deck5 = generate_deck_5_subtraction(1000)

    decks = [
        ("math-01-multiplication-table.json", deck1),
        ("math-02-advanced-multiplication.json", deck2),
        ("math-03-division.json", deck3),
        ("math-04-addition.json", deck4),
        ("math-05-subtraction.json", deck5),
    ]

    for filename, payload in decks:
        path = decks_dir / filename
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Generated {filename}: {len(payload['words'])} cards")

    total = sum(len(p['words']) for _, p in decks)
    print(f"Total Math Cards Generated: {total}")


if __name__ == "__main__":
    main()
