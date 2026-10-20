# Inglizcha – Oʻzbekcha Soʻz Kartochkalari (Telegram Mini App)

Ingliz tilidagi **7 000+ dan ortiq noyob soʻz va iboralarni** (kundalik eng faol soʻzlar Top 500 / 1000 / 2000 / 3000 / 5000, barcha hayotiy mavzular, phrasal verbs, irregular verbs, idioms, collocations hamda IELTS/TOEFL akademik soʻzlar) oʻrganishga moʻljallangan minimalist, chiroyli va tez ishlovchi **Telegram Mini App** hamda **aiogram 3** boti.

Ilova istalgancha soʻz hajmi bilan tez ishlashga moslashtirilgan: dastlab faqat yengil manifest (`webapp/data/index.json`) va joriy tanlangan boʻlimning birinchi fayli yuklanadi; `"Hammasi"` rejimida qolgan boʻlimlar fonda (lazy-loading) interfeysni qotirmasdan yuklanadi.

---

## 📁 Loyiha tuzilmasi

```text
words-app/
├── webapp/
│   ├── index.html                 # Yagona ekranli Mini App sahifasi
│   ├── css/
│   │   └── style.css              # 10 xil mavzu gradiyenti, Light/Dark rejim va 3D flip uslublari
│   ├── js/
│   │   └── app.js                 # Koʻp boʻlimli (multi-deck) lazy-loader, qidiruv, 3D flip, CloudStorage/localStorage
│   ├── data/
│   │   ├── index.json             # Avtomatik yaratiladigan manifest (barcha boʻlimlar roʻyxati va soʻzlar soni)
│   │   ├── decks/                 # 54+ ta kichik JSON lugʻat toʻplamlari (<deck-slug>.json, har biri ~150–300 soʻz)
│   │   └── words.json             # Dastlabki 450 ta tayanch soʻz (zaxira / eksport uchun)
│   └── assets/
│       └── fonts/                 # Oʻzbek lotin harflarini (oʻ, gʻ, ʻ, ’, ') toʻliq qoʻllovchi TTF shriftlar
├── bot/
│   └── bot.py                     # Minimal aiogram 3 bot (/start va WebApp Menu Button)
├── tools/
│   ├── build_index.py             # webapp/data/decks/*.json dan webapp/data/index.json manifestini avtomatik yigʻish
│   ├── validate_words.py          # Barcha boʻlimlarni dublikatlar, boʻsh maydonlar va JSON xatolariga tekshirish
│   └── export_words.py            # flashcards/data/words.py dan webapp/data/decks/ ga birlashtirish
├── requirements.txt
├── .env.example
└── README.md
```

---

## ➕ Kodga tegmasdan yangi soʻzlar / yangi boʻlim qoʻshish

Yangi soʻzlar toʻplamini qoʻshish uchun hech qanday JavaScript yoki HTML kodni oʻzgartirish shart emas:

1. `webapp/data/decks/` papkasiga yangi `<deck-slug>.json` fayl tashlang (masalan, `webapp/data/decks/topic-36-aviation.json`):
   ```json
   {
     "title": "Aviatsiya va parvozlar",
     "category": "Aviation & Flights",
     "group": "topic",
     "words": [
       {
         "english": "fuselage",
         "pronunciation_uz": "fyuzelaj",
         "uzbek": "samolyot korpusi (fyuzelyaj)",
         "pos": "noun",
         "example_en": "The aircraft fuselage is made of lightweight aluminum alloys.",
         "example_uz": "Samolyot korpusi yengil alyuminiyotishmalardan tayyorlangan.",
         "category": "Aviatsiya va parvozlar"
       }
     ]
   }
   ```
   - `group`: `"freq"` (`Eng kerakli soʻzlar` guruhiga tushadi) yoki `"topic"` (`Mavzular` guruhiga tushadi).
2. Quyidagi buyruqlarni ishga tushiring:
   ```bash
   python tools/validate_words.py
   python tools/build_index.py
   ```
   `build_index.py` avtomatik ravishda `webapp/data/index.json` manifestini yangilaydi va yangi boʻlim darhol ilovaning boʻlimlar roʻyxatida hamda `"Hammasi"` rejimida paydo boʻladi.

---

## 🚀 1. Lokal ishga tushirish (Run Locally)

### 1.1. Soʻzlar bazasini tekshirish va manifestni yangilash
```bash
python tools/validate_words.py
python tools/build_index.py
```

### 1.2. WebApp ni lokal HTTP serverda ochish
```bash
python -m http.server 8080 --directory webapp
```
Brauzerda ochish:
- Kunduzgi rejim (Light): `http://localhost:8080`
- Tungi rejim (Dark): `http://localhost:8080/?theme=dark`

---

## 🌐 2. HTTPS Tunnel orqali Telegram ichida sinab koʻrish

Telegram Mini App faqat **HTTPS** manzil orqali ochiladi. Lokal serverni (`8080`-port) internetga HTTPS orqali chiqarish uchun quyidagilardan birini ishlating:

### Variant A — Cloudflare Quick Tunnel (tavsiya etiladi, bepul va roʻyxatdan oʻtmasdan):
```bash
cloudflared tunnel --url http://localhost:8080
```
Terminalda chiqqan `https://xxxx-xxxx.trycloudflare.com` manzilini nusxalab oling.

### Variant B — ngrok:
```bash
ngrok http 8080
```
Terminalda chiqqan `https://xxxx.ngrok-free.app` manzilini nusxalab oling.

---

## ☁️ 3. WebApp ni statik sayt sifatida joylash (Deploy Static Site)

`webapp/` papkasi hech qanday backend talab qilmaydigan tayyor statik saytdir. Uni quyidagi platformalardan biriga bepul joylashingiz mumkin:

1. **GitHub Pages:**
   - Loyihani GitHub repozitoriyga yuklang.
   - **Settings → Pages** boʻlimiga oʻting va `webapp` papkasini tanlang.
2. **Netlify:**
   - [app.netlify.com/drop](https://app.netlify.com/drop) sahifasiga `webapp` papkasini tashlang (drag-and-drop) yoki GitHub ulab **Publish directory:** `webapp` deb belgilang.
3. **Render (Static Site):**
   - Render.com da **New → Static Site** tanlang.
   - **Build Command:** `python tools/build_index.py`
   - **Publish Directory:** `webapp` deb kiriting.

---

## 🤖 4. `.env` va `@BotFather` sozlamalari

### 4.1. `.env` faylini yaratish
`.env.example` faylidan nusxa olib `.env` nomli fayl yarating:
```bash
cp .env.example .env
```
Ichiga `@BotFather` dan olingan token va HTTPS WebApp manzilingizni yozing:
```env
BOT_TOKEN=1234567890:AAH_sizning_bot_tokeningiz
WEBAPP_URL=https://sizning-webapp-manzilingiz.netlify.app
```

### 4.2. Botni ishga tushirish
```bash
pip install -r requirements.txt
python bot/bot.py
```
Bot ishga tushganda avtomatik ravishda Menu Button ni ham sozlaydi va `/start` bosilganda **"So'zlarni o'rganish"** WebApp tugmasini yuboradi.
