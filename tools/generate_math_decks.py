"""
Generate 5 structured Math decks for flashcard practice:
1. math-01-multiplication-table.json (Karra jadvali: 2 dan 9 gacha ketma-ket, 80 ta)
2. math-02-advanced-multiplication.json (Murakkab karra: katta sonlar, aqliy hisob, 200 ta)
3. math-03-division.json (Bo'lish: jadval va aqliy hisob, 150 ta)
4. math-04-addition.json (Qo'shish: tezkor aqliy hisob, 150 ta)
5. math-05-subtraction.json (Ayirish: tezkor aqliy hisob, 150 ta)
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
    """Karra jadvali 2 dan 9 gacha, har biri 1 dan 10 gacha ketma-ket (80 ta misol)."""
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


def generate_deck_2_advanced_mult() -> dict:
    """Murakkab koʻpaytirish: katta sonlar, aqliy hisoblash (200 ta misol)."""
    words = []
    seen = set()

    # User's explicit examples
    specific = [
        (2, 35),
        (6, 889),
        (3, 45),
        (4, 25),
        (5, 64),
        (7, 35),
        (8, 125),
        (12, 15),
        (15, 15),
        (25, 25),
        (16, 25),
        (14, 50),
        (4, 125),
        (8, 25),
        (9, 75),
    ]

    for a, b in specific:
        expr = f"{a} × {b}"
        if expr in seen:
            continue
        seen.add(expr)
        ans = a * b
        pron = f"{uz_num(a)} karra {uz_num(b)}"
        words.append(
            build_card(
                expression=expr,
                answer=ans,
                pron_uz=pron,
                pos_label="Murakkab karra • Aqliy hisob",
                category_label="Murakkab karra",
            )
        )

    # 1-digit by 2-digit practical pairs
    single_digits = [2, 3, 4, 5, 6, 7, 8, 9]
    two_digits = [
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30,
        32, 35, 36, 40, 42, 45, 48, 50, 55, 60, 64, 65, 70, 75, 80, 85, 90, 95, 99
    ]
    for a in single_digits:
        for b in two_digits:
            expr = f"{a} × {b}"
            if expr not in seen:
                seen.add(expr)
                ans = a * b
                words.append(
                    build_card(
                        expression=expr,
                        answer=ans,
                        pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                        pos_label="Murakkab karra • Aqliy hisob",
                        category_label="Murakkab karra",
                    )
                )

    # 1-digit by 3-digit round and nice numbers
    three_digits = [
        105, 110, 115, 120, 125, 130, 140, 150, 160, 175, 200, 220, 250, 300,
        333, 350, 400, 450, 500, 600, 700, 750, 800, 888, 900
    ]
    for a in [2, 3, 4, 5, 6, 7, 8]:
        for b in three_digits:
            expr = f"{a} × {b}"
            if expr not in seen and len(words) < 170:
                seen.add(expr)
                ans = a * b
                words.append(
                    build_card(
                        expression=expr,
                        answer=ans,
                        pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                        pos_label="Katta sonlar • Aqliy hisob",
                        category_label="Murakkab karra",
                    )
                )

    # 2-digit by 2-digit (squares and round products)
    squares = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 30, 35, 40, 45, 50]
    for s in squares:
        expr = f"{s} × {s}"
        if expr not in seen:
            seen.add(expr)
            ans = s * s
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(s)} karra {uz_num(s)} (kvadrat)",
                    pos_label="Kvadrat sonlar",
                    category_label="Murakkab karra",
                )
            )

    two_by_two = [
        (11, 12), (12, 13), (12, 14), (12, 15), (14, 15), (15, 16), (15, 18),
        (15, 20), (16, 20), (18, 20), (20, 25), (20, 30), (20, 35), (20, 45),
        (25, 30), (25, 40), (25, 50), (30, 40), (30, 50), (40, 50)
    ]
    for a, b in two_by_two:
        expr = f"{a} × {b}"
        if expr not in seen:
            seen.add(expr)
            ans = a * b
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(a)} karra {uz_num(b)}",
                    pos_label="2 xonali sonlar",
                    category_label="Murakkab karra",
                )
            )

    # Trim or ensure exactly 200 words
    words = words[:200]
    return {
        "title": "Murakkab koʻpaytirish (Katta sonlar)",
        "category": "Murakkab karra (Katta sonlar)",
        "group": "math",
        "badge": "×+",
        "words": words,
    }


def generate_deck_3_division() -> dict:
    """Bo'lish: jadval va aqliy hisoblash (150 ta misol)."""
    words = []
    seen = set()

    # Table division (2 to 9)
    for divisor in range(2, 10):
        for quot in range(1, 11):
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

    # Advanced mental division (larger numbers)
    adv_pairs = [
        (100, 4), (100, 5), (120, 3), (120, 4), (120, 6), (144, 12), (150, 3),
        (150, 5), (160, 4), (180, 6), (180, 9), (200, 4), (200, 5), (200, 8),
        (225, 15), (240, 6), (240, 8), (250, 5), (250, 25), (270, 9), (300, 5),
        (300, 6), (320, 8), (350, 7), (360, 6), (360, 12), (400, 8), (400, 25),
        (450, 9), (480, 6), (500, 10), (500, 20), (500, 25), (600, 12), (600, 20),
        (625, 25), (640, 8), (700, 7), (720, 8), (720, 9), (750, 25), (800, 16),
        (800, 25), (810, 9), (880, 8), (900, 30), (1000, 2), (1000, 4), (1000, 5),
        (1000, 8), (1000, 10), (1000, 20), (1000, 25), (1000, 50), (1200, 4),
        (1200, 6), (1500, 5), (1600, 4), (2000, 4), (2000, 5), (2500, 50),
        (3000, 6), (3600, 60), (4000, 8), (5000, 50), (5334, 6), (10000, 100)
    ]

    for dividend, divisor in adv_pairs:
        expr = f"{dividend} ÷ {divisor}"
        if expr not in seen and len(words) < 150:
            seen.add(expr)
            quot = dividend // divisor
            words.append(
                build_card(
                    expression=expr,
                    answer=quot,
                    pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                    pos_label="Aqliy boʻlish amali",
                    category_label="Boʻlish",
                )
            )

    # Pad to 150 if needed
    extra_divisors = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 50]
    extra_quots = [15, 18, 22, 24, 28, 32, 35, 42, 45, 48, 55, 65, 75, 85, 95]
    for d in extra_divisors:
        for q in extra_quots:
            if len(words) >= 150:
                break
            dividend = d * q
            expr = f"{dividend} ÷ {d}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=q,
                        pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(d)}",
                        pos_label="Aqliy boʻlish amali",
                        category_label="Boʻlish",
                    )
                )

    words = words[:150]
    return {
        "title": "Boʻlish (Jadval & Aqliy hisoblash)",
        "category": "Boʻlish (Jadval & Aqliy hisoblash)",
        "group": "math",
        "badge": "÷",
        "words": words,
    }


def generate_deck_4_addition() -> dict:
    """Qo'shish: tezkor aqliy hisoblash (150 ta misol)."""
    words = []
    seen = set()

    # Practical 2-digit + 2-digit additions
    add_pairs = [
        (15, 28), (27, 36), (38, 45), (47, 38), (56, 78), (69, 47), (88, 49),
        (79, 86), (95, 68), (34, 57), (46, 68), (58, 74), (67, 85), (78, 93),
        (25, 38), (48, 35), (89, 54), (64, 49), (57, 65), (76, 58), (87, 46),
        (94, 38), (63, 79), (72, 89), (85, 96), (49, 73), (53, 88), (66, 77),
        (18, 45), (29, 63), (37, 54), (48, 67), (59, 72), (68, 83), (74, 59),
        # Rounding helpers to 100
        (75, 25), (65, 35), (55, 45), (85, 15), (95, 5), (68, 32), (74, 26),
        (58, 42), (63, 37), (71, 29), (83, 17), (77, 23), (89, 11), (92, 8),
        # 3-digit + 2-digit
        (125, 75), (145, 55), (168, 32), (185, 45), (235, 65), (275, 45), (345, 55),
        (380, 45), (425, 75), (480, 25), (520, 80), (565, 35), (615, 85), (680, 40),
        (725, 75), (790, 30), (845, 55), (875, 25), (910, 90), (950, 50),
        # 3-digit + 3-digit
        (125, 125), (150, 150), (175, 125), (225, 175), (240, 380), (250, 250),
        (275, 225), (320, 280), (345, 180), (350, 270), (375, 125), (420, 380),
        (450, 350), (475, 125), (520, 480), (550, 450), (580, 220), (620, 380),
        (650, 350), (675, 225), (680, 320), (720, 280), (750, 250), (775, 125),
        (820, 180), (850, 150), (880, 120), (950, 150), (1200, 800), (1500, 1500)
    ]

    for a, b in add_pairs:
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            ans = a + b
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="Qoʻshish amali",
                    category_label="Qoʻshish",
                )
            )

    # Generate more until 150
    random.seed(42)
    while len(words) < 150:
        a = random.randint(21, 98)
        b = random.randint(21, 98)
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            ans = a + b
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="Qoʻshish • Aqliy hisob",
                    category_label="Qoʻshish",
                )
            )

    return {
        "title": "Qoʻshish (Tezkor aqliy hisoblash)",
        "category": "Qoʻshish (Tezkor aqliy hisoblash)",
        "group": "math",
        "badge": "+",
        "words": words,
    }


def generate_deck_5_subtraction() -> dict:
    """Ayirish: tezkor aqliy hisoblash (150 ta misol)."""
    words = []
    seen = set()

    sub_pairs = [
        # Subtracting from tens & 100
        (50, 18), (60, 27), (70, 34), (80, 46), (90, 53),
        (100, 17), (100, 24), (100, 37), (100, 43), (100, 48), (100, 55),
        (100, 64), (100, 73), (100, 82), (100, 85), (100, 91),
        # 2-digit - 2-digit with borrow
        (75, 28), (84, 39), (92, 47), (95, 58), (63, 27), (72, 38), (81, 45),
        (94, 56), (83, 47), (71, 35), (65, 29), (54, 28), (86, 49), (93, 67),
        # Subtracting from 150, 200, 300, 500
        (125, 68), (150, 68), (150, 75), (180, 95), (200, 45), (200, 75),
        (200, 135), (200, 168), (250, 75), (250, 125), (300, 145), (300, 185),
        (350, 175), (400, 160), (400, 245), (450, 180), (500, 185), (500, 260),
        (500, 345), (600, 275), (600, 350), (700, 340), (750, 280), (800, 375),
        # Subtracting from 1000
        (1000, 125), (1000, 250), (1000, 345), (1000, 375), (1000, 450),
        (1000, 550), (1000, 625), (1000, 680), (1000, 750), (1000, 850)
    ]

    for a, b in sub_pairs:
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            ans = a - b
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="Ayirish amali",
                    category_label="Ayirish",
                )
            )

    # Generate more until 150
    random.seed(99)
    while len(words) < 150:
        a = random.randint(35, 150)
        b = random.randint(11, a - 5)
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            ans = a - b
            words.append(
                build_card(
                    expression=expr,
                    answer=ans,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="Ayirish • Aqliy hisob",
                    category_label="Ayirish",
                )
            )

    return {
        "title": "Ayirish (Tezkor aqliy hisoblash)",
        "category": "Ayirish (Tezkor aqliy hisoblash)",
        "group": "math",
        "badge": "−",
        "words": words,
    }


def main():
    root = Path(__file__).resolve().parent.parent
    decks_dir = root / "webapp" / "data" / "decks"
    decks_dir.mkdir(parents=True, exist_ok=True)

    deck1 = generate_deck_1_table()
    deck2 = generate_deck_2_advanced_mult()
    deck3 = generate_deck_3_division()
    deck4 = generate_deck_4_addition()
    deck5 = generate_deck_5_subtraction()

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
