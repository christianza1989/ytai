# Autonominis Muzikantas (Autonomous Musician)

Sistema, kuri savarankiškai kuria muziką naudodama Suno API ir Gemini AI, ir gali ją publikuoti į YouTube.

## 🚀 Greita Pradžia

### 1. Įdiekite Priklausomybes
```bash
pip install -r requirements.txt
```

### 2. Nustatykite API Raktus
Kopijuokite `.env.example` į `.env` ir įveskite tikrus API raktus:

```bash
cp .env.example .env
```

Redaguokite `.env` failą:
```env
SUNO_API_KEY=your_actual_suno_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 3. Paleiskite Sistemą
```bash
python main.py
```

## 📁 Projekto Struktūra

```
autonominis-muzikantas/
├── main.py                 # Pagrindinis vykdymo failas
├── core/
│   ├── services/
│   │   ├── suno_client.py      # Suno API klientas
│   │   └── gemini_client.py    # Gemini AI klientas
│   ├── utils/              # Pagalbinės funkcijos
│   └── models/             # Duomenų modeliai
├── output/                 # Sugeneruota muzika ir failai
├── temp/                   # Laikini failai
├── .env                    # Aplinkos kintamieji
├── .env.example           # API raktų pavyzdys
├── requirements.txt       # Python priklausomybės
└── README.md              # Šis failas
```

## 🔧 API Konfiguracija

### Suno API
- Gauti API raktą: [Suno API](https://api.sunoapi.org)
- Reikalingas mokamas planas muzikos generavimui

### Google Gemini API
- Gauti API raktą: [Google AI Studio](https://makersuite.google.com/app/apikey)
- Numatytasis modelis: `gemini-1.5-flash` (galima keisti per `GEMINI_MODEL` kintamąjį)
- Palaikomi modeliai: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-1.0-pro`

## 🎵 Funkcionalumas

### Dabartinė Versija (Phase 0)
- ✅ Suno API integracija
- ✅ Gemini AI kūrybinių idėjų generavimas
- ✅ Bazinė muzikos generavimo funkcija
- ✅ Error handling ir fallback'ai
- ✅ Kreditų tikrinimas

### Planuojama (Phase 1-4)
- 📋 YouTube API integracija
- 📋 Automatizuotas video kūrimas
- 📋 Analitikos ir mokymosi sistema
- 📋 Kelių kanalų palaikymas

## 🛠️ Išplėstinis Naudojimas

### Programinis Sąsajos Naudojimas

```python
from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient

# Inicijuoti klientus
suno = SunoClient()
gemini = GeminiClient()

# Sugeneruoti kūrybinę idėją
brief = gemini.generate_creative_brief("Lo-Fi Hip Hop", "rainy night in Tokyo")

# Sugeneruoti muziką
task_id = suno.generate_music_simple(brief['lyrics_prompt'])

# Patikrinti statusą
status = suno.get_task_status(task_id)
```

## 📊 API Limitai ir Kaina

### Suno API
- **Limitas:** 20 užklausų per 10 sekundžių
- **Failų saugojimas:** 15 dienų
- **Modeliai:** V3_5, V4, V4_5 (skirtingos kainos)

### Gemini API
- **Limitas:** Priklauso nuo plano
- **Kaina:** Nemokama iki tam tikro limito

## 🔒 Saugumas

- API raktai saugomi `.env` faile (neįkelkite į Git)
- Nenaudokite demonstracinių raktų gamyboje
- Reguliariai keiskite API raktus

## 📈 Plėtros Planas

### Phase 1: MVP (2-3 savaitės)
- Bazinė muzikos generavimo funkcija
- Lokalus failų saugojimas
- Kūrybinių idėjų generavimas

### Phase 2: YouTube Integracija (2 savaitės)
- Video kūrimo automatizavimas
- YouTube įkėlimo funkcija
- Metaduomenų optimizavimas

### Phase 3: Autonomijos Ciklas (3-4 savaitės)
- Analitikos sistema
- Mokymosi algoritmai
- Grįžtamojo ryšio ciklas

### Phase 4: Mastelio Didinimas (Nuolatinis)
- Kelių kanalų valdymas
- Išplėstinė analitika
- A/B testavimas

## 🤝 Prisidėjimas

1. Fork'inti projektą
2. Sukurti feature branch'ą
3. Commit'inti pakeitimus
4. Push'inti į branch'ą
5. Sukurti Pull Request

## 📄 Licencija

Šis projektas yra atviro kodo ir platinamas pagal MIT licenciją.

## 📞 Palaikymas

Jei turite klausimų ar problemų:
1. Patikrinkite `.env` konfigūraciją
2. Įsitikinkite, kad API raktai galioja
3. Patikrinkite interneto ryšį
4. Peržiūrėkite log'us terminale

---

**Pastaba:** Ši sistema reikalauja mokamų API paslaugų. Prieš pradėdami įsitikinkite, kad turite reikiamus API raktus ir kreditus.
