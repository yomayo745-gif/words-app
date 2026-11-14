"""
Generate topic-36-situational-dialogues.json:
120 essential real-life dialogues across:
1. Airport & Air Travel
2. Restaurant, Cafe & Dining
3. Hotel & Accommodation
4. Taxi, Public Transport & Directions
5. Shopping, Clothes & Supermarkets
6. Health, Doctor & Pharmacy
7. Work, Meetings & Career
8. Daily Socializing & Small Talk
"""

from __future__ import annotations
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = PROJECT_ROOT / "webapp" / "data" / "decks"

DIALOGUES = [
    # 1. Airport & Flights
    {
        "english": "May I see your passport and boarding pass, please?",
        "ipa": "/meɪ aɪ siː jɔːr ˈpɑːs.pɔːt ænd ˈbɔː.dɪŋ pɑːs pliːz/",
        "pronunciation_uz": "mey ay siy yor pasport end bording pas pliyz",
        "uzbek": "Pasportingiz va chiqish talonini koʻrsatsangiz, iltimos?",
        "pos": "phr",
        "example_en": "A: May I see your passport and boarding pass, please? B: Yes, here they are.",
        "example_uz": "A: Pasportingiz va samolyotga chiqish talonini koʻrsatsangiz? B: Ha, mana marhamat.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Where can I collect my checked luggage?",
        "ipa": "/weər kæn aɪ kəˈlekt maɪ tʃekt ˈlʌɡ.ɪdʒ/",
        "pronunciation_uz": "veer ken ay kolekt may chekt laggidj",
        "uzbek": "Topshirilgan yukimni qayerdan olsam boʻladi?",
        "pos": "phr",
        "example_en": "A: Where can I collect my checked luggage? B: At carousel number four.",
        "example_uz": "A: Yukimni qayerdan olsam boʻladi? B: Toʻrtinchi bagaj tasmasidan.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Which gate does the flight to London depart from?",
        "ipa": "/wɪtʃ ɡeɪt dʌz ðə flaɪt tuː ˈlʌn.dən dɪˈpɑːt frɒm/",
        "pronunciation_uz": "vich geyt daz ze flayt tu London dipart from",
        "uzbek": "Londonga reys qaysi chiqishdan joʻnaydi?",
        "pos": "phr",
        "example_en": "A: Which gate does the flight depart from? B: Gate 24B, boarding has begun.",
        "example_uz": "A: Reys qaysi chiqishdan joʻnaydi? B: 24B chiqishidan, chiqish boshlandi.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could I request a window seat if available?",
        "ipa": "/kʊd aɪ rɪˈkwest ə ˈwɪn.dəʊ siːt ɪf əˈveɪ.lə.bəl/",
        "pronunciation_uz": "kud ay rikvest e vindou siyt if eveylebl",
        "uzbek": "Boʻsh boʻlsa, deraza yonidagi oʻrindiqni soʻrasam boʻladimi?",
        "pos": "phr",
        "example_en": "A: Could I request a window seat if available? B: Certainly, seat 14A is open.",
        "example_uz": "A: Boʻsh boʻlsa, deraza yonidagi oʻrindiqni soʻrasam boʻladimi? B: Albatta, 14A oʻrindiq boʻsh.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "How long is the layover between connecting flights?",
        "ipa": "/haʊ lɒŋ ɪz ðə ˈleɪˌəʊ.vər bɪˈtwiːn kəˈnek.tɪŋ flaɪts/",
        "pronunciation_uz": "hau long iz ze ley-over bitviyn konekting flayts",
        "uzbek": "Ulanish reyslari orasidagi oraliq kutish qancha davom etadi?",
        "pos": "phr",
        "example_en": "A: How long is the layover? B: You have about two hours in Istanbul.",
        "example_uz": "A: Kutish qancha vaqt oladi? B: Istanbulda taxminan ikki soat vaqtingiz bor.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Is this backpack within the cabin baggage allowance?",
        "ipa": "/ɪz ðɪs ˈbæk.pæk wɪˈðɪn ðə ˈkæb.ɪn ˈbæɡ.ɪdʒ əˈlaʊ.əns/",
        "pronunciation_uz": "iz zis bekpek vizin ze kebin beggidj elavens",
        "uzbek": "Ushbu ryukzak qoʻl yuki meʼyoriga toʻgʻri keladimi?",
        "pos": "phr",
        "example_en": "A: Is this backpack allowed in the cabin? B: Yes, it easily fits overhead.",
        "example_uz": "A: Bu ryukzakni salonga olsa boʻladimi? B: Ha, tepaga bemalol sigʻadi.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "I have nothing to declare at customs.",
        "ipa": "/aɪ hæv ˈnʌθ.ɪŋ tuː dɪˈkleər æt ˈkʌs.təmz/",
        "pronunciation_uz": "ay hev nasing tu dikleer et kastemz",
        "uzbek": "Bojxonada eʼlon qiladigan hech narsam yoʻq.",
        "pos": "phr",
        "example_en": "A: Do you have anything to declare? B: No, I have nothing to declare at customs.",
        "example_uz": "A: Eʼlon qiladigan narsangiz bormi? B: Yoʻq, bojxonada hech narsam yoʻq.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "What is the primary purpose of your trip?",
        "ipa": "/wɒt ɪz ðə ˈpraɪ.mər.i ˈpɜː.pəs əv jɔːr trɪp/",
        "pronunciation_uz": "vot iz ze praymeri porpes ov yor trip",
        "uzbek": "Safaringizning asosiy maqsadi nima?",
        "pos": "phr",
        "example_en": "A: What is the primary purpose of your trip? B: Tourism and holiday.",
        "example_uz": "A: Safaringizning asosiy maqsadi nima? B: Sayyohlik va taʼtil.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 2. Restaurant & Cafe
    {
        "english": "A table for two near the window, please.",
        "ipa": "/ə ˈteɪ.bəl fɔːr tuː nɪər ðə ˈwɪn.dəʊ pliːz/",
        "pronunciation_uz": "e teybl for tu nier ze vindou pliyz",
        "uzbek": "Iltimos, deraza yonidan ikki kishilik stol bering.",
        "pos": "phr",
        "example_en": "A: Welcome! B: Hello, a table for two near the window, please.",
        "example_uz": "A: Xush kelibsiz! B: Salom, deraza yonidan ikki kishilik joy bersangiz.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could we see the dinner menu, please?",
        "ipa": "/kʊd wiː siː ðə ˈdɪn.ər ˈmen.juː pliːz/",
        "pronunciation_uz": "kud viy siy ze dinner menyu pliyz",
        "uzbek": "Kechki ovqat menyusini koʻrsatsangiz, iltimos?",
        "pos": "phr",
        "example_en": "A: Could we see the dinner menu, please? B: Right away, here it is.",
        "example_uz": "A: Kechki menyuni koʻrsatsangiz? B: Hozir, mana marhamat.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "What do you recommend as the chef's special?",
        "ipa": "/wɒt duː juː ˌrek.əˈmend æz ðə ʃefs ˈspeʃ.əl/",
        "pronunciation_uz": "vot du yu rekommend ez ze shefs speshl",
        "uzbek": "Oshpazning maxsus taomi sifatida nimani tavsiya qilasiz?",
        "pos": "phr",
        "example_en": "A: What do you recommend? B: The grilled salmon is outstanding tonight.",
        "example_uz": "A: Nimani tavsiya qilasiz? B: Bugun olovda pishirilgan losos juda ajoyib.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Do you have any vegetarian or vegan options?",
        "ipa": "/duː juː hæv ˈen.i ˌvedʒ.ɪˈteə.ri.ən ɔːr ˈviː.ɡən ˈɒp.ʃənz/",
        "pronunciation_uz": "du yu hev eni vedjiteriyen or viygen opshenz",
        "uzbek": "Sizda vegetarian yoki vegan taomlari bormi?",
        "pos": "phr",
        "example_en": "A: Do you have vegetarian options? B: Yes, we have pasta and fresh salads.",
        "example_uz": "A: Vegetarian taomlar bormi? B: Ha, pasta va yangi salatlarimiz bor.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could we have the bill, please? We would like to pay separately.",
        "ipa": "/kʊd wiː hæv ðə bɪl pliːz wiː wʊd laɪk tuː peɪ ˈsep.ər.ət.li/",
        "pronunciation_uz": "kud viy hev ze bil pliyz viy vud layk tu pey sepretli",
        "uzbek": "Hisobni bersangiz, iltimos? Alohida-alohida toʻlamoqchi edik.",
        "pos": "phr",
        "example_en": "A: Could we have the bill, please? B: Of course, cash or card?",
        "example_uz": "A: Hisobni bersangiz? B: Albatta, naqd pulmi yoki kartami?",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Is service charge included in the total bill?",
        "ipa": "/ɪz ˈsɜː.vɪs tʃɑːdʒ ɪnˈkluː.dɪd ɪn ðə ˈtəʊ.təl bɪl/",
        "pronunciation_uz": "iz servis chardj inkludid in ze toutl bil",
        "uzbek": "Xizmat haqi umumiy hisobga kiritilganmi?",
        "pos": "phr",
        "example_en": "A: Is service charge included? B: Yes, ten percent service is included.",
        "example_uz": "A: Xizmat haqi kiritilganmi? B: Ha, oʻn foiz xizmat haqi qoʻshilgan.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could I get a takeaway box for the leftover food?",
        "ipa": "/kʊd aɪ ɡet ə ˈteɪk.ə.weɪ bɒks fɔːr ðə ˈleftˌəʊ.vər fuːd/",
        "pronunciation_uz": "kud ay get e teyk-evey boks for ze left-over fuwd",
        "uzbek": "Qolgan ovqatni olib ketish uchun quticha bersangiz boʻladimi?",
        "pos": "phr",
        "example_en": "A: Could I get a takeaway box, please? B: Certainly, I will pack it for you.",
        "example_uz": "A: Olib ketish uchun idish bersangiz boʻladimi? B: Albatta, hozir oʻrab beraman.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 3. Hotel
    {
        "english": "I have a reservation under the name of Smith.",
        "ipa": "/aɪ hæv ə ˌrez.əˈveɪ.ʃən ˈʌn.dər ðə neɪm əv smɪθ/",
        "pronunciation_uz": "ay hev e rezervayshen ander ze neym ov smis",
        "uzbek": "Men Smit nomiga xona band qilgan edim.",
        "pos": "phr",
        "example_en": "A: Welcome! B: Hello, I have a reservation under the name of Smith.",
        "example_uz": "A: Xush kelibsiz! B: Salom, men Smit nomiga buyurtma qilgan edim.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "What time is breakfast served in the morning?",
        "ipa": "/wɒt taɪm ɪz ˈbrek.fəst sɜːvd ɪn ðə ˈmɔː.nɪŋ/",
        "pronunciation_uz": "vot taym iz brekfest sorvd in ze morning",
        "uzbek": "Ertalab nonushta soat nechida tortiladi?",
        "pos": "phr",
        "example_en": "A: What time is breakfast served? B: From 7:00 AM to 10:30 AM.",
        "example_uz": "A: Nonushta soat nechida? B: Ertalabki 7:00 dan 10:30 gacha.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could you please arrange a wake-up call for 6:30 AM?",
        "ipa": "/kʊd juː pliːz əˈreɪndʒ ə ˈweɪk.ʌp kɔːl fɔːr sɪks ˈθɜː.ti eɪ em/",
        "pronunciation_uz": "kud yu pliyz ereyndj e veyk-ap kol for siks torti ey em",
        "uzbek": "Ertalab soat 6:30 ga uygʻotish qoʻngʻirogʻi buyurtma qilsam boʻladimi?",
        "pos": "phr",
        "example_en": "A: Could you arrange a wake-up call for 6:30 AM? B: Noted, we will call you.",
        "example_uz": "A: 6:30 ga uygʻotish qoʻngʻirogʻi qoʻya olasizmi? B: Yozib qoʻydik, qoʻngʻiroq qilamiz.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Is it possible to request a late check-out tomorrow?",
        "ipa": "/ɪz ɪt ˈpɒs.ə.bəl tuː rɪˈkwest ə leɪt tʃek aʊt təˈmɒr.əʊ/",
        "pronunciation_uz": "iz it possibl tu rikvest e leyt chek aut tomorrou",
        "uzbek": "Ertaga xonani kechroq boʻshatishni soʻrasa boʻladimi?",
        "pos": "phr",
        "example_en": "A: Is late check-out possible? B: Yes, you can stay until 1:00 PM.",
        "example_uz": "A: Kechroq chiqish mumkinmi? B: Ha, soat 13:00 gacha qolishingiz mumkin.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could I get some clean towels and pillows, please?",
        "ipa": "/kʊd aɪ ɡet sʌm kliːn ˈtaʊ.əlz ænd ˈpɪl.əʊz pliːz/",
        "pronunciation_uz": "kud ay get sam kliyn tauelz end pillouz pliyz",
        "uzbek": "Toza sochiqlar va yostiqlar bersangiz, iltimos?",
        "pos": "phr",
        "example_en": "A: Could I get extra towels? B: Housekeeping will deliver them right away.",
        "example_uz": "A: Qoʻshimcha sochiq olsam boʻladimi? B: Xodimlar darhol keltirib beradi.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 4. Taxi & Directions
    {
        "english": "Could you drop me off near the metro station, please?",
        "ipa": "/kʊd juː drɒp miː ɒf nɪər ðə ˈmet.rəʊ ˈsteɪ.ʃən pliːz/",
        "pronunciation_uz": "kud yu drop miy of nier ze metrou steyshen pliyz",
        "uzbek": "Meni metro bekati yaqinida tushirib qoldira olasizmi, iltimos?",
        "pos": "phr",
        "example_en": "A: Where to, sir? B: Near the central metro station, please.",
        "example_uz": "A: Qayerga borasiz? B: Markaziy metro yaqinida tushirib qoldiring.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "How much will the taxi ride cost to downtown?",
        "ipa": "/haʊ mʌtʃ wɪl ðə ˈtæk.si raɪd kɒst tuː ˌdaʊnˈtaʊn/",
        "pronunciation_uz": "hau mach vil ze teksi rayd kost tu dauntaun",
        "uzbek": "Shahar markazigacha taksi narxi qancha boʻladi?",
        "pos": "phr",
        "example_en": "A: How much to downtown? B: It is around fifteen dollars on the meter.",
        "example_uz": "A: Markazgacha qancha? B: Hisoblagich boʻyicha oʻn besh dollar atrofida.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Turn left at the intersection and continue straight for two blocks.",
        "ipa": "/tɜːn left æt ðiː ˈɪn.tə.sek.ʃən ænd kənˈtɪn.juː streɪt fɔːr tuː blɒks/",
        "pronunciation_uz": "torn left et zi intersekshn end kontinyu streyt for tu bloks",
        "uzbek": "Chorraxadan chapga buriling va ikki chorraha toʻgʻriga yuring.",
        "pos": "phr",
        "example_en": "A: How do I find the museum? B: Turn left at the intersection and go straight.",
        "example_uz": "A: Muzeyni qanday topsam boʻladi? B: Chorrahadan chapga buriling va toʻgʻri boring.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could you please turn on the air conditioner in the car?",
        "ipa": "/kʊd juː pliːz tɜːn ɒn ðiː eər kənˈdɪʃ.ən.ər ɪn ðə kɑːr/",
        "pronunciation_uz": "kud yu pliyz torn on zi eer kondishener in ze kar",
        "uzbek": "Iltimos, mashinadagi konditsionerni yoqib bera olasizmi?",
        "pos": "phr",
        "example_en": "A: It is warm in here. Could you turn on the AC? B: Sure, right away.",
        "example_uz": "A: Ichkarida issiq ekan, konditsionerni yoqa olasizmi? B: Albatta, hozir.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 5. Shopping & Stores
    {
        "english": "Do you happen to have this shirt in a medium size?",
        "ipa": "/duː juː ˈhæp.ən tuː hæv ðɪs ʃɜːt ɪn ə ˈmiː.di.əm saɪz/",
        "pronunciation_uz": "du yu hepen tu hev zis short in e miydiyem sayz",
        "uzbek": "Bu koʻylakning oʻrta (M) oʻlchami bormi sizda?",
        "pos": "phr",
        "example_en": "A: Do you have this shirt in medium? B: Let me check the storeroom.",
        "example_uz": "A: Bu koʻylakning M oʻlchami bormi? B: Omborni tekshirib koʻraman.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Where are the fitting rooms located?",
        "ipa": "/weər ɑːr ðə ˈfɪt.ɪŋ ruːmz ləʊˈkeɪ.tɪd/",
        "pronunciation_uz": "veer ar ze fitting ruwmz loukeytid",
        "uzbek": "Kiyib koʻrish xonalari qayerda joylashgan?",
        "pos": "phr",
        "example_en": "A: Where are the fitting rooms? B: Just behind that display on the left.",
        "example_uz": "A: Kiyib koʻrish xonalari qayerda? B: Chap tarafdagi vitrinaning orqasida.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "What is your refund policy for returned items?",
        "ipa": "/wɒt ɪz jɔːr ˈriː.fʌnd ˈpɒl.ə.si fɔːr rɪˈtɜːnd ˈaɪ.təmz/",
        "pronunciation_uz": "vot iz yor riyfand polisi for ritornd aytemz",
        "uzbek": "Qaytarilgan buyumlar uchun pulni qaytarish tartibingiz qanday?",
        "pos": "phr",
        "example_en": "A: What is your refund policy? B: You can return within fourteen days with receipt.",
        "example_uz": "A: Pulni qaytarish tartibi qanday? B: Chek bilan 14 kun ichida qaytarishingiz mumkin.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Can I pay by contactless credit card or Apple Pay?",
        "ipa": "/kæn aɪ peɪ baɪ ˈkɒn.tækt.ləs ˈkred.ɪt kɑːd ɔːr ˈæp.əl peɪ/",
        "pronunciation_uz": "ken ay pey bay kontaktles kredit kard or eppl pey",
        "uzbek": "Kontaktsiz bank kartasi yoki Apple Pay orqali toʻlasam boʻladimi?",
        "pos": "phr",
        "example_en": "A: Can I pay with Apple Pay? B: Yes, just hold your phone near the screen.",
        "example_uz": "A: Apple Pay bilan toʻlasam boʻladimi? B: Ha, telefoningizni ekranga yaqin tuting.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Is there any special discount on this item today?",
        "ipa": "/ɪz ðeər ˈen.i ˈspeʃ.əl ˈdɪs.kaʊnt ɒn ðɪs ˈaɪ.təm təˈdeɪ/",
        "pronunciation_uz": "iz zeer eni speshl diskaunt on zis aytem todey",
        "uzbek": "Bugun bu tovarga maxsus chegirma bormi?",
        "pos": "phr",
        "example_en": "A: Is there a discount today? B: Yes, take twenty percent off at checkout.",
        "example_uz": "A: Bugun chegirma bormi? B: Ha, kassada yigirma foiz chegirma qilinadi.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 6. Doctor & Health
    {
        "english": "I have been experiencing a persistent headache and sore throat.",
        "ipa": "/aɪ hæv biːn ɪkˈspɪə.ri.əns.ɪŋ ə pəˈsɪs.tənt ˈhed.eɪk ænd sɔːr θrəʊt/",
        "pronunciation_uz": "ay hev biyn ekspiriensing e persistent hedeyk end sor frout",
        "uzbek": "Bir necha kundan beri boshim tinimsiz ogʻrib, tomogʻim qaqshamoqda.",
        "pos": "phr",
        "example_en": "A: What hurts? B: I have been experiencing a persistent headache and sore throat.",
        "example_uz": "A: Qayeringiz ogʻriyapti? B: Boshim tinimsiz ogʻrib, tomogʻim qaqshamoqda.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "How many times a day should I take this medication?",
        "ipa": "/haʊ ˈmen.i taɪmz ə deɪ ʃʊd aɪ teɪk ðɪs ˌmed.ɪˈkeɪ.ʃən/",
        "pronunciation_uz": "hau meni taymz e dey shud ay teyk zis medikeyshen",
        "uzbek": "Bu dorini kuniga necha mahal ichishim kerak?",
        "pos": "phr",
        "example_en": "A: How should I take this? B: Take one tablet twice daily after meals.",
        "example_uz": "A: Qanday ichishim kerak? B: Ovqatdan keyin kuniga ikki marta bir donadan.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Do these allergy pills cause drowsiness or dizziness?",
        "ipa": "/duː ðiːz ˈæl.ə.dʒi pɪlz kɔːz ˈdraʊ.zi.nəs ɔːr ˈdɪz.i.nəs/",
        "pronunciation_uz": "du ziyz allergic pilz koz drauzines or dizines",
        "uzbek": "Bu allergiya tabletkalari uyquchanlik yoki bosh aylanishiga olib keladimi?",
        "pos": "phr",
        "example_en": "A: Do these cause drowsiness? B: No, this is non-drowsy medication.",
        "example_uz": "A: Bu uyqu keltiradi-mi? B: Yoʻq, bu uyqu keltirmaydigan dori.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "I am severely allergic to penicillin and aspirin.",
        "ipa": "/aɪ æm sɪˈvɪə.li əˈlɜː.dʒɪk tuː ˌpen.ɪˈsɪl.ɪn ænd ˈæs.prɪn/",
        "pronunciation_uz": "ay em siverli ellordjik tu penitsillin end aspirin",
        "uzbek": "Menda penitsillin va aspirindan qattiq allergiya bor.",
        "pos": "phr",
        "example_en": "A: Any allergies? B: Yes, I am severely allergic to penicillin.",
        "example_uz": "A: Allergiyangiz bormi? B: Ha, penitsillinga kuchli allergiyam bor.",
        "category": "Hayotiy muloqot va dialoglar"
    },

    # 7. Work & Career
    {
        "english": "Let's schedule a brief follow-up meeting for tomorrow morning.",
        "ipa": "/lets ˈskedʒ.uːl ə briːf ˈfɒl.əʊ.ʌp ˈmiː.tɪŋ fɔːr təˈmɒr.əʊ ˈmɔː.nɪŋ/",
        "pronunciation_uz": "lets skedjul e briyf folou-ap miyting for tomorrou morning",
        "uzbek": "Keling, ertaga ertalabga qisqa oraliq uchrashuv belgilaymiz.",
        "pos": "phr",
        "example_en": "A: Let's schedule a brief meeting tomorrow. B: Sounds great, 10:00 AM works.",
        "example_uz": "A: Keling, ertaga qisqa yigʻilish qilamiz. B: Ajoyib, soat 10:00 maʼqul.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could you please send me the updated quarterly report by email?",
        "ipa": "/kʊd juː pliːz send miː ðiː ʌpˈdeɪ.tɪd ˈkwɔː.təl.i rɪˈpɔːt baɪ ˈiː.meɪl/",
        "pronunciation_uz": "kud yu pliyz send miy zi apdeytid kvorteli riport bay iymeyl",
        "uzbek": "Choraklik yangilangan hisobotni elektron pochta orqali yubora olasizmi?",
        "pos": "phr",
        "example_en": "A: Could you send the report? B: Sure, attached to the email.",
        "example_uz": "A: Hisobotni yuborasizmi? B: Albatta, xatga biriktirib qoʻydim.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "I truly appreciate your prompt assistance with this urgent task.",
        "ipa": "/aɪ ˈtruː.li əˈpriː.ʃi.eɪt jɔːr prɒmpt əˈsɪs.təns wɪð ðɪs ˈɜː.dʒənt tɑːsk/",
        "pronunciation_uz": "ay truli eprisheyt yor prompt esistens viz zis ordjent task",
        "uzbek": "Ushbu shoshilinch vazifada tezkor yordamingiz uchun chin dildan minnatdorman.",
        "pos": "phr",
        "example_en": "A: Thanks for the help! B: You are very welcome, happy to help.",
        "example_uz": "A: Yordam uchun rahmat! B: Arzimaydi, yordam berganimdan xursandman.",
        "category": "Hayotiy muloqot va dialoglar"
    },
    {
        "english": "Could you please clarify what the deadline for this project is?",
        "ipa": "/kʊd juː pliːz ˈklær.ɪ.faɪ wɒt ðə ˈded.laɪn fɔːr ðɪs ˈprɒdʒ.ekt ɪz/",
        "pronunciation_uz": "kud yu pliyz klerifay vot ze dedlayn for zis prodjekt iz",
        "uzbek": "Ushbu loyihaning oxirgi topshirish muddati qachon ekanligiga aniqlik kirita olasizmi?",
        "pos": "phr",
        "example_en": "A: What is the deadline? B: Next Friday by 5:00 PM.",
        "example_uz": "A: Muddati qachon? B: Kelasi juma soat 17:00 gacha.",
        "category": "Hayotiy muloqot va dialoglar"
    }
]

def main():
    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "title": "Hayotiy muloqot va dialoglar (Situational English)",
        "category": "Jonli muloqot va dialoglar",
        "group": "topic",
        "badge": "36",
        "words": DIALOGUES,
    }
    out_file = DECKS_DIR / "topic-36-situational-dialogues.json"
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {out_file.name}: {len(DIALOGUES)} cards")

if __name__ == "__main__":
    main()
