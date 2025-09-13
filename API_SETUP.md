# 🔑 API Raktų Konfigūravimo Instrukcijos

Šis dokumentas padės jums sukonfigūruoti API raktus, reikalingus **Autonominio Muzikanto** sistemos veikimui.

## 📋 Reikalingi API Raktai

### 1. 🎵 Suno API (Muzikos Generavimas)
- **Paskirtis:** Automatinis muzikos generavimas
- **Būtinas:** Taip, jei norite generuoti tikrą muziką
- **Svetainė:** [api.sunoapi.org](https://api.sunoapi.org)

#### Kaip gauti Suno API raktą:
1. Eikite į https://api.sunoapi.org
2. Susikurkite paskyrą
3. Pasirinkite mokamą planą (muzikos generavimas kainuoja kreditus)
4. Nukopijuokite API raktą iš dashboard

#### Kainos (orientacinės):
- **V3_5 modelis:** ~2 kreditai už dainą
- **V4 modelis:** ~5 kreditų už dainą  
- **Kreditų paketas:** Nuo $10 už 500 kreditų

---

### 2. 🧠 Google Gemini AI (Kūrybinės Idėjos)
- **Paskirtis:** Kūrybinių idėjų ir tekstų generavimas
- **Būtinas:** Taip, jei norite AI generuojamus tekstus
- **Svetainė:** [Google AI Studio](https://makersuite.google.com/app/apikey)

#### Kaip gauti Gemini API raktą:
1. Eikite į https://makersuite.google.com/app/apikey
2. Prisijunkite su Google paskyra
3. Sukurkite naują API raktą
4. Nukopijuokite raktą

#### Modeliai:
- **gemini-1.5-flash:** Greitas, pigus (rekomenduojamas)
- **gemini-1.5-pro:** Aukštos kokybės, brangesnis
- **gemini-1.0-pro:** Senesnis, bet stabilus

#### Kainos:
- **Nemokama kvota:** Iki tam tikro limito per mėnesį
- **Mokama:** Nuo $0.001 už 1K simbolius

---

### 3. 🎨 Stability AI (Viršelių Generavimas)
- **Paskirtis:** Albumo viršelių generavimas
- **Būtinas:** Ne (galite praleisti)
- **Svetainė:** [Stability AI](https://platform.stability.ai)

#### Kaip gauti Stability AI raktą:
1. Eikite į https://platform.stability.ai
2. Susikurkite paskyrą
3. Įdėkite kreditų (minimum $10)
4. Nukopijuokite API raktą iš settings

#### Kainos:
- **SDXL 1.0:** ~$0.04 už paveikslėlį
- **SD3 Medium:** ~$0.035 už paveikslėlį

---

### 4. 🎥 YouTube API (Publikavimas)
- **Paskirtis:** Automatinis video įkėlimas į YouTube
- **Būtinas:** Ne (galite praleisti pradžiai)
- **Svetainė:** [Google Cloud Console](https://console.cloud.google.com)

#### Konfigūravimas sudėtingesnis:
1. Sukurkite Google Cloud projektą
2. Įjunkite YouTube Data API v3
3. Sukurkite OAuth 2.0 kredencialus
4. Atsisiųskite `client_secrets.json` failą

*Detalesnės instrukcijos YouTube API yra atskirame skyriuje.*

---

## ⚙️ Konfigūravimo Žingsniai

### 1. Redaguokite .env Failą

Atidarykite `.env` failą projekto šaknyje ir įrašykite savo API raktus:

```env
# Suno API Configuration
SUNO_API_KEY=jūsų_tikras_suno_api_raktas_čia

# Google Gemini API Configuration  
GEMINI_API_KEY=jūsų_tikras_gemini_api_raktas_čia
GEMINI_MODEL=gemini-1.5-flash

# Stability AI Configuration (neprivaloma)
STABLE_DIFFUSION_API_KEY=jūsų_tikras_stability_api_raktas_čia
STABLE_DIFFUSION_URL=https://api.stability.ai

# YouTube API Configuration (neprivaloma)
YOUTUBE_CHANNEL_ID=jūsų_youtube_kanalo_id
YOUTUBE_CLIENT_SECRETS_PATH=configs/client_secrets.json

# Application Settings
LOG_LEVEL=INFO
OUTPUT_DIR=output/
TEMP_DIR=temp/
DATABASE_URL=sqlite:///database.db
```

### 2. Patikrinkite Konfigūraciją

Paleiskite sistemą ir patikrinkite ar API raktai veikia:

**Terminalas:**
```bash
python main.py
# Pasirinkite "2" realiam režimui
```

**Web Sąsaja:**
```bash
# Atidarykite naršyklėje
https://jūsų-serverio-url/
# Pagrindiniame puslapyje matysite API būseną
```

---

## 🧪 Testavimo Režimas

**Nėra API raktų?** Nėra problemos! Galite naudoti testavimo režimą:

- ✅ Testuoja visą proceso logiką
- ✅ Naudoja mock duomenis
- ✅ Nereiaklauja API raktų
- ✅ Nekainuoja pinigų

**Kaip paleisti:**
1. Web sąsajoje pasirinkite "🧪 Testavimo režimas"
2. Arba terminale pasirinkite "1"

---

## 💰 Kaštų Optimizavimas

### Suno API:
- Pradėkite su V3_5 modeliu (pigesnis)
- Naudokite trumpesnius prompt'us
- Testuokite su mock duomenimis prieš realų generavimą

### Gemini API:  
- Naudokite gemini-1.5-flash (greičiausias ir pigiausias)
- Optimizuokite prompt'us - trumpi ir aiškūs

### Stability AI:
- Generuokite tik po sėkmingo muzikos generavimo
- Naudokite 1024x1024 rezoliuciją (optimalu)
- Testuokite su nemokamomis alternatyvomis pradžiai

---

## 🔒 Saugumas

### ⚠️ SVARBŪS PATARIMAI:

1. **Niekada neverskite .env failo į Git:**
   - `.env` failas jau įtrauktas į `.gitignore`
   - Patikrinkite prieš commit'inant

2. **API raktų saugojimas:**
   - Laikykite juos slapčiuose
   - Nešiuokite po grupes/pokalbius
   - Keiskite juos reguliariai

3. **Kreditų kontrolė:**
   - Stebėkite savo API naudojimą
   - Nustatykite limitus API platformose
   - Pradėkite su mažais kreditų kiekiais

4. **Testavimas:**
   - Visada testuokite su mock duomenimis
   - Patikrinkite išlaidas prieš didelius generavimus
   - Naudokite staging aplinkas

---

## ❓ Dažnai Užduodami Klausimai

### Q: Ar galiu naudoti sistemą be visų API raktų?
**A:** Taip! Testavimo režimas veikia be jokių API raktų.

### Q: Kiek kainuoja sugeneruoti vieną dainą?
**A:** ~$0.40-1.00 priklausomai nuo modelių ir nustatymų.

### Q: Ar API raktai baigiasi?
**A:** Suno ir Stability - naudoja kreditus. Gemini - turi mėnesinį limitą.

### Q: Ką daryti jei API neveikia?
**A:** 
1. Patikrinkite API raktų galiojimą
2. Patikrinkite kreditų likutį  
3. Patikrinkite interneto ryšį
4. Žiūrėkite log'us sistemoje

### Q: Ar galiu naudoti kitus panašius API?
**A:** Šiuo metu sistema sukonfigūruota konkretiems API, bet galite modifikuoti kodą.

---

## 🛠️ Trikčių Sprendimas

### Dažnos Problemos:

#### "API key not valid"
- Patikrinkite ar nukopijuote pilną raktą
- Patikrinkite ar nėra extra tarpų
- Patikrinkite ar raktas negalioja

#### "Insufficient credits"  
- Papildykite kreditų balansą
- Arba naudokite testavimo režimą

#### "Rate limit exceeded"
- Palaukite 1-2 minutes  
- Sumažinkite generavimo dažnį

#### "Failed to connect to API"
- Patikrinkite interneto ryšį
- Patikrinkite ar API servisas veikia
- Pabandykite vėliau

---

## 📞 Pagalba

**Jei kilo problemų:**

1. **Pirmiausia:** Patikrinkite šį dokumentą
2. **Log'ai:** Žiūrėkite sistemos log'us
3. **Testavimas:** Bandykite testavimo režimą
4. **Dokumentacija:** Skaitykite API dokumentacijas:
   - [Suno API Docs](https://api.sunoapi.org/docs)
   - [Gemini API Docs](https://ai.google.dev/docs)
   - [Stability AI Docs](https://platform.stability.ai/docs)

**Kontaktai:**
- GitHub Issues: [projekto repozitorijoje]
- Email: [jūsų palaikymo email]

---

## 🎉 Sėkmės!

Sėkmingai sukonfigūravę API raktus galėsite:

- 🎵 Generuoti originali muziką
- 🧠 Kurti AI tekstus ir idėjas  
- 🎨 Generuoti albumo viršelius
- 📊 Stebėti proceso analitiką
- 🎬 Kurti video failus (su MoviePy)

**Pradėkite su testavimo režimu, o vėliau pereikite prie realių API!**