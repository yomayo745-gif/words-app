"""
Generate 3 new rich Math decks:
1. math-06-percentages.json (1,000 cards: Foizlar • Tezkor aqliy hisoblash)
2. math-07-roots-and-powers.json (1,000 cards: Ildizlar va Darajalar)
3. math-08-fractions.json (1,000 cards: Kasrlar • Oddiy va o'nlik kasrlar)

Total: 3,000 cards.
"""

from __future__ import annotations
import json
import math
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"

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


def build_card(expression: str, answer_str: str, pron_uz: str, pos_label: str, category_label: str, example_uz: str) -> dict[str, str]:
    return {
        "english": f"{expression} = ?",
        "ipa": "",
        "pronunciation_uz": pron_uz,
        "uzbek": answer_str,
        "pos": pos_label,
        "example_en": f"{expression} = {answer_str}",
        "example_uz": example_uz,
        "category": category_label,
    }


def generate_deck_6_percentages(target_count: int = 1000) -> dict:
    words = []
    seen = set()
    rng = random.Random(20261120)

    # 1. 25%, 50%, 75%
    for pct in [25, 50, 75]:
        div = 4 if pct in (25, 75) else 2
        for base in range(20, 4000, 4 if div == 4 else 10):
            if (base * pct) % 100 != 0:
                continue
            ans = (base * pct) // 100
            expr = f"{base} ning {pct}% i"
            if expr not in seen and len(words) < 250:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer_str=str(ans),
                        pron_uz=f"{uz_num(base)}ning {uz_num(pct)} foizi",
                        pos_label="Asosiy foizlar • Aqliy hisob",
                        category_label="Foizlar (Aqliy hisoblash)",
                        example_uz=f"{base} ning {pct}% i = {ans} ({uz_num(base).capitalize()}ning {uz_num(pct)} foizi — {uz_num(ans)})",
                    )
                )

    # 2. 10%, 20%, 30%, 40%, 60%, 70%, 80%, 90%
    while len(words) < 550:
        pct = rng.choice([10, 20, 30, 40, 60, 70, 80, 90])
        base = rng.randint(4, 500) * 10
        if (base * pct) % 100 != 0:
            continue
        ans = (base * pct) // 100
        expr = f"{base} ning {pct}% i"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(ans),
                    pron_uz=f"{uz_num(base)}ning {uz_num(pct)} foizi",
                    pos_label="Oʻnlik foizlar • Aqliy hisob",
                    category_label="Foizlar (Aqliy hisoblash)",
                    example_uz=f"{base} ning {pct}% i = {ans} ({uz_num(base).capitalize()}ning {uz_num(pct)} foizi — {uz_num(ans)})",
                )
            )

    # 3. 5%, 15%, 35%, 45%, 55%, 65%, 85%, 95%
    while len(words) < 800:
        pct = rng.choice([5, 15, 35, 45, 55, 65, 85, 95])
        base = rng.randint(4, 350) * 20
        if (base * pct) % 100 != 0:
            continue
        ans = (base * pct) // 100
        expr = f"{base} ning {pct}% i"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(ans),
                    pron_uz=f"{uz_num(base)}ning {uz_num(pct)} foizi",
                    pos_label="Murakkab foizlar",
                    category_label="Foizlar (Aqliy hisoblash)",
                    example_uz=f"{base} ning {pct}% i = {ans} ({uz_num(base).capitalize()}ning {uz_num(pct)} foizi — {uz_num(ans)})",
                )
            )

    # 4. 2%, 3%, 4%, 6%, 7%, 8%, 9%, 12%, 14%, 16%, 18%, 24%, 32%
    while len(words) < target_count:
        pct = rng.choice([2, 3, 4, 6, 7, 8, 9, 12, 14, 16, 18, 24, 32, 45])
        base = rng.randint(2, 150) * (50 if pct % 2 == 0 else 100)
        if (base * pct) % 100 != 0:
            continue
        ans = (base * pct) // 100
        expr = f"{base} ning {pct}% i"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(ans),
                    pron_uz=f"{uz_num(base)}ning {uz_num(pct)} foizi",
                    pos_label="Tezkor aqliy foiz",
                    category_label="Foizlar (Aqliy hisoblash)",
                    example_uz=f"{base} ning {pct}% i = {ans} ({uz_num(base).capitalize()}ning {uz_num(pct)} foizi — {uz_num(ans)})",
                )
            )

    rng.shuffle(words)
    return {
        "title": "Foizlar (Tezkor aqliy hisoblash)",
        "category": "Foizlar (Aqliy hisoblash)",
        "group": "math",
        "badge": "%",
        "words": words,
    }


def to_superscript(n: int) -> str:
    mapping = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    return "".join(mapping[c] for c in str(n))


def generate_deck_7_roots_powers(target_count: int = 1000) -> dict:
    words = []
    seen = set()
    rng = random.Random(20261121)

    # 1. Square roots: √16 to √10000
    for r in range(4, 101):
        x = r * r
        expr = f"√{x}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(r),
                    pron_uz=f"ildiz ostida {uz_num(x)}",
                    pos_label="Kvadrat ildiz",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"√{x} = {r} (Ildiz ostida {uz_num(x)} — {uz_num(r)})",
                )
            )

    # 2. Cube roots: ∛8 to ∛42875 (2^3 to 35^3)
    for c in range(2, 36):
        x = c * c * c
        expr = f"∛{x}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(c),
                    pron_uz=f"kub ildiz ostida {uz_num(x)}",
                    pos_label="Kub ildiz",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"∛{x} = {c} (Kub ildiz ostida {uz_num(x)} — {uz_num(c)})",
                )
            )

    # 3. Powers of 2: 2^1 to 2^16
    for p in range(1, 17):
        ans = 2 ** p
        expr = f"2{to_superscript(p)}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(ans),
                    pron_uz=f"ikkininig {uz_num(p)}-darajasi",
                    pos_label="2 ning darajalari",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"2{to_superscript(p)} = {ans} (Ikkininig {uz_num(p)}-darajasi — {uz_num(ans)})",
                )
            )

    # 4. Powers of 3, 4, 5, 6, 7, 8, 9, 10
    powers_table = [
        (3, range(2, 9)),
        (4, range(2, 7)),
        (5, range(2, 7)),
        (6, range(2, 5)),
        (7, range(2, 5)),
        (8, range(2, 5)),
        (9, range(2, 5)),
        (10, range(2, 7)),
        (11, [2, 3]),
        (12, [2, 3]),
        (13, [2, 3]),
        (14, [2]),
        (15, [2, 3]),
        (16, [2]),
        (20, [2, 3, 4]),
        (25, [2, 3]),
        (30, [2, 3]),
        (40, [2, 3]),
        (50, [2, 3]),
    ]
    for base, p_range in powers_table:
        for p in p_range:
            ans = base ** p
            expr = f"{base}{to_superscript(p)}"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer_str=str(ans),
                        pron_uz=f"{uz_num(base)}ning {uz_num(p)}-darajasi",
                        pos_label="Darajaga koʻtarish",
                        category_label="Ildizlar va Darajalar",
                        example_uz=f"{base}{to_superscript(p)} = {ans} ({uz_num(base).capitalize()}ning {uz_num(p)}-darajasi — {uz_num(ans)})",
                    )
                )

    # 5. Squares of 2-digit numbers: 11^2 to 99^2
    for n in range(11, 100):
        if n % 10 != 0:
            ans = n * n
            expr = f"{n}²"
            if expr not in seen:
                seen.add(expr)
                words.append(
                    build_card(
                        expression=expr,
                        answer_str=str(ans),
                        pron_uz=f"{uz_num(n)}ning kvadrati",
                        pos_label="Kvadrat sonlar",
                        category_label="Ildizlar va Darajalar",
                        example_uz=f"{n}² = {ans} ({uz_num(n).capitalize()}ning kvadrati — {uz_num(ans)})",
                    )
                )

    # 6. Pythagorean and Power mental arithmetic: a² + b² = c², a² - b²
    pythagorean_triplets = [
        (3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17),
        (12, 16, 20), (7, 24, 25), (10, 24, 26), (20, 21, 29), (12, 35, 37),
        (9, 40, 41), (15, 20, 25), (14, 48, 50), (18, 24, 30), (16, 30, 34),
        (21, 28, 35), (11, 60, 61), (13, 84, 85), (36, 77, 85), (39, 80, 89)
    ]
    for a, b, c in pythagorean_triplets:
        # a² + b²
        expr1 = f"{a}² + {b}²"
        if expr1 not in seen:
            seen.add(expr1)
            words.append(
                build_card(
                    expression=expr1,
                    answer_str=str(c * c),
                    pron_uz=f"{uz_num(a)} kvadrati qoʻshuv {uz_num(b)} kvadrati",
                    pos_label="Kvadratlar yigʻindisi",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"{a}² + {b}² = {c*c} ({a}²={a*a}, {b}²={b*b})",
                )
            )
        # √(c² - a²) = b
        expr2 = f"√({c}² − {a}²)"
        if expr2 not in seen:
            seen.add(expr2)
            words.append(
                build_card(
                    expression=expr2,
                    answer_str=str(b),
                    pron_uz=f"ildiz ostida {uz_num(c)} kvadrati ayiruv {uz_num(a)} kvadrati",
                    pos_label="Pifagor ildizlari",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"√({c}² − {a}²) = {b} ({c*c} − {a*a} = {b*b})",
                )
            )

    # 7. Square roots up to 1200
    for r in range(101, 1200):
        if len(words) >= target_count:
            break
        x = r * r
        expr = f"√{x}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(r),
                    pron_uz=f"ildiz ostida {uz_num(x)}",
                    pos_label="Katta sonlar ildizi",
                    category_label="Ildizlar va Darajalar",
                    example_uz=f"√{x} = {r} (Ildiz ostida {uz_num(x)} — {uz_num(r)})",
                )
            )

    rng.shuffle(words)
    return {
        "title": "Ildizlar va Darajalar (Aqliy hisob)",
        "category": "Ildizlar va Darajalar (Aqliy hisob)",
        "group": "math",
        "badge": "√x",
        "words": words,
    }


def generate_deck_8_fractions(target_count: int = 1000) -> dict:
    words = []
    seen = set()
    rng = random.Random(20261122)

    # 1. Decimal conversions of fractions: 1/2, 1/4, 3/4, 1/5, 2/5, 3/5, 4/5, 1/8, 3/8, 5/8, 7/8, 1/10, etc.
    denominators = [2, 4, 5, 8, 10, 16, 20, 25, 40, 50]
    for den in denominators:
        for num in range(1, den * 3):
            if math.gcd(num, den) == 1:
                val = num / den
                val_str = f"{val:.4f}".rstrip("0").rstrip(".")
                expr = f"{num}/{den} oʻnlik kasrda"
                if expr not in seen and len(words) < 250:
                    seen.add(expr)
                    words.append(
                        build_card(
                            expression=expr,
                            answer_str=val_str,
                            pron_uz=f"{uz_num(den)}dan {uz_num(num)}",
                            pos_label="Oʻnlik kasrga aylantirish",
                            category_label="Kasrlar (Oddiy va oʻnlik)",
                            example_uz=f"{num}/{den} = {val_str} ({uz_num(den).capitalize()}dan {uz_num(num)} — {val_str})",
                        )
                    )

    # 2. Fractions of numbers: "240 ning 3/4 qismi", "350 ning 2/5 qismi"
    fraction_pairs = [
        (1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
        (1, 6), (5, 6), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
        (1, 8), (3, 8), (5, 8), (7, 8), (1, 9), (2, 9), (4, 9), (5, 9), (7, 9), (8, 9),
        (1, 10), (3, 10), (7, 10), (9, 10), (1, 12), (5, 12), (7, 12), (11, 12),
        (1, 15), (2, 15), (4, 15), (7, 15), (8, 15), (11, 15), (14, 15),
        (1, 20), (3, 20), (7, 20), (9, 20), (11, 20), (13, 20), (17, 20), (19, 20),
    ]

    while len(words) < 650:
        num, den = rng.choice(fraction_pairs)
        base = rng.randint(2, 150) * den
        ans = (base * num) // den
        expr = f"{base} ning {num}/{den} qismi"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=str(ans),
                    pron_uz=f"{uz_num(base)}ning {uz_num(den)}dan {uz_num(num)} qismi",
                    pos_label="Sonning ulushini topish",
                    category_label="Kasrlar (Oddiy va oʻnlik)",
                    example_uz=f"{base} ning {num}/{den} qismi = {ans} ({base} ÷ {den} × {num} = {ans})",
                )
            )

    # 3. Addition of fractions: a/b + c/d
    while len(words) < 850:
        den1 = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        den2 = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        num1 = rng.randint(1, den1 - 1)
        num2 = rng.randint(1, den2 - 1)
        lcm = (den1 * den2) // math.gcd(den1, den2)
        top = num1 * (lcm // den1) + num2 * (lcm // den2)
        g = math.gcd(top, lcm)
        ans_num = top // g
        ans_den = lcm // g
        ans_str = f"{ans_num}/{ans_den}" if ans_den > 1 else str(ans_num)
        expr = f"{num1}/{den1} + {num2}/{den2}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=ans_str,
                    pron_uz=f"{uz_num(den1)}dan {uz_num(num1)} qoʻshuv {uz_num(den2)}dan {uz_num(num2)}",
                    pos_label="Kasrlarni qoʻshish",
                    category_label="Kasrlar (Oddiy va oʻnlik)",
                    example_uz=f"{expr} = {ans_str}",
                )
            )

    # 4. Subtraction of fractions: a/b - c/d
    while len(words) < target_count:
        den1 = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        den2 = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        num1 = rng.randint(1, den1)
        num2 = rng.randint(1, den2 - 1)
        # ensure positive difference
        if (num1 / den1) <= (num2 / den2):
            continue
        lcm = (den1 * den2) // math.gcd(den1, den2)
        top = num1 * (lcm // den1) - num2 * (lcm // den2)
        g = math.gcd(top, lcm)
        ans_num = top // g
        ans_den = lcm // g
        ans_str = f"{ans_num}/{ans_den}" if ans_den > 1 else str(ans_num)
        expr = f"{num1}/{den1} − {num2}/{den2}"
        if expr not in seen:
            seen.add(expr)
            words.append(
                build_card(
                    expression=expr,
                    answer_str=ans_str,
                    pron_uz=f"{uz_num(den1)}dan {uz_num(num1)} ayiruv {uz_num(den2)}dan {uz_num(num2)}",
                    pos_label="Kasrlarni ayirish",
                    category_label="Kasrlar (Oddiy va oʻnlik)",
                    example_uz=f"{expr} = {ans_str}",
                )
            )

    rng.shuffle(words)
    return {
        "title": "Kasrlar (Oddiy va oʻnlik kasrlar)",
        "category": "Kasrlar (Oddiy va oʻnlik)",
        "group": "math",
        "badge": "½",
        "words": words,
    }


def main():
    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    d6 = generate_deck_6_percentages(1000)
    d7 = generate_deck_7_roots_powers(1000)
    d8 = generate_deck_8_fractions(1000)

    for fn, d in [
        ("math-06-percentages.json", d6),
        ("math-07-roots-and-powers.json", d7),
        ("math-08-fractions.json", d8),
    ]:
        out_file = DECKS_DIR / fn
        out_file.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Generated {fn}: {len(d['words'])} cards")


if __name__ == "__main__":
    main()
