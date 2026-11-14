"""
Generate challenging, thought-provoking, non-repetitive mental math decks:
1. math-01-multiplication-table.json (80 cards: 2..9 karra in strict sequence)
2. math-02-advanced-multiplication.json (1,000 cards: truly challenging, 2x2 digits, 1x3 digits, squares, non-trivial)
3. math-03-division.json (1,000 cards: 4-digit ÷ 2-digit, 3-digit ÷ 2-digit, challenging quotients)
4. math-04-addition.json (1,000 cards: 3-digit + 3-digit, multi-step carryovers)
5. math-05-subtraction.json (1,000 cards: double borrows, borrowing across zeroes)

Every deck (2..5) is thoroughly shuffled with deterministic seed so no two adjacent cards
have the same pattern or predictable answer!
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


def generate_deck_2_challenging_mult(target_count: int = 1000) -> dict:
    """Murakkab koʻpaytirish: qiyin, o'ylanadigan, turfa xil (1,000 ta misol)."""
    words = []
    seen = set()
    rng = random.Random(20261114)

    # 1. User's explicit priority examples
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

    # 2. Squares from 11^2 to 99^2 (essential mental math benchmark)
    for s in range(11, 100):
        if s % 10 != 0: # skip trivial 20x20, 30x30
            expr = f"{s} × {s}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=s * s,
                        pron_uz=f"{uz_num(s)} karra {uz_num(s)} (kvadrat)",
                        pos_label="Kvadrat sonlar • Aqliy hisob",
                        category_label="Murakkab karra",
                    )
                )

    # 3. 2-digit x 2-digit challenging non-trivial products (no ending in 0)
    # E.g. 23x47, 34x56, 48x37, 59x43, 67x28, 74x39, 86x45, 93x27
    while len(words) < 550:
        a = rng.randint(17, 98)
        b = rng.randint(17, 98)
        if a % 10 == 0 or b % 10 == 0:
            continue
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

    # 4. 1-digit x 3-digit with high digits (6, 7, 8, 9 with heavy carryovers, like 6 x 889)
    while len(words) < 850:
        a = rng.choice([6, 7, 8, 9, 4, 3])
        b = rng.randint(234, 989)
        if b % 10 == 0:
            continue
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

    # 5. 3-digit x 2-digit mental math tricks (125 x 48, 250 x 36, 150 x 84, 145 x 16)
    three_digit_bases = [125, 150, 175, 225, 250, 350, 450, 750, 120, 140, 160, 180, 240, 360]
    for base in three_digit_bases:
        for mul in range(12, 48, 2):
            if len(words) >= target_count:
                break
            expr = f"{base} × {mul}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer=base * mul,
                        pron_uz=f"{uz_num(base)} karra {uz_num(mul)}",
                        pos_label="Katta sonlar • Aqliy hisob",
                        category_label="Murakkab karra",
                    )
                )

    # Fill remaining with varied 2-digit x 2-digit
    while len(words) < target_count:
        a = rng.randint(21, 99)
        b = rng.randint(21, 99)
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

    # Crucial: SHUFFLE the deck thoroughly so adjacent cards are completely diverse and non-repetitive!
    rng.shuffle(words)
    return {
        "title": "Murakkab koʻpaytirish (Katta sonlar)",
        "category": "Murakkab karra (Katta sonlar)",
        "group": "math",
        "badge": "×+",
        "words": words[:target_count],
    }


def generate_deck_3_challenging_div(target_count: int = 1000) -> dict:
    """Murakkab boʻlish: 4 xonali va 3 xonali sonlarni 2 xonaliga bo'lish (1,000 ta misol)."""
    words = []
    seen = set()
    rng = random.Random(20261115)

    # 1. 4-digit ÷ 2-digit = 2-digit quotient (e.g. 5334 ÷ 6 = 889, 4416 ÷ 46 = 96)
    # Generate by multiplying two non-trivial 2-digit numbers
    while len(words) < 500:
        quot = rng.randint(21, 98)
        divisor = rng.randint(13, 98)
        dividend = quot * divisor
        if dividend < 1000 or dividend > 9999:
            continue
        expr = f"{dividend} ÷ {divisor}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=quot,
                    pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                    pos_label="4 xonali sonni boʻlish",
                    category_label="Boʻlish",
                )
            )

    # 2. 3-digit ÷ 2-digit = 2-digit quotient (e.g. 864 ÷ 24 = 36, 952 ÷ 28 = 34, 756 ÷ 27 = 28)
    while len(words) < 800:
        quot = rng.randint(14, 49)
        divisor = rng.randint(12, 48)
        dividend = quot * divisor
        if dividend < 150 or dividend > 999:
            continue
        expr = f"{dividend} ÷ {divisor}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=quot,
                    pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                    pos_label="3 xonali sonni boʻlish",
                    category_label="Boʻlish",
                )
            )

    # 3. 3-digit ÷ 1-digit with challenging carryovers (e.g. 679 ÷ 7 = 97, 864 ÷ 9 = 96)
    while len(words) < 950:
        divisor = rng.choice([6, 7, 8, 9, 3])
        quot = rng.randint(45, 145)
        dividend = divisor * quot
        if dividend < 200 or dividend > 999:
            continue
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

    # 4. Large round quotients (e.g. 7200 ÷ 48 = 150, 12500 ÷ 25 = 500)
    round_divisors = [15, 16, 18, 24, 25, 32, 36, 45, 48, 54, 64, 75, 125, 250]
    while len(words) < target_count:
        divisor = rng.choice(round_divisors)
        quot = rng.choice([25, 35, 45, 55, 65, 75, 125, 150, 250, 350])
        dividend = divisor * quot
        expr = f"{dividend} ÷ {divisor}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=quot,
                    pron_uz=f"{uz_num(dividend)} boʻlingan {uz_num(divisor)}",
                    pos_label="Katta sonlarni boʻlish",
                    category_label="Boʻlish",
                )
            )

    rng.shuffle(words)
    return {
        "title": "Boʻlish (Jadval & Aqliy hisoblash)",
        "category": "Boʻlish (Jadval & Aqliy hisoblash)",
        "group": "math",
        "badge": "÷",
        "words": words[:target_count],
    }


def generate_deck_4_challenging_add(target_count: int = 1000) -> dict:
    """Murakkab qo'shish: 3 xonali va 4 xonali sonlar, ko'p bosqichli o'tishlar (1,000 ta misol)."""
    words = []
    seen = set()
    rng = random.Random(20261116)

    # 1. 3-digit + 3-digit with double and triple carryovers (e.g. 478 + 389 = 867, 769 + 584 = 1353)
    while len(words) < 600:
        a = rng.randint(245, 989)
        b = rng.randint(245, 989)
        # ensure carryover in tens or ones
        if (a % 10 + b % 10 < 10) and ((a // 10) % 10 + (b // 10) % 10 < 10):
            continue
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a + b,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="3 xonali sonlarni qoʻshish",
                    category_label="Qoʻshish",
                )
            )

    # 2. 4-digit + 3-digit and 4-digit + 4-digit (e.g. 1475 + 889 = 2364, 2685 + 1758 = 4443)
    while len(words) < 850:
        a = rng.randint(1150, 4890)
        b = rng.randint(280, 2890)
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a + b,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="Katta sonlarni qoʻshish",
                    category_label="Qoʻshish",
                )
            )

    # 3. 2-digit + 2-digit with high digits (7, 8, 9 with carryovers) (e.g. 87 + 98 = 185)
    while len(words) < target_count:
        a = rng.randint(48, 99)
        b = rng.randint(48, 99)
        expr = f"{a} + {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a + b,
                    pron_uz=f"{uz_num(a)} qoʻshuv {uz_num(b)}",
                    pos_label="2 xonali sonlarni qoʻshish",
                    category_label="Qoʻshish",
                )
            )

    rng.shuffle(words)
    return {
        "title": "Qoʻshish (Tezkor aqliy hisoblash)",
        "category": "Qoʻshish (Tezkor aqliy hisoblash)",
        "group": "math",
        "badge": "+",
        "words": words[:target_count],
    }


def generate_deck_5_challenging_sub(target_count: int = 1000) -> dict:
    """Murakkab ayirish: qarz olishlar, nollar orqali o'tish, 3 va 4 xonali sonlar (1,000 ta misol)."""
    words = []
    seen = set()
    rng = random.Random(20261117)

    # 1. 3-digit - 3-digit with double borrows (e.g. 612 - 278 = 334, 823 - 487 = 336)
    while len(words) < 500:
        a = rng.randint(340, 995)
        b = rng.randint(125, a - 25)
        # ensure borrowing happens: ones of a < ones of b or tens of a < tens of b
        if (a % 10 >= b % 10) and ((a // 10) % 10 >= (b // 10) % 10):
            continue
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a - b,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="3 xonali sonlarni ayirish",
                    category_label="Ayirish",
                )
            )

    # 2. Borrowing across zeros (e.g. 2034 - 789 = 1245, 3021 - 1658 = 1363, 5003 - 2769 = 2234)
    while len(words) < 800:
        thousands = rng.randint(2, 6) * 1000
        a = thousands + rng.randint(1, 45) # e.g. 2005, 3012, 4034
        b = rng.randint(245, a - 250)
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a - b,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="Nollar orqali ayirish",
                    category_label="Ayirish",
                )
            )

    # 3. 3-digit - 2-digit with double borrow (e.g. 314 - 78 = 236, 503 - 68 = 435)
    while len(words) < target_count:
        a = rng.randint(125, 940)
        b = rng.randint(38, 98)
        if a <= b or (a % 10 >= b % 10):
            continue
        expr = f"{a} − {b}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer=a - b,
                    pron_uz=f"{uz_num(a)} ayiruv {uz_num(b)}",
                    pos_label="Qarz olib ayirish",
                    category_label="Ayirish",
                )
            )

    rng.shuffle(words)
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
    deck2 = generate_deck_2_challenging_mult(1000)
    deck3 = generate_deck_3_challenging_div(1000)
    deck4 = generate_deck_4_challenging_add(1000)
    deck5 = generate_deck_5_challenging_sub(1000)

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
    print(f"Total Challenging Math Cards: {total}")


if __name__ == "__main__":
    main()
