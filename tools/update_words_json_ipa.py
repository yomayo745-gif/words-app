import json
from pathlib import Path
from add_ipa_to_decks import get_word_ipa

WORDS_JSON = Path(r"C:\Users\user\Desktop\words-app\webapp\data\words.json")
if WORDS_JSON.exists():
    data = json.loads(WORDS_JSON.read_text(encoding="utf-8"))
    for w in data:
        w["ipa"] = get_word_ipa(w["english"])
    WORDS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {len(data)} words in {WORDS_JSON}")
