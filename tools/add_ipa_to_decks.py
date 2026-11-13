"""
Enrich all deck files in webapp/data/decks/*.json with accurate IPA phonetic transcription (/.../).
Uses CMU pronunciation database with high-accuracy tokenization, stress markings, and irregular verb handling.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path
import eng_to_ipa as ipa

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"
DB_PATH = Path(sys.prefix) / "Lib" / "site-packages" / "eng_to_ipa" / "resources" / "CMU_dict.db"

if not DB_PATH.exists():
    # Try user site packages or import location
    DB_PATH = Path(ipa.__file__).resolve().parent / "resources" / "CMU_dict.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT word, phonemes FROM dictionary")
cmu_cache: dict[str, list[str]] = {}
for w, p in cur.fetchall():
    cmu_cache.setdefault(w, []).append(p)
conn.close()

SPECIAL_WORDS: dict[str, str] = {
    "be": "biː",
    "been": "biːn",
    "was": "wɒz",
    "were": "wɜːr",
    "have": "hæv",
    "has": "hæz",
    "had": "hæd",
    "do": "duː",
    "does": "dʌz",
    "did": "dɪd",
    "the": "ðə",
    "a": "ə",
    "an": "æn",
    "to": "tuː",
    "of": "əv",
    "and": "ænd",
    "in": "ɪn",
    "is": "ɪz",
    "it": "ɪt",
    "you": "juː",
    "that": "ðæt",
    "he": "hiː",
    "she": "ʃiː",
    "we": "wiː",
    "they": "ðeɪ",
    "for": "fɔːr",
    "on": "ɒn",
    "with": "wɪð",
    "as": "æz",
    "at": "æt",
    "by": "baɪ",
    "from": "frɒm",
    "or": "ɔːr",
    "but": "bʌt",
    "not": "nɒt",
    "timezone": "ˈtaɪmzoʊn",
    "searchable": "ˈsɜːrtʃəbəl",
    "precedented": "ˈprɛsɪdəntɪd",
    "2nd": "ˈsɛkənd",
    "1st": "fɜːrst",
    "3rd": "θɜːrd",
    "etc": "ɪtˈsɛtərə",
    "e.g.": "fɔːr ɪɡˈzæmpəl",
    "i.e.": "ðæt ɪz",
    "awoken": "əˈwoʊkən",
    "gotten": "ˈɡɒtn",
    "spelt": "spɛlt",
    "span": "spæn",
    "spun": "spʌn",
    "spoilt": "spɔɪlt",
    "dustpan": "ˈdʌstpæn",
    "secondhand": "ˈsɛkəndˌhænd",
    "cannot": "ˈkænɒt",
    "wifi": "ˈwaɪfaɪ",
    "smartphone": "ˈsmɑːrtfoʊn",
    "website": "ˈwɛbˌsaɪt",
    "online": "ˈɒnˌlaɪn",
}

def single_token_ipa(tok: str) -> str:
    clean = tok.lower().strip(".,!?:;\"'()[]")
    if not clean:
        return tok
    if clean in SPECIAL_WORDS:
        return SPECIAL_WORDS[clean]
    
    cmu = cmu_cache.get(clean)
    if cmu:
        try:
            res = ipa.cmu_to_ipa([[cmu[0]]], mark=False)[0][0]
            res = res.replace("ʧ", "tʃ").replace("ʤ", "dʒ")
            return res
        except Exception:
            pass
    
    conv = ipa.convert(clean)
    if conv and "*" not in conv:
        return conv.replace("ʧ", "tʃ").replace("ʤ", "dʒ")
    
    return clean.replace("*", "")

def get_word_ipa(english: str) -> str:
    raw = english.strip()
    if raw.lower() in SPECIAL_WORDS:
        return f"/{SPECIAL_WORDS[raw.lower()]}/"
    
    parts = re.findall(r"[A-Za-z0-9']+|[^A-Za-z0-9'\s]+|\s+", raw)
    out_parts = []
    for p in parts:
        if re.match(r"^[A-Za-z0-9']+$", p):
            out_parts.append(single_token_ipa(p))
        else:
            out_parts.append(p)
    
    ipa_str = "".join(out_parts)
    ipa_str = re.sub(r"\s+", " ", ipa_str).strip()
    return f"/{ipa_str}/"

def process_all_decks():
    deck_files = sorted(DECKS_DIR.glob("*.json"))
    total_words = 0
    total_files = len(deck_files)

    for deck_file in deck_files:
        raw_text = deck_file.read_text(encoding="utf-8")
        payload = json.loads(raw_text)
        is_dict_root = isinstance(payload, dict)
        words = payload.get("words", []) if is_dict_root else payload

        for w in words:
            total_words += 1
            w["ipa"] = get_word_ipa(w["english"])

        if is_dict_root:
            deck_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            deck_file.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Successfully added IPA to {total_words} words across {total_files} deck files in {DECKS_DIR}")

if __name__ == "__main__":
    process_all_decks()
