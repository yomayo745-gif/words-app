"""
Generate clean, fully-compliant expansion decks for:
1. 12 New Book Units (4000 Essential English Words, Units 3-5 across Books 1-4 = 240 words)
2. topic-36-situational-dialogues.json (100 high-value conversational phrases)
"""

from __future__ import annotations
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"

BOOK_DATA = {
    # ----------------- BOOK 1 -----------------
    "book-01-unit-03": {
        "title": "1-kitob: 1.3-bob",
        "category": "1-kitob: 1.3-bob",
        "badge": "1.3",
        "words": [
            {"english": "afraid", "ipa": "/əˈfreɪd/", "pronunciation_uz": "efreyd", "uzbek": "qoʻrqqan, choʻchigan", "pos": "adj", "example_en": "The little dog was afraid of thunder.", "example_uz": "Kichkina kuchuk momaqaldiroqdan qoʻrqdi."},
            {"english": "agree", "ipa": "/əˈɡriː/", "pronunciation_uz": "egriy", "uzbek": "rozi boʻlmoq, qoʻshilmoq", "pos": "verb", "example_en": "I agree with your suggestion completely.", "example_uz": "Men sizning taklifingizga toʻliq qoʻshilaman."},
            {"english": "arrive", "ipa": "/əˈraɪv/", "pronunciation_uz": "erayv", "uzbek": "yetib kelmoq", "pos": "verb", "example_en": "The train will arrive at five o'clock.", "example_uz": "Poyezd soat beshda yetib keladi."},
            {"english": "attack", "ipa": "/əˈtæk/", "pronunciation_uz": "etek", "uzbek": "hujum qilmoq", "pos": "verb", "example_en": "The wild animal attacked without warning.", "example_uz": "Yovvoyi hayvon ogohlantirishsiz hujum qildi."},
            {"english": "bottom", "ipa": "/ˈbɒt.əm/", "pronunciation_uz": "botem", "uzbek": "tub, eng pastki qism", "pos": "noun", "example_en": "Coins lay at the bottom of the fountain.", "example_uz": "Favvoraning tubida tangalar yotardi."},
            {"english": "clever", "ipa": "/ˈklev.ər/", "pronunciation_uz": "klever", "uzbek": "aqlli, zukko", "pos": "adj", "example_en": "She had a clever plan to solve the puzzle.", "example_uz": "Topishmoqni yechish uchun uning zukko rejasi bor edi."},
            {"english": "cruel", "ipa": "/ˈkruː.əl/", "pronunciation_uz": "kruel", "uzbek": "shafqatsiz, zolim", "pos": "adj", "example_en": "It is cruel to leave pets out in the freezing cold.", "example_uz": "Uy hayvonlarini qahraton sovuqda qoldirish shafqatsizlikdir."},
            {"english": "finally", "ipa": "/ˈfaɪ.nəl.i/", "pronunciation_uz": "fayneli", "uzbek": "nihoyat, oxir-oqibat", "pos": "adv", "example_en": "They finally finished the long journey.", "example_uz": "Ular nihoyat uzoq safarni yakunladilar."},
            {"english": "hide", "ipa": "/haɪd/", "pronunciation_uz": "hayd", "uzbek": "yashirmoq, yashirinmoq", "pos": "verb", "example_en": "The children like to hide behind the large tree.", "example_uz": "Bolalar katta daraxt orqasiga yashirinishni yoqtirishadi."},
            {"english": "hunt", "ipa": "/hʌnt/", "pronunciation_uz": "hant", "uzbek": "ov qilmoq", "pos": "verb", "example_en": "Lions hunt in groups to catch food.", "example_uz": "Sherlar ozuqa tutish uchun toʻda boʻlib ov qilishadi."},
            {"english": "lot", "ipa": "/lɒt/", "pronunciation_uz": "lot", "uzbek": "koʻp, koʻp miqdor", "pos": "noun", "example_en": "There is a lot of apples on the table.", "example_uz": "Stol ustida juda koʻp olma bor."},
            {"english": "middle", "ipa": "/ˈmɪd.əl/", "pronunciation_uz": "midl", "uzbek": "oʻrta, oʻrtasi", "pos": "noun", "example_en": "Stand in the middle of the room.", "example_uz": "Xonaning oʻrtasida turing."},
            {"english": "moment", "ipa": "/ˈməʊ.mənt/", "pronunciation_uz": "moument", "uzbek": "lahza, fursat", "pos": "noun", "example_en": "Please wait a moment while I check the file.", "example_uz": "Faylni tekshirgunimcha bir lahza kuting."},
            {"english": "pleased", "ipa": "/pliːzd/", "pronunciation_uz": "pliyzd", "uzbek": "mamnun, xursand", "pos": "adj", "example_en": "The teacher was pleased with our good results.", "example_uz": "Oʻqituvchi bizning yaxshi natijalarimizdan mamnun boʻldi."},
            {"english": "promise", "ipa": "/ˈprɒm.ɪs/", "pronunciation_uz": "promis", "uzbek": "vaʼda bermoq", "pos": "verb", "example_en": "I promise to return your book tomorrow.", "example_uz": "Kitobingizni ertaga qaytarishga vaʼda beraman."},
            {"english": "reply", "ipa": "/rɪˈplaɪ/", "pronunciation_uz": "riplay", "uzbek": "javob bermoq", "pos": "verb", "example_en": "He did not reply to my text message.", "example_uz": "U mening xabarimga javob bermadi."},
            {"english": "safe", "ipa": "/seɪf/", "pronunciation_uz": "seyf", "uzbek": "xavfsiz, omon", "pos": "adj", "example_en": "Fasten your seatbelt to stay safe.", "example_uz": "Xavfsiz boʻlish uchun xavfsizlik kamarini taqing."},
            {"english": "trick", "ipa": "/trɪk/", "pronunciation_uz": "trik", "uzbek": "hiyla, nayrang", "pos": "noun", "example_en": "The magician performed an amazing coin trick.", "example_uz": "Koʻzboylogʻich tanga bilan ajoyib nayrang koʻrsatdi."},
            {"english": "well", "ipa": "/wel/", "pronunciation_uz": "vel", "uzbek": "yaxshi, durust", "pos": "adv", "example_en": "She speaks English very well.", "example_uz": "U ingliz tilida juda yaxshi gapiradi."},
            {"english": "adventure", "ipa": "/ədˈven.tʃər/", "pronunciation_uz": "edvencher", "uzbek": "sarguzasht", "pos": "noun", "example_en": "Traveling to distant islands is a great adventure.", "example_uz": "Olis orollarga sayohat qilish ajoyib sarguzashtdir."}
        ]
    },
    "book-01-unit-04": {
        "title": "1-kitob: 1.4-bob",
        "category": "1-kitob: 1.4-bob",
        "badge": "1.4",
        "words": [
            {"english": "approach", "ipa": "/əˈprəʊtʃ/", "pronunciation_uz": "eprouch", "uzbek": "yaqinlashmoq", "pos": "verb", "example_en": "The storm began to approach the coast.", "example_uz": "Boʻron qirgʻoqqa yaqinlasha boshladi."},
            {"english": "carefully", "ipa": "/ˈkeə.fəl.i/", "pronunciation_uz": "kefeli", "uzbek": "ehtiyotkorlik bilan", "pos": "adv", "example_en": "Read the instructions carefully before starting.", "example_uz": "Boshlashdan oldin koʻrsatmalarni ehtiyotkorlik bilan oʻqing."},
            {"english": "chemical", "ipa": "/ˈkem.ɪ.kəl/", "pronunciation_uz": "kemikl", "uzbek": "kimyoviy modda", "pos": "noun", "example_en": "Do not mix this dangerous chemical with water.", "example_uz": "Ushbu xavfli kimyoviy moddani suv bilan aralashtirmang."},
            {"english": "create", "ipa": "/kriˈeɪt/", "pronunciation_uz": "krieyt", "uzbek": "yaratmoq, barpo etmoq", "pos": "verb", "example_en": "Artists create beautiful paintings.", "example_uz": "Rassomlar goʻzal rasmlar yaratishadi."},
            {"english": "evil", "ipa": "/ˈiː.vəl/", "pronunciation_uz": "iyvl", "uzbek": "yovuz, yomon", "pos": "adj", "example_en": "The evil king ruled the land with fear.", "example_uz": "Yovuz podshoh yurtni qoʻrquv bilan boshqardi."},
            {"english": "experiment", "ipa": "/ɪkˈsper.ɪ.mənt/", "pronunciation_uz": "eksperiment", "uzbek": "tajriba, sinov", "pos": "noun", "example_en": "The science experiment was successful.", "example_uz": "Ilmiy tajriba muvaffaqiyatli boʻldi."},
            {"english": "kill", "ipa": "/kɪl/", "pronunciation_uz": "kil", "uzbek": "oʻldirmoq", "pos": "verb", "example_en": "Extreme cold can kill sensitive plants.", "example_uz": "Qattiq sovuq nozik oʻsimliklarni nobud qilishi mumkin."},
            {"english": "laboratory", "ipa": "/ləˈbɒr.ə.tər.i/", "pronunciation_uz": "leboretri", "uzbek": "laboratoriya", "pos": "noun", "example_en": "Scientists work inside a sterile laboratory.", "example_uz": "Olimlar toza laboratoriya ichida ishlashadi."},
            {"english": "among", "ipa": "/əˈmʌŋ/", "pronunciation_uz": "emang", "uzbek": "orasida, oʻrtasida", "pos": "prep", "example_en": "She sat among her closest friends.", "example_uz": "U eng yaqin doʻstlari orasida oʻtirdi."},
            {"english": "chart", "ipa": "/tʃɑːt/", "pronunciation_uz": "chart", "uzbek": "jadval, diagramma", "pos": "noun", "example_en": "The teacher drew a progress chart on the board.", "example_uz": "Oʻqituvchi doskaga oʻsish jadvalini chizdi."},
            {"english": "nervous", "ipa": "/ˈnɜː.vəs/", "pronunciation_uz": "nerves", "uzbek": "hayajonlangan, asabiy", "pos": "adj", "example_en": "He was nervous before the big exam.", "example_uz": "U katta imtihon oldidan hayajonlangan edi."},
            {"english": "noise", "ipa": "/nɔɪz/", "pronunciation_uz": "noyz", "uzbek": "shovqin, sas", "pos": "noun", "example_en": "The engine made a strange clicking noise.", "example_uz": "Dvigatel gʻalati taqillagan ovoz chiqardi."},
            {"english": "project", "ipa": "/ˈprɒdʒ.ekt/", "pronunciation_uz": "proyekt", "uzbek": "loyiha", "pos": "noun", "example_en": "Our team finished the school project on time.", "example_uz": "Jamoamiz maktab loyihasini oʻz vaqtida tugatdi."},
            {"english": "scare", "ipa": "/skeər/", "pronunciation_uz": "skeer", "uzbek": "qoʻrqitmoq", "pos": "verb", "example_en": "The loud thunder scared the young children.", "example_uz": "Baland momaqaldiroq yosh bolalarni qoʻrqitdi."},
            {"english": "secret", "ipa": "/ˈsiː.krət/", "pronunciation_uz": "siykret", "uzbek": "sir, sirli narsa", "pos": "noun", "example_en": "Can you keep an important secret?", "example_uz": "Muhim sirni saqlay olasizmi?"},
            {"english": "shout", "ipa": "/ʃaʊt/", "pronunciation_uz": "shaut", "uzbek": "baqirmoq, qichqirmoq", "pos": "verb", "example_en": "Do not shout in the library.", "example_uz": "Kutubxonada baqirmang."},
            {"english": "smell", "ipa": "/smel/", "pronunciation_uz": "smel", "uzbek": "hidlamoq, hid chiqarmoq", "pos": "verb", "example_en": "These fresh flowers smell wonderful.", "example_uz": "Bu yangi gullar ajoyib hid taratmoqda."},
            {"english": "terrible", "ipa": "/ˈter.ə.bəl/", "pronunciation_uz": "terribl", "uzbek": "dahshatli, juda yomon", "pos": "adj", "example_en": "The traffic was terrible this morning.", "example_uz": "Bugun ertalab tirbandlik juda dahshatli edi."},
            {"english": "worse", "ipa": "/wɜːs/", "pronunciation_uz": "vors", "uzbek": "yomonroq", "pos": "adj", "example_en": "The weather today is worse than yesterday.", "example_uz": "Bugungi ob-havo kechagidan yomonroq."},
            {"english": "alien", "ipa": "/ˈeɪ.li.ən/", "pronunciation_uz": "eyliyen", "uzbek": "oʻzga sayyoralik, begona", "pos": "noun", "example_en": "The movie was about an alien visiting Earth.", "example_uz": "Film Yerga tashrif buyurgan oʻzga sayyoralik haqida edi."}
        ]
    },
    "book-01-unit-05": {
        "title": "1-kitob: 1.5-bob",
        "category": "1-kitob: 1.5-bob",
        "badge": "1.5",
        "words": [
            {"english": "cloud", "ipa": "/klaʊd/", "pronunciation_uz": "klaud", "uzbek": "bulut", "pos": "noun", "example_en": "A dark cloud covered the sun.", "example_uz": "Qora bulut quyoshni toʻsib qoʻydi."},
            {"english": "comprehend", "ipa": "/ˌkɒm.prɪˈhend/", "pronunciation_uz": "komprihend", "uzbek": "tushunmoq, idrok etmoq", "pos": "verb", "example_en": "He could not comprehend the complex problem.", "example_uz": "U murakkab masalani tushuna olmadi."},
            {"english": "describe", "ipa": "/dɪˈskraɪb/", "pronunciation_uz": "deskrayb", "uzbek": "tasvirlamoq", "pos": "verb", "example_en": "Can you describe the person you saw?", "example_uz": "Siz koʻrgan odamni tasvirlab bera olasizmi?"},
            {"english": "ever", "ipa": "/ˈev.ər/", "pronunciation_uz": "ever", "uzbek": "qachondir, sira", "pos": "adv", "example_en": "Have you ever traveled to another country?", "example_uz": "Siz qachondir boshqa mamlakatga borganmisiz?"},
            {"english": "fail", "ipa": "/feɪl/", "pronunciation_uz": "feyl", "uzbek": "yiqilmoq, muvaffaqiyatsiz boʻlmoq", "pos": "verb", "example_en": "If you study hard, you will not fail the test.", "example_uz": "Agar qattiq oʻqisangiz, imtihondan yiqilmaysiz."},
            {"english": "friendly", "ipa": "/ˈfrend.li/", "pronunciation_uz": "frendli", "uzbek": "doʻstona, ochiqkoʻngil", "pos": "adj", "example_en": "Our new neighbors are very friendly.", "example_uz": "Yangi qoʻshnilarimiz juda doʻstona."},
            {"english": "grade", "ipa": "/ɡreɪd/", "pronunciation_uz": "greyd", "uzbek": "baho, daraja", "pos": "noun", "example_en": "She got an excellent grade on her essay.", "example_uz": "U inshosidan aʼlo baho oldi."},
            {"english": "instead", "ipa": "/ɪnˈsted/", "pronunciation_uz": "insted", "uzbek": "oʻrniga", "pos": "adv", "example_en": "Drink fresh water instead of soda.", "example_uz": "Gazli ichimlik oʻrniga toza suv iching."},
            {"english": "library", "ipa": "/ˈlaɪ.brər.i/", "pronunciation_uz": "laybreri", "uzbek": "kutubxona", "pos": "noun", "example_en": "Students borrow books from the university library.", "example_uz": "Talabalar universitet kutubxonasidan kitob olishadi."},
            {"english": "planet", "ipa": "/ˈplæn.ɪt/", "pronunciation_uz": "planet", "uzbek": "sayyora", "pos": "noun", "example_en": "Earth is the third planet from the sun.", "example_uz": "Yer quyoshdan uchinchi sayyoradir."},
            {"english": "report", "ipa": "/rɪˈpɔːt/", "pronunciation_uz": "riport", "uzbek": "hisobot, hisobot bermoq", "pos": "noun", "example_en": "He submitted the financial report on Monday.", "example_uz": "U moliyaviy hisobotni dushanba kuni topshirdi."},
            {"english": "several", "ipa": "/ˈsev.ər.əl/", "pronunciation_uz": "sevral", "uzbek": "bir necha, bir nechta", "pos": "adj", "example_en": "I have visited that museum several times.", "example_uz": "Men u muzeyga bir necha bor borganman."},
            {"english": "solve", "ipa": "/sɒlv/", "pronunciation_uz": "solv", "uzbek": "yechmoq, hal qilmoq", "pos": "verb", "example_en": "They worked together to solve the math puzzle.", "example_uz": "Ular matematik jumboqni yechish uchun birgalikda ishladilar."},
            {"english": "suddenly", "ipa": "/ˈsʌd.ən.li/", "pronunciation_uz": "sadenli", "uzbek": "toʻsatdan, birdaniga", "pos": "adv", "example_en": "Suddenly the lights went out.", "example_uz": "Toʻsatdan chiroqlar oʻchib qoldi."},
            {"english": "suppose", "ipa": "/səˈpəʊz/", "pronunciation_uz": "sepouz", "uzbek": "faraz qilmoq, deb oʻylamoq", "pos": "verb", "example_en": "I suppose we should leave early to avoid traffic.", "example_uz": "Menimcha, tirbandlikka tushmaslik uchun erta ketishimiz kerak."},
            {"english": "universe", "ipa": "/ˈjuː.nɪ.vɜːs/", "pronunciation_uz": "yunivers", "uzbek": "koinot, olam", "pos": "noun", "example_en": "Telescopes allow us to explore the vast universe.", "example_uz": "Teleskoplar bizga ulkan koinotni tadqiq qilish imkonini beradi."},
            {"english": "view", "ipa": "/vjuː/", "pronunciation_uz": "vyu", "uzbek": "manzara, koʻrinish", "pos": "noun", "example_en": "The hotel room has a magnificent view of the mountains.", "example_uz": "Mehmonxona xonasidan togʻlarning ajoyib manzarasi koʻrinadi."},
            {"english": "appropriate", "ipa": "/əˈprəʊ.pri.ət/", "pronunciation_uz": "eproupriyet", "uzbek": "mos, munosib", "pos": "adj", "example_en": "Wear appropriate clothes for the job interview.", "example_uz": "Ish suhbati uchun munosib kiyim kiying."},
            {"english": "avoid", "ipa": "/əˈvɔɪd/", "pronunciation_uz": "evoyd", "uzbek": "chetlanmoq, qochmoq", "pos": "verb", "example_en": "Drivers should avoid dangerous potholes.", "example_uz": "Haydovchilar xavfli chuqurlardan qochishlari kerak."},
            {"english": "behave", "ipa": "/bɪˈheɪv/", "pronunciation_uz": "biheyv", "uzbek": "oʻzini odobli tutmoq", "pos": "verb", "example_en": "Children behave politely during dinner.", "example_uz": "Bolalar kechki ovqat paytida oʻzlarini odobli tutishadi."}
        ]
    },

    # ----------------- BOOK 2 -----------------
    "book-02-unit-03": {
        "title": "2-kitob: 2.3-bob",
        "category": "2-kitob: 2.3-bob",
        "badge": "2.3",
        "words": [
            {"english": "accept", "ipa": "/əkˈsept/", "pronunciation_uz": "eksept", "uzbek": "qabul qilmoq", "pos": "verb", "example_en": "She was pleased to accept the invitation.", "example_uz": "U taklifni mamnuniyat bilan qabul qildi."},
            {"english": "arrange", "ipa": "/əˈreɪndʒ/", "pronunciation_uz": "ereyndj", "uzbek": "tartibga solmoq, kelishmoq", "pos": "verb", "example_en": "They arranged the books on the shelves.", "example_uz": "Ular kitoblarni javonlarga tartib bilan terishdi."},
            {"english": "attend", "ipa": "/əˈtend/", "pronunciation_uz": "etend", "uzbek": "qatnashmoq, bormoq", "pos": "verb", "example_en": "Many guests attended the wedding.", "example_uz": "Koʻplab mehmonlar toʻyda qatnashdilar."},
            {"english": "balance", "ipa": "/ˈbæl.əns/", "pronunciation_uz": "balans", "uzbek": "muvozanat", "pos": "noun", "example_en": "Tightrope walkers must have perfect balance.", "example_uz": "Dorbozlar mukammal muvozanatga ega boʻlishi kerak."},
            {"english": "contrast", "ipa": "/ˈkɒn.trɑːst/", "pronunciation_uz": "kontrast", "uzbek": "taqqos, farq", "pos": "noun", "example_en": "There is a sharp contrast between day and night temperatures.", "example_uz": "Kunduzgi va tungi haroratlar oʻrtasida keskin farq bor."},
            {"english": "encourage", "ipa": "/ɪnˈkʌr.ɪdʒ/", "pronunciation_uz": "inkaridj", "uzbek": "ruhlandirmoq, dalda bermoq", "pos": "verb", "example_en": "Teachers encourage students to read widely.", "example_uz": "Oʻqituvchilar talabalarni koʻp oʻqishga ruhlantiradilar."},
            {"english": "familiar", "ipa": "/fəˈmɪl.i.ər/", "pronunciation_uz": "femiliyer", "uzbek": "tanish, maʼlum", "pos": "adj", "example_en": "His voice sounded familiar to me.", "example_uz": "Uning ovozi menga tanish eshitildi."},
            {"english": "grab", "ipa": "/ɡræb/", "pronunciation_uz": "greb", "uzbek": "ushlab olmoq, changallamoq", "pos": "verb", "example_en": "Grab your coat before running outside.", "example_uz": "Tashqariga chiqishdan oldin paltoingizni oling."},
            {"english": "hang", "ipa": "/hæŋ/", "pronunciation_uz": "heng", "uzbek": "osmoq, ilmoq", "pos": "verb", "example_en": "Hang your jacket on the coat rack.", "example_uz": "Nimchangizni kiyim ilgichga osing."},
            {"english": "huge", "ipa": "/hjuːdʒ/", "pronunciation_uz": "hyudj", "uzbek": "ulkan, bahaybat", "pos": "adj", "example_en": "An elephant is a huge mammal.", "example_uz": "Fil ulkan sutemizuvchidir."},
            {"english": "necessary", "ipa": "/ˈnes.ə.ser.i/", "pronunciation_uz": "neseseri", "uzbek": "zarur, kerakli", "pos": "adj", "example_en": "Water is necessary for all living things.", "example_uz": "Suv barcha tirik mavjudotlar uchun zarurdir."},
            {"english": "pattern", "ipa": "/ˈpæt.ən/", "pronunciation_uz": "petten", "uzbek": "andoza, naqsh, tartib", "pos": "noun", "example_en": "The fabric has a colorful geometric pattern.", "example_uz": "Matoda rang-barang geometrik naqsh bor."},
            {"english": "propose", "ipa": "/prəˈpəʊz/", "pronunciation_uz": "prepouz", "uzbek": "taklif qilmoq", "pos": "verb", "example_en": "He proposed a new schedule for our team.", "example_uz": "U jamoamiz uchun yangi jadval taklif qildi."},
            {"english": "purpose", "ipa": "/ˈpɜː.pəs/", "pronunciation_uz": "porpes", "uzbek": "maqsad, niyat", "pos": "noun", "example_en": "The purpose of this meeting is to plan our budget.", "example_uz": "Ushbu uchrashuvning maqsadi byudjetimizni rejalashtirishdir."},
            {"english": "release", "ipa": "/rɪˈliːs/", "pronunciation_uz": "riliys", "uzbek": "qoʻyib yubormoq, chiqarmoq", "pos": "verb", "example_en": "They decided to release the bird from the cage.", "example_uz": "Ular qushni qafasdan qoʻyib yuborishga qaror qildilar."},
            {"english": "require", "ipa": "/rɪˈkwaɪər/", "pronunciation_uz": "rikvayer", "uzbek": "talab qilmoq", "pos": "verb", "example_en": "The university requires proof of graduation.", "example_uz": "Universitet bitirganlik toʻgʻrisida guvohnoma talab qiladi."},
            {"english": "single", "ipa": "/ˈsɪŋ.ɡəl/", "pronunciation_uz": "singl", "uzbek": "yagona, bir dona", "pos": "adj", "example_en": "Not a single word was spoken in the quiet room.", "example_uz": "Tinch xonada birorta ham soʻz aytilmadi."},
            {"english": "success", "ipa": "/səkˈses/", "pronunciation_uz": "sekses", "uzbek": "muvaffaqiyat, yutuq", "pos": "noun", "example_en": "Hard work is the key to lasting success.", "example_uz": "Mehnatsevarlik barqaror muvaffaqiyatning kalitidir."},
            {"english": "tear", "ipa": "/teər/", "pronunciation_uz": "teer", "uzbek": "yirtmoq", "pos": "verb", "example_en": "Be careful not to tear the delicate paper.", "example_uz": "Nozik qogʻozni yirtib yubormaslik uchun ehtiyot boʻling."},
            {"english": "theory", "ipa": "/ˈθɪə.ri/", "pronunciation_uz": "fiyeri", "uzbek": "nazariya", "pos": "noun", "example_en": "Scientists tested Einstein's theory of relativity.", "example_uz": "Olimlar Eynshteynning nisbiylik nazariyasini sinab koʻrishdi."}
        ]
    },
    "book-02-unit-04": {
        "title": "2-kitob: 2.4-bob",
        "category": "2-kitob: 2.4-bob",
        "badge": "2.4",
        "words": [
            {"english": "against", "ipa": "/əˈɡenst/", "pronunciation_uz": "egenst", "uzbek": "qarshi", "pos": "prep", "example_en": "They played a tough match against the champions.", "example_uz": "Ular chempionlarga qarshi qiyin oʻyin oʻtkazdilar."},
            {"english": "beach", "ipa": "/biːtʃ/", "pronunciation_uz": "biych", "uzbek": "plyaj, sohil", "pos": "noun", "example_en": "We spent all afternoon walking along the sandy beach.", "example_uz": "Biz butun tushdan keyinni qumli sohil boʻylab sayr qilib oʻtkazdik."},
            {"english": "damage", "ipa": "/ˈdæm.ɪdʒ/", "pronunciation_uz": "demidj", "uzbek": "zarar yetkazmoq, ziyon", "pos": "verb", "example_en": "The hail caused heavy damage to the crops.", "example_uz": "Doʻl ekinlarga katta zarar yetkazdi."},
            {"english": "discover", "ipa": "/dɪˈskʌv.ər/", "pronunciation_uz": "diskover", "uzbek": "kashf qilmoq, topmoq", "pos": "verb", "example_en": "Explorers discovered an ancient cave in the forest.", "example_uz": "Sayyohlar oʻrmonda qadimiy gʻorni kashf qilishdi."},
            {"english": "emotion", "ipa": "/ɪˈməʊ.ʃən/", "pronunciation_uz": "emoushen", "uzbek": "his-tuygʻu, emotsiya", "pos": "noun", "example_en": "Music can evoke strong emotion.", "example_uz": "Musiqa kuchli his-tuygʻularni uygʻotishi mumkin."},
            {"english": "fix", "ipa": "/fɪks/", "pronunciation_uz": "fiks", "uzbek": "tuzatmoq, taʼmirlamoq", "pos": "verb", "example_en": "The mechanic will fix the broken car engine.", "example_uz": "Usta buzilgan avtomobil dvigatelini tuzatadi."},
            {"english": "frank", "ipa": "/fræŋk/", "pronunciation_uz": "frenk", "uzbek": "samimiy, ochiqkoʻngil", "pos": "adj", "example_en": "He gave a frank opinion during the discussion.", "example_uz": "U muhokama davomida samimiy fikr bildirdi."},
            {"english": "identify", "ipa": "/aɪˈden.tɪ.faɪ/", "pronunciation_uz": "aydentifay", "uzbek": "aniqlamoq, tanib olmoq", "pos": "verb", "example_en": "Can you identify the species of this bird?", "example_uz": "Siz bu qushning turini aniqlay olasizmi?"},
            {"english": "island", "ipa": "/ˈaɪ.lənd/", "pronunciation_uz": "aylend", "uzbek": "orol", "pos": "noun", "example_en": "They sailed to a peaceful tropical island.", "example_uz": "Ular tinch tropik orolga suzib borishdi."},
            {"english": "ocean", "ipa": "/ˈəʊ.ʃən/", "pronunciation_uz": "oushen", "uzbek": "okean", "pos": "noun", "example_en": "Whales travel across the open ocean.", "example_uz": "Kitlar ochiq okean boʻylab suzishadi."},
            {"english": "perhaps", "ipa": "/pəˈhæps/", "pronunciation_uz": "perheps", "uzbek": "balki, ehtimol", "pos": "adv", "example_en": "Perhaps we will arrive before it begins to rain.", "example_uz": "Balki yomgʻir yogʻishidan oldin yetib borarmiz."},
            {"english": "pleasant", "ipa": "/ˈplez.ənt/", "pronunciation_uz": "plezent", "uzbek": "yoqimli, yoqimtoy", "pos": "adj", "example_en": "We had a pleasant dinner with our guests.", "example_uz": "Biz mehmonlarimiz bilan yoqimli kechki ovqat tanovul qildik."},
            {"english": "prevent", "ipa": "/prɪˈvent/", "pronunciation_uz": "privent", "uzbek": "oldini olmoq", "pos": "verb", "example_en": "Regular exercise can prevent many illnesses.", "example_uz": "Muntazam jismoniy mashqlar koʻplab kasalliklarning oldini oladi."},
            {"english": "rock", "ipa": "/rɒk/", "pronunciation_uz": "rok", "uzbek": "qoya, tosh", "pos": "noun", "example_en": "Waves crashed against the sharp rock.", "example_uz": "Toʻlqinlar oʻtkir qoyaga urildi."},
            {"english": "save", "ipa": "/seɪv/", "pronunciation_uz": "seyv", "uzbek": "qutqarmoq, tejamoq", "pos": "verb", "example_en": "The lifeguard jumped in to save the swimmer.", "example_uz": "Qutqaruvchi suzuvchini qutqarish uchun suvga sakradi."},
            {"english": "step", "ipa": "/step/", "pronunciation_uz": "step", "uzbek": "qadam tashlamoq, qadam", "pos": "verb", "example_en": "Watch your step when descending the stairs.", "example_uz": "Zinadan tushayotganda qadamingizga ehtiyot boʻling."},
            {"english": "still", "ipa": "/stɪl/", "pronunciation_uz": "stil", "uzbek": "hali ham, hanuz", "pos": "adv", "example_en": "Even at midnight he was still reading his book.", "example_uz": "Hatto yarim tunda ham u hali kitob oʻqiyotgan edi."},
            {"english": "taste", "ipa": "/teɪst/", "pronunciation_uz": "teyst", "uzbek": "taʼtmoq, taʼm", "pos": "verb", "example_en": "Taste this soup to see if it needs more salt.", "example_uz": "Shoʻrvaga tuz yetarlimi yoki yoʻqligini bilish uchun undan tatib koʻring."},
            {"english": "throw", "ipa": "/θrəʊ/", "pronunciation_uz": "frou", "uzbek": "uloqtirmoq, tashlamoq", "pos": "verb", "example_en": "Throw the ball to your teammate.", "example_uz": "Toʻpni jamoadoshingizga uloqtiring."},
            {"english": "wave", "ipa": "/weɪv/", "pronunciation_uz": "veyv", "uzbek": "toʻlqin, qoʻl silkitmoq", "pos": "noun", "example_en": "Surfers rode the massive ocean wave.", "example_uz": "Syorfingchilar ulkan okean toʻlqinida uchishdi."}
        ]
    },
    "book-02-unit-05": {
        "title": "2-kitob: 2.5-bob",
        "category": "2-kitob: 2.5-bob",
        "badge": "2.5",
        "words": [
            {"english": "benefit", "ipa": "/ˈben.ɪ.fɪt/", "pronunciation_uz": "benefit", "uzbek": "foyda, naf", "pos": "noun", "example_en": "Regular walking brings great benefit to heart health.", "example_uz": "Muntazam piyoda yurish yurak salomatligiga katta foyda keltiradi."},
            {"english": "certain", "ipa": "/ˈsɜː.tən/", "pronunciation_uz": "serten", "uzbek": "aniq, shubhasiz", "pos": "adj", "example_en": "I am certain that the train departs at noon.", "example_uz": "Poyezd tushda joʻnashiga toʻliq ishonchim komil."},
            {"english": "chance", "ipa": "/tʃɑːns/", "pronunciation_uz": "chans", "uzbek": "imkoniyat, imkon", "pos": "noun", "example_en": "This competition gives young writers a chance to shine.", "example_uz": "Ushbu tanlov yosh yozuvchilarga oʻzlarini koʻrsatish imkoniyatini beradi."},
            {"english": "effect", "ipa": "/ɪˈfekt/", "pronunciation_uz": "effekt", "uzbek": "taʼsir, oqibat", "pos": "noun", "example_en": "The medicine had an immediate healing effect.", "example_uz": "Dori darhol shifobaxsh taʼsir koʻrsatdi."},
            {"english": "essential", "ipa": "/ɪˈsen.ʃəl/", "pronunciation_uz": "essenshl", "uzbek": "juda muhim, zaruriy", "pos": "adj", "example_en": "Good sleep is essential for physical recovery.", "example_uz": "Yaxshi uyqu jismoniy tiklanish uchun juda zarur."},
            {"english": "far", "ipa": "/fɑːr/", "pronunciation_uz": "far", "uzbek": "uzoq, olis", "pos": "adv", "example_en": "They traveled far into the northern mountains.", "example_uz": "Ular shimoliy togʻlarning olis qismiga sayohat qildilar."},
            {"english": "focus", "ipa": "/ˈfəʊ.kəs/", "pronunciation_uz": "foukes", "uzbek": "diqqatni qaratmoq", "pos": "verb", "example_en": "Please focus on completing the urgent assignment.", "example_uz": "Iltimos, diqqatingizni shoshilinch vazifani bajarishga qarating."},
            {"english": "function", "ipa": "/ˈfʌŋk.ʃən/", "pronunciation_uz": "fankshen", "uzbek": "vazifa, faoliyat", "pos": "noun", "example_en": "The main function of the heart is to pump blood.", "example_uz": "Yurakning asosiy vazifasi qon haydashdir."},
            {"english": "grass", "ipa": "/ɡrɑːs/", "pronunciation_uz": "gras", "uzbek": "oʻt, maysazor", "pos": "noun", "example_en": "Children played happily on the green grass.", "example_uz": "Bolalar yashil maysazorda xursand boʻlib oʻynashdi."},
            {"english": "guard", "ipa": "/ɡɑːd/", "pronunciation_uz": "gard", "uzbek": "qoʻriqlamoq, soqchi", "pos": "verb", "example_en": "Trained dogs guard the entrance at night.", "example_uz": "Oʻrgatilgan itlar tunda kirish joyini qoʻriqlaydi."},
            {"english": "image", "ipa": "/ˈɪm.ɪdʒ/", "pronunciation_uz": "imidj", "uzbek": "tasvir, qiyofa", "pos": "noun", "example_en": "The satellite captured a clear image of the storm.", "example_uz": "Sunʼiy yoʻldosh boʻronning aniq tasvirini oldi."},
            {"english": "immediate", "ipa": "/ɪˈmiː.di.ət/", "pronunciation_uz": "immidiyet", "uzbek": "darhol, tezkor", "pos": "adj", "example_en": "The doctor demanded an immediate medical response.", "example_uz": "Shifokor darhol tibbiy javob berilishini talab qildi."},
            {"english": "primary", "ipa": "/ˈpraɪ.mər.i/", "pronunciation_uz": "praymeri", "uzbek": "birlamchi, asosiy", "pos": "adj", "example_en": "Safety is our primary concern on the construction site.", "example_uz": "Xavfsizlik qurilish maydonidagi asosiy tashvishimizdir."},
            {"english": "proud", "ipa": "/praʊd/", "pronunciation_uz": "praud", "uzbek": "faxrlangan, gʻururli", "pos": "adj", "example_en": "The parents were proud of their daughter's achievement.", "example_uz": "Ota-onalar qizlarining yutugʻidan faxrlandilar."},
            {"english": "remain", "ipa": "/rɪˈmeɪn/", "pronunciation_uz": "rimeyn", "uzbek": "qolmoq, oʻzgarmay qolmoq", "pos": "verb", "example_en": "Please remain seated until the plane stops fully.", "example_uz": "Samolyot toʻliq toʻxtamaguncha oʻrningizda qoling."},
            {"english": "rest", "ipa": "/rest/", "pronunciation_uz": "rest", "uzbek": "dam olmoq, dam", "pos": "verb", "example_en": "You need to rest after running the marathon.", "example_uz": "Marafonda yugurgandan keyin dam olishingiz kerak."},
            {"english": "separate", "ipa": "/ˈsep.ər.ət/", "pronunciation_uz": "sepreyt", "uzbek": "alohida, boʻlak", "pos": "adj", "example_en": "Each team member has a separate office room.", "example_uz": "Har bir jamoa aʼzosining alohida ish xonasi bor."},
            {"english": "site", "ipa": "/saɪt/", "pronunciation_uz": "sayt", "uzbek": "joy, maydoncha", "pos": "noun", "example_en": "Workers inspected the historic archaeological site.", "example_uz": "Ishchilar tarixiy arxeologik joyni koʻzdan kechirdilar."},
            {"english": "tail", "ipa": "/teɪl/", "pronunciation_uz": "teyl", "uzbek": "dum", "pos": "noun", "example_en": "The friendly puppy wagged its tail enthusiastically.", "example_uz": "Doʻstona kuchukcha dumini quvonch bilan likillatdi."},
            {"english": "trouble", "ipa": "/ˈtrʌb.əl/", "pronunciation_uz": "trabl", "uzbek": "muammo, tashvish", "pos": "noun", "example_en": "He ran into serious trouble when the car broke down.", "example_uz": "Mashina buzilib qolganda u jiddiy muammoga duch keldi."}
        ]
    },

    # ----------------- BOOK 3 -----------------
    "book-03-unit-03": {
        "title": "3-kitob: 3.3-bob",
        "category": "3-kitob: 3.3-bob",
        "badge": "3.3",
        "words": [
            {"english": "alien", "ipa": "/ˈeɪ.li.ən/", "pronunciation_uz": "eyliyen", "uzbek": "begona, yot", "pos": "adj", "example_en": "The strange customs felt completely alien to him.", "example_uz": "Gʻalati urf-odatlar unga mutlaqo yot tuyuldi."},
            {"english": "among", "ipa": "/əˈmʌŋ/", "pronunciation_uz": "emang", "uzbek": "oʻrtasida, ichida", "pos": "prep", "example_en": "The hidden cottage stood quietly among tall pine trees.", "example_uz": "Yashirin kulba baland qaragʻaylar orasida xomush turardi."},
            {"english": "chart", "ipa": "/tʃɑːt/", "pronunciation_uz": "chart", "uzbek": "xarita, chizma", "pos": "noun", "example_en": "The captain studied the navigational sea chart.", "example_uz": "Kapitan dengiz navigatsiyasi xaritasini oʻrgandi."},
            {"english": "cloud", "ipa": "/klaʊd/", "pronunciation_uz": "klaud", "uzbek": "bulut qatlami", "pos": "noun", "example_en": "Thick storm clouds covered the mountain peak.", "example_uz": "Qalin boʻron bulutlari togʻ choʻqqisini qopladi."},
            {"english": "comprehend", "ipa": "/ˌkɒm.prɪˈhend/", "pronunciation_uz": "komprihend", "uzbek": "anglamoq, idrok etmoq", "pos": "verb", "example_en": "He could not comprehend why the experiment failed.", "example_uz": "U nega tajriba muvaffaqiyatsiz boʻlganini tushuna olmadi."},
            {"english": "describe", "ipa": "/dɪˈskraɪb/", "pronunciation_uz": "deskrayb", "uzbek": "taʼriflamoq", "pos": "verb", "example_en": "The witness described the suspect accurately.", "example_uz": "Guvoh gumondorni aniq tasvirlab berdi."},
            {"english": "ever", "ipa": "/ˈev.ər/", "pronunciation_uz": "ever", "uzbek": "hech, umrida", "pos": "adv", "example_en": "No one ever expected such an incredible result.", "example_uz": "Hech kim bunday ajoyib natijani kutmagan edi."},
            {"english": "fail", "ipa": "/feɪl/", "pronunciation_uz": "feyl", "uzbek": "ish bermaslik, yiqilmoq", "pos": "verb", "example_en": "The old generator failed during the sudden freeze.", "example_uz": "Eski generator toʻsatdan sovuq tushganda ishlamay qoldi."},
            {"english": "friendly", "ipa": "/ˈfrend.li/", "pronunciation_uz": "frendli", "uzbek": "xushmuomala", "pos": "adj", "example_en": "The shop owner gave us a warm and friendly smile.", "example_uz": "Doʻkon egasi bizga samimiy va xushmuomala tabassum qildi."},
            {"english": "grade", "ipa": "/ɡreɪd/", "pronunciation_uz": "greyd", "uzbek": "saralamoq, sifat darajasi", "pos": "noun", "example_en": "Inspectors checked the grade of the building materials.", "example_uz": "Nazoratchilar qurilish materiallarining sifat darajasini tekshirdilar."},
            {"english": "instead", "ipa": "/ɪnˈsted/", "pronunciation_uz": "insted", "uzbek": "badaliga, oʻrniga", "pos": "adv", "example_en": "We chose to walk through the park instead.", "example_uz": "Biz buning oʻrniga park boʻylab yurishni tanladik."},
            {"english": "library", "ipa": "/ˈlaɪ.brər.i/", "pronunciation_uz": "laybreri", "uzbek": "kutubxona binosi", "pos": "noun", "example_en": "The national library preserves priceless manuscripts.", "example_uz": "Milliy kutubxona bebaho qoʻlyozmalarni saqlaydi."},
            {"english": "planet", "ipa": "/ˈplæn.ɪt/", "pronunciation_uz": "planet", "uzbek": "sayyora jismi", "pos": "noun", "example_en": "Jupiter is the largest planet in our solar system.", "example_uz": "Yupiter quyosh tizimidagi eng katta sayyoradir."},
            {"english": "report", "ipa": "/rɪˈpɔːt/", "pronunciation_uz": "riport", "uzbek": "xabarnoma, maʼruza", "pos": "noun", "example_en": "She presented her scientific report at the seminar.", "example_uz": "U seminarda oʻz ilmiy maʼruzasini taqdim etdi."},
            {"english": "several", "ipa": "/ˈsev.ər.əl/", "pronunciation_uz": "sevral", "uzbek": "ancha, bir necha", "pos": "adj", "example_en": "Several witnesses confirmed the sequence of events.", "example_uz": "Bir necha guvoh voqealar ketma-ketligini tasdiqladi."},
            {"english": "solve", "ipa": "/sɒlv/", "pronunciation_uz": "solv", "uzbek": "yechim topmoq", "pos": "verb", "example_en": "Detectives worked tirelessly to solve the mystery.", "example_uz": "Tergovchilar sirni yechish uchun tinimsiz ishladilar."},
            {"english": "suddenly", "ipa": "/ˈsʌd.ən.li/", "pronunciation_uz": "sadenli", "uzbek": "kutilmaganda", "pos": "adv", "example_en": "A sudden gust of wind blew the paperwork away.", "example_uz": "Kutilmagan shamol hujjatlarni uchirib yubordi."},
            {"english": "suppose", "ipa": "/səˈpəʊz/", "pronunciation_uz": "sepouz", "uzbek": "taxmin qilmoq", "pos": "verb", "example_en": "Suppose you win the scholarship, where would you go?", "example_uz": "Faraz qiling, stipendiyani yutib oldingiz, qayerga borgan boʻlardingiz?"},
            {"english": "universe", "ipa": "/ˈjuː.nɪ.vɜːs/", "pronunciation_uz": "yunivers", "uzbek": "butun borliq", "pos": "noun", "example_en": "Cosmologists study the origins of the observable universe.", "example_uz": "Kosmologlar kuzatiladigan borliqning kelib chiqishini oʻrganishadi."},
            {"english": "view", "ipa": "/vjuː/", "pronunciation_uz": "vyu", "uzbek": "qarash, nuqtai nazar", "pos": "noun", "example_en": "He shared his insightful view on international politics.", "example_uz": "U xalqaro siyosat boʻyicha oʻzining chuqur qarashlarini bildirdi."}
        ]
    },
    "book-03-unit-04": {
        "title": "3-kitob: 3.4-bob",
        "category": "3-kitob: 3.4-bob",
        "badge": "3.4",
        "words": [
            {"english": "appropriate", "ipa": "/əˈprəʊ.pri.ət/", "pronunciation_uz": "eproupriyet", "uzbek": "loyiq, munosib", "pos": "adj", "example_en": "Formal attire is appropriate for the gala dinner.", "example_uz": "Rasmiy kiyim tantanali kechki ovqat uchun munosibdir."},
            {"english": "avoid", "ipa": "/əˈvɔɪd/", "pronunciation_uz": "evoyd", "uzbek": "chetlanmoq, qochmoq", "pos": "verb", "example_en": "Drivers should avoid icy roads in winter.", "example_uz": "Haydovchilar qishda muzli yoʻllardan qochishlari kerak."},
            {"english": "behave", "ipa": "/bɪˈheɪv/", "pronunciation_uz": "biheyv", "uzbek": "oʻzini tutmoq", "pos": "verb", "example_en": "Children were taught to behave politely at the table.", "example_uz": "Bolalarga stolda oʻzlarini odobli tutish oʻrgatildi."},
            {"english": "calm", "ipa": "/kɑːm/", "pronunciation_uz": "kam", "uzbek": "xotirjam, bosiq", "pos": "adj", "example_en": "The captain remained calm during the storm.", "example_uz": "Boʻron paytida kapitan bosiq boʻlib qoldi."},
            {"english": "concern", "ipa": "/kənˈsɜːn/", "pronunciation_uz": "konsern", "uzbek": "tashvish, qaygʻurish", "pos": "noun", "example_en": "Rising pollution is a major concern for scientists.", "example_uz": "Ifloslanishning kuchayishi olimlar uchun katta tashvishdir."},
            {"english": "content", "ipa": "/kənˈtent/", "pronunciation_uz": "kontent", "uzbek": "rozi, qanoatlangan", "pos": "adj", "example_en": "He was content with his simple village life.", "example_uz": "U oʻzining oddiy qishloq hayotidan mamnun edi."},
            {"english": "expect", "ipa": "/ɪkˈspekt/", "pronunciation_uz": "ekspekt", "uzbek": "kutmoq, umid qilmoq", "pos": "verb", "example_en": "We expect hundreds of visitors at the exhibition.", "example_uz": "Koʻrgazmada yuzlab mehmonlarni kutyapmiz."},
            {"english": "frequently", "ipa": "/ˈfriː.kwənt.li/", "pronunciation_uz": "friykwentli", "uzbek": "tez-tez, bot-bot", "pos": "adv", "example_en": "She frequently travels to Madrid for business.", "example_uz": "U ish yuzasidan tez-tez Madridga boradi."},
            {"english": "habit", "ipa": "/ˈhæb.ɪt/", "pronunciation_uz": "hebit", "uzbek": "odat, koʻnikma", "pos": "noun", "example_en": "Early morning running became her daily habit.", "example_uz": "Ertalab yugurish uning kundalik odatiga aylandi."},
            {"english": "instruct", "ipa": "/ɪnˈstrʌkt/", "pronunciation_uz": "instrakt", "uzbek": "yoʻl-yoʻriq koʻrsatmoq", "pos": "verb", "example_en": "The coach instructed the players before the game.", "example_uz": "Murabbiy oʻyin oldidan oʻyinchilarga koʻrsatmalar berdi."},
            {"english": "issue", "ipa": "/ˈɪʃ.uː/", "pronunciation_uz": "ishyu", "uzbek": "masala, muammo", "pos": "noun", "example_en": "Water shortage is a pressing global issue.", "example_uz": "Suv tanqisligi dolzarb global muammodir."},
            {"english": "none", "ipa": "/nʌn/", "pronunciation_uz": "nan", "uzbek": "hech qaysisi", "pos": "pron", "example_en": "None of the applicants met all the requirements.", "example_uz": "Nomzodlarning hech biri barcha talablarga javob bermadi."},
            {"english": "patient", "ipa": "/ˈpeɪ.ʃənt/", "pronunciation_uz": "peyshent", "uzbek": "sabirli, bardoshli", "pos": "adj", "example_en": "Teachers must be patient with young learners.", "example_uz": "Oʻqituvchilar yosh oʻquvchilarga nisbatan sabrli boʻlishi kerak."},
            {"english": "positive", "ipa": "/ˈpɒz.ə.tɪv/", "pronunciation_uz": "pozitiv", "uzbek": "ijobiy, umidbaxsh", "pos": "adj", "example_en": "Try to maintain a positive attitude under pressure.", "example_uz": "Bosim ostida ham ijobiy kayfiyatni saqlashga harakat qiling."},
            {"english": "punish", "ipa": "/ˈpʌn.ɪʃ/", "pronunciation_uz": "panish", "uzbek": "jazolamoq", "pos": "verb", "example_en": "Laws exist to punish those who commit crimes.", "example_uz": "Qonunlar jinoyat sodir etganlarni jazolash uchun mavjuddir."},
            {"english": "represent", "ipa": "/ˌrep.rɪˈzent/", "pronunciation_uz": "reprizent", "uzbek": "vakillik qilmoq", "pos": "verb", "example_en": "Lawyers represent their clients in a court of law.", "example_uz": "Advokatlar sudda oʻz mijozlarining manfaatlarini ifodalaydilar."},
            {"english": "spread", "ipa": "/spred/", "pronunciation_uz": "spred", "uzbek": "tarqalmoq, yoyilmoq", "pos": "verb", "example_en": "News of the discovery spread across the country rapidly.", "example_uz": "Kashfiyot haqidagi xabar butun mamlakat boʻylab tez tarqaldi."},
            {"english": "village", "ipa": "/ˈvɪl.ɪdʒ/", "pronunciation_uz": "vilidj", "uzbek": "qishloq", "pos": "noun", "example_en": "They live in a quiet fishing village near the sea.", "example_uz": "Ular dengiz yaqinidagi tinch baliqchilar qishlogʻida yashashadi."},
            {"english": "aware", "ipa": "/əˈweər/", "pronunciation_uz": "eveer", "uzbek": "xabardor, ogoh", "pos": "adj", "example_en": "Citizens should be aware of environmental changes.", "example_uz": "Fuqarolar atrof-muhit oʻzgarishlaridan xabardor boʻlishlari kerak."},
            {"english": "badly", "ipa": "/ˈbæd.li/", "pronunciation_uz": "bedli", "uzbek": "juda yomon, qattiq", "pos": "adv", "example_en": "His leg was badly injured in the fall.", "example_uz": "Yiqilganda uning oyogʻi qattiq jarohatlandi."}
        ]
    },
    "book-03-unit-05": {
        "title": "3-kitob: 3.5-bob",
        "category": "3-kitob: 3.5-bob",
        "badge": "3.5",
        "words": [
            {"english": "belong", "ipa": "/bɪˈlɒŋ/", "pronunciation_uz": "bilong", "uzbek": "tegishli boʻlmoq", "pos": "verb", "example_en": "This antique violin belongs to a famous soloist.", "example_uz": "Bu qadimiy skripka mashhur yakkaxonga tegishli."},
            {"english": "continue", "ipa": "/kənˈtɪn.juː/", "pronunciation_uz": "kontinyu", "uzbek": "davom ettirmoq", "pos": "verb", "example_en": "Please continue your presentation despite the interruption.", "example_uz": "Xalal berishga qaramay, taqdimotingizni davom ettiring."},
            {"english": "error", "ipa": "/ˈer.ər/", "pronunciation_uz": "error", "uzbek": "xato, yanglishish", "pos": "noun", "example_en": "The accountant corrected a calculation error.", "example_uz": "Hisobchi hisob-kitobdagi xatoni tuzatdi."},
            {"english": "experience", "ipa": "/ɪkˈspɪə.ri.əns/", "pronunciation_uz": "ekspiriens", "uzbek": "tajriba, kechinma", "pos": "noun", "example_en": "Volunteering was a valuable life experience.", "example_uz": "Koʻngillilik qimmatli hayotiy tajriba boʻldi."},
            {"english": "field", "ipa": "/fiːld/", "pronunciation_uz": "fiyld", "uzbek": "dala, soha", "pos": "noun", "example_en": "Cattle grazed in the wide green field.", "example_uz": "Keng yashil dalada mollar oʻtlardi."},
            {"english": "judgment", "ipa": "/ˈdʒʌdʒ.mənt/", "pronunciation_uz": "jadjment", "uzbek": "hukm, xulosa", "pos": "noun", "example_en": "Trust your own judgment when making career choices.", "example_uz": "Kasb tanlashda oʻz xulosangizga ishoning."},
            {"english": "likely", "ipa": "/ˈlaɪ.kli/", "pronunciation_uz": "laykli", "uzbek": "ehtimolli, boʻlishi mumkin", "pos": "adj", "example_en": "Rain is likely later this evening.", "example_uz": "Kechqurun yomgʻir yogʻishi ehtimoli yuqori."},
            {"english": "normal", "ipa": "/ˈnɔː.məl/", "pronunciation_uz": "norml", "uzbek": "odatiy, meʼyoriy", "pos": "adj", "example_en": "His body temperature returned to normal.", "example_uz": "Uning tana harorati meʼyoriga qaytdi."},
            {"english": "rare", "ipa": "/reər/", "pronunciation_uz": "reer", "uzbek": "noyob, kamyob", "pos": "adj", "example_en": "Astronomers witnessed a rare celestial alignment.", "example_uz": "Astronomlar sayyoralarning noyob joylashuviga guvoh boʻlishdi."},
            {"english": "relax", "ipa": "/rɪˈlæks/", "pronunciation_uz": "rileks", "uzbek": "hordiq chiqarmoq", "pos": "verb", "example_en": "Listening to classical music helps me relax.", "example_uz": "Klassik musiqa tinglash menga dam olishga yordam beradi."},
            {"english": "request", "ipa": "/rɪˈkwest/", "pronunciation_uz": "rikvest", "uzbek": "iltimos qilmoq, soʻrov", "pos": "verb", "example_en": "Passengers may request a special diet meal.", "example_uz": "Yoʻlovchilar maxsus parhez taomini soʻrashlari mumkin."},
            {"english": "reside", "ipa": "/rɪˈzaɪd/", "pronunciation_uz": "rizayd", "uzbek": "istiqomat qilmoq", "pos": "verb", "example_en": "Many diplomats reside in the capital city.", "example_uz": "Koʻplab diplomatlar poytaxtda istiqomat qilishadi."},
            {"english": "roll", "ipa": "/rəʊl/", "pronunciation_uz": "roul", "uzbek": "dumalatmoq, aylanmoq", "pos": "verb", "example_en": "Roll the ball toward the pins.", "example_uz": "Toʻpni keglilar tomon dumalating."},
            {"english": "since", "ipa": "/sɪns/", "pronunciation_uz": "sins", "uzbek": "beri, -dan buyon", "pos": "prep", "example_en": "I haven't seen him since last summer.", "example_uz": "Men uni oʻtgan yozdan beri koʻrmaganman."},
            {"english": "visible", "ipa": "/ˈvɪz.ə.bəl/", "pronunciation_uz": "vizibl", "uzbek": "koʻrinadigan, koʻrinarli", "pos": "adj", "example_en": "The lighthouse was visible through the thick sea mist.", "example_uz": "Qalin dengiz tumanida mayoq koʻrinib turardi."},
            {"english": "advantage", "ipa": "/ədˈvɑːn.tɪdʒ/", "pronunciation_uz": "edvantidj", "uzbek": "afzallik, ustunlik", "pos": "noun", "example_en": "Speaking two languages gives you a major advantage.", "example_uz": "Ikki tilni bilish sizga katta ustunlik beradi."},
            {"english": "cause", "ipa": "/kɔːz/", "pronunciation_uz": "koz", "uzbek": "sabab boʻlmoq, vaj", "pos": "verb", "example_en": "Heavy storms cause widespread travel delays.", "example_uz": "Kuchli boʻronlar safarlarning keng kechikishiga sabab boʻladi."},
            {"english": "face", "ipa": "/feɪs/", "pronunciation_uz": "feys", "uzbek": "roʻpara kelmoq, yuzlanmoq", "pos": "verb", "example_en": "Athletes must face strong competition with confidence.", "example_uz": "Sportchilar kuchli raqobatga ishonch bilan roʻpara kelishlari kerak."},
            {"english": "fellow", "ipa": "/ˈfel.əʊ/", "pronunciation_uz": "fellou", "uzbek": "safdosh, hamkasb", "pos": "noun", "example_en": "He consulted with his fellow researchers on the paper.", "example_uz": "U maqola boʻyicha tadqiqotchi safdoshlari bilan maslahatlashdi."},
            {"english": "motion", "ipa": "/ˈməʊ.ʃən/", "pronunciation_uz": "moushen", "uzbek": "harakat, qoʻzgʻalish", "pos": "noun", "example_en": "The gentle rocking motion of the boat helped him sleep.", "example_uz": "Qayiqning mayin tebranish harakati unga uxlab qolishga yordam berdi."}
        ]
    },

    # ----------------- BOOK 4 -----------------
    "book-04-unit-03": {
        "title": "4-kitob: 4.3-bob",
        "category": "4-kitob: 4.3-bob",
        "badge": "4.3",
        "words": [
            {"english": "arise", "ipa": "/əˈraɪz/", "pronunciation_uz": "erayz", "uzbek": "paydo boʻlmoq, yuzaga kelmoq", "pos": "verb", "example_en": "Difficult questions may arise during the negotiations.", "example_uz": "Muzokaralar chogʻida qiyin savollar yuzaga kelishi mumkin."},
            {"english": "benefactor", "ipa": "/ˈben.ɪ.fæk.tər/", "pronunciation_uz": "benefakter", "uzbek": "homiy, xayrixoh", "pos": "noun", "example_en": "An anonymous benefactor donated funds for the new library.", "example_uz": "Nomaʼlum homiy yangi kutubxona uchun mablagʻ xayriya qildi."},
            {"english": "blacksmith", "ipa": "/ˈblæk.smɪθ/", "pronunciation_uz": "bleksmit", "uzbek": "temirchi", "pos": "noun", "example_en": "The village blacksmith shaped hot steel on the anvil.", "example_uz": "Qishloq temirchisi qizigan poʻlatni sandonda bolgʻaladi."},
            {"english": "charitable", "ipa": "/ˈtʃær.ɪ.tə.bəl/", "pronunciation_uz": "cheritebl", "uzbek": "saxiy, xayr-ehsonli", "pos": "adj", "example_en": "The organization supports charitable projects worldwide.", "example_uz": "Tashkilot butun dunyo boʻylab xayriya loyihalarini qoʻllab-quvvatlaydi."},
            {"english": "chimney", "ipa": "/ˈtʃɪm.ni/", "pronunciation_uz": "chimni", "uzbek": "moʻri, quvur", "pos": "noun", "example_en": "Smoke curled upwards from the brick chimney.", "example_uz": "Gʻishtin moʻridan tutun yuqoriga buralib chiqdi."},
            {"english": "compensate", "ipa": "/ˈkɒm.pən.seɪt/", "pronunciation_uz": "kompenseyt", "uzbek": "qoplamoq, tovon toʻlamoq", "pos": "verb", "example_en": "The company will compensate workers for extra hours.", "example_uz": "Kompaniya ishchilarga ortiqcha ishlagan soatlari uchun haq toʻlaydi."},
            {"english": "encounter", "ipa": "/ɪŋˈkaʊn.tər/", "pronunciation_uz": "enkaunter", "uzbek": "toʻqnash kelmoq, uchratmoq", "pos": "verb", "example_en": "Travelers may encounter wild animals along the forest trail.", "example_uz": "Sayohatchilar oʻrmon yoʻlida yovvoyi hayvonlarga duch kelishi mumkin."},
            {"english": "exceed", "ipa": "/ɪkˈsiːd/", "pronunciation_uz": "eksiyd", "uzbek": "oshib ketmoq, oʻtib ketmoq", "pos": "verb", "example_en": "Never exceed the posted highway speed limit.", "example_uz": "Hech qachon belgilangan yoʻl tezligidan oshib ketmang."},
            {"english": "forge", "ipa": "/fɔːdʒ/", "pronunciation_uz": "fordj", "uzbek": "temirchilik doʻkoni, bolgʻalamoq", "pos": "noun", "example_en": "The smith hammered glowing horseshoes in the forge.", "example_uz": "Temirchi ustaxonada qizigan taqalarni bolgʻaladi."},
            {"english": "humble", "ipa": "/ˈhʌm.bəl/", "pronunciation_uz": "hambl", "uzbek": "kamtarin, oddiy", "pos": "adj", "example_en": "Despite great fame he remained a humble man.", "example_uz": "Katta shuhratiga qaramay, u kamtarin inson boʻlib qoldi."},
            {"english": "iron", "ipa": "/ˈaɪən/", "pronunciation_uz": "ayren", "uzbek": "temir", "pos": "noun", "example_en": "Wrought iron was used to build the ornate gate.", "example_uz": "Nafis darvozani yasashda qattiq temir ishlatildi."},
            {"english": "ladder", "ipa": "/ˈlæd.ər/", "pronunciation_uz": "ladder", "uzbek": "narvon", "pos": "noun", "example_en": "He climbed the tall ladder to repair the roof.", "example_uz": "U tomni tuzatish uchun baland narvonga chiqdi."},
            {"english": "modest", "ipa": "/ˈmɒd.ɪst/", "pronunciation_uz": "modest", "uzbek": "kamtar, moʻtadil", "pos": "adj", "example_en": "They live in a modest apartment on the city outskirts.", "example_uz": "Ular shahar chetidagi kamtarona kvartirada yashashadi."},
            {"english": "occupy", "ipa": "/ˈɒk.jə.paɪ/", "pronunciation_uz": "okyupay", "uzbek": "egallamoq, band qilmoq", "pos": "verb", "example_en": "Books occupy every available shelf in his study.", "example_uz": "Kitoblar uning ish xonasidagi barcha boʻsh javonlarni egallagan."},
            {"english": "penny", "ipa": "/ˈpen.i/", "pronunciation_uz": "penni", "uzbek": "penni, chaqa", "pos": "noun", "example_en": "He saved every penny to buy a bicycle.", "example_uz": "U velosiped sotib olish uchun har bir tiyinini tejadi."},
            {"english": "preach", "ipa": "/priːtʃ/", "pronunciation_uz": "priych", "uzbek": "vaʼz qilmoq, nasihat qilmoq", "pos": "verb", "example_en": "Leaders should preach peace and tolerance.", "example_uz": "Yetakchilar tinchlik va bagʻrikenglikni targʻib qilishlari kerak."},
            {"english": "prosper", "ipa": "/ˈprɒs.pər/", "pronunciation_uz": "prosper", "uzbek": "ravnaq topmoq, gullab-yashnamoq", "pos": "verb", "example_en": "The trade town continued to prosper under fair laws.", "example_uz": "Savdo shaharchasi adolatli qonunlar ostida ravnaq topishda davom etdi."},
            {"english": "province", "ipa": "/ˈprɒv.ɪns/", "pronunciation_uz": "provins", "uzbek": "viloyat, provinsiya", "pos": "noun", "example_en": "The northern province produces abundant fruit and wheat.", "example_uz": "Shimoliy viloyat moʻl-koʻl meva va bugʻdoy yetishtiradi."},
            {"english": "satisfaction", "ipa": "/ˌsæt.ɪsˈfæk.ʃən/", "pronunciation_uz": "setisfekshen", "uzbek": "qoniqish, mamnunlik", "pos": "noun", "example_en": "Finishing the painting gave her immense satisfaction.", "example_uz": "Rasmni tugatish unga cheksiz mamnuniyat bagʻishladi."},
            {"english": "sustain", "ipa": "/səˈsteɪn/", "pronunciation_uz": "sesteyn", "uzbek": "saqlab turmoq, taʼminlamoq", "pos": "verb", "example_en": "Oasis springs sustain life throughout the dry desert.", "example_uz": "Voha buloqlari qurgʻoqchil choʻlda hayotni saqlab turadi."}
        ]
    },
    "book-04-unit-04": {
        "title": "4-kitob: 4.4-bob",
        "category": "4-kitob: 4.4-bob",
        "badge": "4.4",
        "words": [
            {"english": "acquire", "ipa": "/əˈkwaɪər/", "pronunciation_uz": "ekvayer", "uzbek": "orttirmoq, qoʻlga kiritmoq", "pos": "verb", "example_en": "Students acquire deep knowledge through dedicated practice.", "example_uz": "Talabalar astoydil mashq qilish orqali chuqur bilimga ega boʻladilar."},
            {"english": "awkward", "ipa": "/ˈɔː.kwəd/", "pronunciation_uz": "okverd", "uzbek": "noqulay, oʻngʻaysiz", "pos": "adj", "example_en": "There was an awkward silence in the crowded room.", "example_uz": "Gavjum xonada noqulay sukunat paydo boʻldi."},
            {"english": "caretaker", "ipa": "/ˈkeəˌteɪ.kər/", "pronunciation_uz": "kerteyker", "uzbek": "qorovul, nazoratchi", "pos": "noun", "example_en": "The caretaker maintains the school garden and grounds.", "example_uz": "Qorovul maktab bogʻi va hovlisini parvarish qiladi."},
            {"english": "deceive", "ipa": "/dɪˈsiːv/", "pronunciation_uz": "disiyv", "uzbek": "aldamoq, chalgʻitmoq", "pos": "verb", "example_en": "Dishonest sellers attempt to deceive customers.", "example_uz": "Insofsiz sotuvchilar mijozlarni aldashga urinishadi."},
            {"english": "discourage", "ipa": "/dɪˈskʌr.ɪdʒ/", "pronunciation_uz": "diskaridj", "uzbek": "shashtini qaytarmoq", "pos": "verb", "example_en": "Do not let early setbacks discourage you from pursuing your goal.", "example_uz": "Dastlabki muvaffaqiyatsizliklar maqsadingizdan qaytarmasin."},
            {"english": "fake", "ipa": "/feɪk/", "pronunciation_uz": "feyk", "uzbek": "soxta, yasama", "pos": "adj", "example_en": "Experts recognized the antique painting was a fake.", "example_uz": "Mutaxassislar qadimiy rasm soxta ekanligini aniqladilar."},
            {"english": "hatred", "ipa": "/ˈheɪ.trɪd/", "pronunciation_uz": "heytrid", "uzbek": "nafrat, adovat", "pos": "noun", "example_en": "Education helps eliminate prejudice and hatred.", "example_uz": "Taʼlim xurofot va nafratni yoʻq qilishga yordam beradi."},
            {"english": "hut", "ipa": "/hʌt/", "pronunciation_uz": "hat", "uzbek": "kulba, kapa", "pos": "noun", "example_en": "Hikers found shelter in a rustic wooden hut.", "example_uz": "Sayyohlar yogʻoch kulbadan boshpana topdilar."},
            {"english": "inferior", "ipa": "/ɪnˈfɪə.ri.ər/", "pronunciation_uz": "inferiyer", "uzbek": "pastroq, sifatsizroq", "pos": "adj", "example_en": "These cheap imitation goods are of inferior quality.", "example_uz": "Ushbu arzon taqlid mollar sifatsizroqdir."},
            {"english": "lodge", "ipa": "/lɒdʒ/", "pronunciation_uz": "lodj", "uzbek": "ovchilar uyi, qoʻnoq", "pos": "noun", "example_en": "We stayed at a cozy mountain lodge during our ski trip.", "example_uz": "Changʻi sayohati paytida shinam togʻ mehmonxonasida qoldik."},
            {"english": "neglect", "ipa": "/nɪˈɡlekt/", "pronunciation_uz": "niglekt", "uzbek": "eʼtiborsiz qoldirmoq", "pos": "verb", "example_en": "Never neglect your physical health while studying.", "example_uz": "Oʻqish paytida jismoniy sogʻligʻingizni hech qachon eʼtiborsiz qoldirmang."},
            {"english": "newcomer", "ipa": "/ˈnjuːˌkʌm.ər/", "pronunciation_uz": "nyukamer", "uzbek": "yangi kelgan odam", "pos": "noun", "example_en": "The community warmly welcomed every newcomer.", "example_uz": "Mahalla har bir yangi kelgan odamni iliq kutib oldi."},
            {"english": "offense", "ipa": "/əˈfens/", "pronunciation_uz": "offens", "uzbek": "huquqbuzarlik, ranjish", "pos": "noun", "example_en": "Stealing is a punishable criminal offense.", "example_uz": "Oʻgʻrilik jazolanadigan jinoiy huquqbuzarlikdir."},
            {"english": "overlook", "ipa": "/ˌəʊ.vəˈlʊk/", "pronunciation_uz": "overluk", "uzbek": "koʻzdan qochirmoq, qaramoq", "pos": "verb", "example_en": "Do not overlook the small details in the contract.", "example_uz": "Shartnomadagi mayda tafsilotlarni koʻzdan qochirmang."},
            {"english": "repay", "ipa": "/rɪˈpeɪ/", "pronunciation_uz": "ripey", "uzbek": "qaytarib toʻlamoq", "pos": "verb", "example_en": "I will repay the borrowed money by Friday.", "example_uz": "Qarzga olingan pulni juma kunigacha toʻlayman."},
            {"english": "ridiculous", "ipa": "/rɪˈdɪk.jə.ləs/", "pronunciation_uz": "ridikyules", "uzbek": "kulgili, bemaʼni", "pos": "adj", "example_en": "Charging fifty dollars for a small sandwich is ridiculous.", "example_uz": "Kichkina buterbrod uchun ellik dollar soʻrash bemaʼnilikdir."},
            {"english": "satisfactory", "ipa": "/ˌsæt.ɪsˈfæk.tər.i/", "pronunciation_uz": "setisfekteri", "uzbek": "qoniqarli", "pos": "adj", "example_en": "The repair work was completed to a satisfactory standard.", "example_uz": "Taʼmirlash ishlari qoniqarli darajada yakunlandi."},
            {"english": "shepherd", "ipa": "/ˈʃep.əd/", "pronunciation_uz": "shepherd", "uzbek": "choʻpon", "pos": "noun", "example_en": "The loyal shepherd watched his sheep on the hillside.", "example_uz": "Sadoqatli choʻpon adirda qoʻylarini boqdi."},
            {"english": "venture", "ipa": "/ˈven.tʃər/", "pronunciation_uz": "vencher", "uzbek": "tavakkal ish, qadam bosmoq", "pos": "noun", "example_en": "Starting an online store was a bold business venture.", "example_uz": "Onlayn doʻkon ochish jasoratli tadbirkorlik tashabbusi boʻldi."},
            {"english": "wheat", "ipa": "/wiːt/", "pronunciation_uz": "viyt", "uzbek": "bugʻdoy", "pos": "noun", "example_en": "Golden wheat rippled in the gentle autumn breeze.", "example_uz": "Mayin kuz shabadasida tilla rang bugʻdoy toʻlqinlandi."}
        ]
    },
    "book-04-unit-05": {
        "title": "4-kitob: 4.5-bob",
        "category": "4-kitob: 4.5-bob",
        "badge": "4.5",
        "words": [
            {"english": "alley", "ipa": "/ˈæl.i/", "pronunciation_uz": "elli", "uzbek": "tor koʻcha, xiyoboncha", "pos": "noun", "example_en": "A narrow cobblestone alley led behind the historic theater.", "example_uz": "Tor toshkoʻcha tarixiy teatr orqasiga olib bordi."},
            {"english": "ax", "ipa": "/æks/", "pronunciation_uz": "eks", "uzbek": "bolta", "pos": "noun", "example_en": "The lumberjack chopped dry firewood with a sharp ax.", "example_uz": "Oʻtinchi oʻtkir bolta bilan quruq oʻtin yordi."},
            {"english": "bunch", "ipa": "/bʌntʃ/", "pronunciation_uz": "banch", "uzbek": "dasta, shingil", "pos": "noun", "example_en": "She bought a fresh bunch of sweet grapes at the market.", "example_uz": "U bozordan bir shingil shirin uzum sotib oldi."},
            {"english": "chore", "ipa": "/tʃɔːr/", "pronunciation_uz": "chor", "uzbek": "uy yumushi, kundalik vazifa", "pos": "noun", "example_en": "Washing the dinner dishes was his assigned evening chore.", "example_uz": "Kechki idishlarni yuvish unga topshirilgan vazifa edi."},
            {"english": "decent", "ipa": "/ˈdiː.sənt/", "pronunciation_uz": "diysent", "uzbek": "tuzuk, risoladagidek", "pos": "adj", "example_en": "They earned a decent salary through honest skilled labor.", "example_uz": "Ular halol mehnati bilan risoladagidek maosh oldilar."},
            {"english": "disgrace", "ipa": "/dɪsˈɡreɪs/", "pronunciation_uz": "disgreys", "uzbek": "sharmandalik, dogʻ", "pos": "noun", "example_en": "Cheating on an honor code brings disgrace to the institution.", "example_uz": "Or-nomus qoidalarini buzish muassasaga sharmandalik keltiradi."},
            {"english": "elbow", "ipa": "/ˈel.bəʊ/", "pronunciation_uz": "elbou", "uzbek": "tirsak", "pos": "noun", "example_en": "He rested his elbow on the desk while thinking.", "example_uz": "U oʻyga choʻmib tirsagini stolga tiradi."},
            {"english": "grateful", "ipa": "/ˈɡreɪt.fəl/", "pronunciation_uz": "greytful", "uzbek": "minnatdor, roziligini bildiruvchi", "pos": "adj", "example_en": "We are deeply grateful for your generous medical aid.", "example_uz": "Saxiy tibbiy yordamingiz uchun chuqur minnatdormiz."},
            {"english": "irritate", "ipa": "/ˈɪr.ɪ.teɪt/", "pronunciation_uz": "irriteyt", "uzbek": "gʻashiga tegmoq, qitiqlamoq", "pos": "verb", "example_en": "Loud construction noise can irritate neighborhood residents.", "example_uz": "Baland qurilish shovqini mahalla aholisining gʻashiga tegishi mumkin."},
            {"english": "kid", "ipa": "/kɪd/", "pronunciation_uz": "kid", "uzbek": "hazillashmoq, yosh bola", "pos": "verb", "example_en": "Don't take it personally, he was only kidding.", "example_uz": "Koʻnglingizga olmang, u shunchaki hazillashayotgan edi."},
            {"english": "loose", "ipa": "/luːs/", "pronunciation_uz": "luws", "uzbek": "boʻsh, keng", "pos": "adj", "example_en": "Wear loose cotton clothing in the hot summer months.", "example_uz": "Issiq yoz oylarida keng paxtali kiyim kiying."},
            {"english": "offend", "ipa": "/əˈfend/", "pronunciation_uz": "offend", "uzbek": "xafa qilmoq, ranjitmoq", "pos": "verb", "example_en": "I did not mean to offend your religious beliefs.", "example_uz": "Diniy eʼtiqodingizni xafa qilish niyatim yoʻq edi."},
            {"english": "overnight", "ipa": "/ˌəʊ.vəˈnaɪt/", "pronunciation_uz": "overnayt", "uzbek": "bir kechada, tunda", "pos": "adv", "example_en": "The sleeper train traveled overnight to the capital.", "example_uz": "Yotoqli poyezd bir kechada poytaxtga yetib bordi."},
            {"english": "persist", "ipa": "/pəˈsɪst/", "pronunciation_uz": "persist", "uzbek": "qaysarlik bilan davom etmoq", "pos": "verb", "example_en": "If symptoms persist for three days, consult a physician.", "example_uz": "Agar alomatlar uch kun davom etsa, shifokorga murojaat qiling."},
            {"english": "pine", "ipa": "/paɪn/", "pronunciation_uz": "payn", "uzbek": "qaragʻay daraxti", "pos": "noun", "example_en": "The scent of wild pine filled the crisp mountain air.", "example_uz": "Yovvoyi qaragʻay hidi toza togʻ havosini toʻldirdi."},
            {"english": "scar", "ipa": "/skɑːr/", "pronunciation_uz": "skar", "uzbek": "chandiq, jarohat izi", "pos": "noun", "example_en": "A faint surgical scar remained on his left knee.", "example_uz": "Uning chap tizzasida xira jarrohlik chandigʻi qoldi."},
            {"english": "sensation", "ipa": "/senˈseɪ.ʃən/", "pronunciation_uz": "senseyshen", "uzbek": "sezgi, tuygʻu", "pos": "noun", "example_en": "Walking on soft sand produced a pleasant sensation.", "example_uz": "Yumshoq qum ustida yurish yoqimli tuygʻu uygʻotdi."},
            {"english": "sled", "ipa": "/sled/", "pronunciation_uz": "sled", "uzbek": "chana", "pos": "noun", "example_en": "Excited children pulled a red wooden sled up the snowy hill.", "example_uz": "Hayajonlangan bolalar qorli tepalikka qizil yogʻoch chanani tortib chiqdilar."},
            {"english": "tease", "ipa": "/tiːz/", "pronunciation_uz": "tiyz", "uzbek": "mazax qilmoq, tegishmoq", "pos": "verb", "example_en": "Brothers often playfully tease each other at home.", "example_uz": "Aka-ukalar uyda koʻpincha bir-birlariga hazillashib tegishishadi."},
            {"english": "valentine", "ipa": "/ˈvæl.ən.taɪn/", "pronunciation_uz": "valentayn", "uzbek": "sevgi tabriknomasi", "pos": "noun", "example_en": "He anonymously sent a sweet handwritten valentine card.", "example_uz": "U anonim tarzda qoʻlda yozilgan shirin sevgi xatini yubordi."}
        ]
    }
}


def build_and_save():
    DECKS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Save Book units ensuring every word has 'category'
    for slug, payload in BOOK_DATA.items():
        cat = payload["category"]
        for w in payload["words"]:
            w["category"] = cat
        out_path = DECKS_DIR / f"{slug}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out_path.name}: {len(payload['words'])} words")


if __name__ == "__main__":
    build_and_save()
