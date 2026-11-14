import urllib.request
import urllib.parse

def clean_audio_text(text):
    t = text.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ").replace("-", " minus ").replace("=", " equals ").replace("?", "")
    return " ".join(t.split())

cases = ["2 × 7 = ?", "2 × 35 = ?", "72 ÷ 8 = ?", "25 + 38 = ?", "100 − 37 = ?"]
for c in cases:
    cl = clean_audio_text(c)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={urllib.parse.quote(cl)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    res = urllib.request.urlopen(req)
    print(f"{c} -> \"{cl}\": {res.status}, {len(res.read())} bytes")
