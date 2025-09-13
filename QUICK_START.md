# 🚀 Greitas Paleidimas - Autonominis Muzikantas

## 1️⃣ Staigus Pradėjimas (30 sekundžių)

```bash
# 1. Įdiekite priklausomybes
pip install -r requirements.txt

# 2. Paleiskite testavimo režimą
python main.py
# Pasirinkite "1" - Testavimo režimas

# 🌐 ARBA paleiskite PAGRINDINĮ web interface
python web_launch.py
# 🔐 Atidarykite: http://localhost:8000 (Slaptažodis: admin123)
```

**✅ Veiks iš karto! Nereikia API raktų testavimui.**

---

## 2️⃣ 🌐 PAGRINDINIS Web Interface (Rekomenduojama)

### 🚀 Admin Panel paleidimas:

```bash
# Paleiskite PAGRINDINĮ admin interface
python web_launch.py

# 🔐 Prisijunkite: http://localhost:8000
# Slaptažodis: admin123
```

### 🏰 Pilnas funkcionalumas:
- **✅ API Configuration** - suveskite API raktus
- **✅ Music Generation** - real-time generavimas  
- **✅ 10-Channel Empire** - kelių kanalų valdymas
- **✅ Analytics & Monitoring** - išsami analitika
- **✅ Voice Cloning** - balso klonavimo sistema
- **✅ Trending Hijacker** - viral content sistema

### 🌐 Prieinamumas:
- **🎯 PAGRINDINIS:** http://localhost:8000 (Port 8000)
- **Alternatyvus:** http://localhost:5000 (Basic interface)

---

## 3️⃣ Kas Yra Dėžėje

### 📁 Struktūra:
```
autonominis-muzikantas/
├── 🎵 main.py              # Terminalas
├── 🌐 web_app.py           # Web sąsaja  
├── 📋 templates/           # HTML šablonai
├── 🔧 core/               # Pagrindinis kodas
│   ├── services/          # API klientai
│   ├── utils/             # Įrankiai  
│   └── analytics/         # Analitika
├── 📂 output/             # Rezultatai
├── 🧪 mock_audio/         # Test failai
└── 📖 docs/               # Dokumentacija
```

### 🎛️ Funkcijos:
- ✅ **Muzikos generavimas** (Suno API)
- ✅ **AI tekstai** (Gemini)  
- ✅ **Viršelių kūrimas** (Stability AI)
- ✅ **Video generavimas** (MoviePy)
- ✅ **YouTube integracija** (YouTube API)
- ✅ **Web sąsaja** (Flask)
- ✅ **Analitika** ir ataskaitos

---

## 4️⃣ Veikimo Režimai

### 🧪 Testavimo Režimas:
- **Nereikia API raktų**
- **Naudoja mock duomenis**  
- **Testuoja visą logiką**
- **Nekainuoja pinigų**

### 🔑 Realus Režimas:
- **Reikia API raktų** (žr. `API_SETUP.md`)
- **Generuoja tikrą muziką**
- **Naudoja kreditus**
- **Pilnas funkcionalumas**

### 🔄 Hibridinis Režimas:
- **Realūs AI tekstai + Mock garsas**
- **Optimalus testavimui su tekstais**

---

## 5️⃣ Greitas Testavimas

### Terminalo Komandos:

```bash
# Testavimo režimas
echo "1" | python main.py

# Realus režimas (su API)
echo "2" | python main.py  

# YouTube testavimas
echo "4" | python main.py
```

### Web Sąsajos Testavimas:

1. Atidarykite http://localhost:5000
2. Pasirinkite "Testavimo režimas"
3. Įveskite žanrą ir temą
4. Spauskite "Pradėti Generavimą"
5. Stebėkite progresą `/status` puslapyje
6. Rezultatai bus `/outputs` puslapyje

---

## 6️⃣ Tipiniai Rezultatai

### Po Sėkmingo Generavimo:

```
📂 output/Lo_Fi_Hip_Hop_Track_20250913_123456/
├── 🎵 track_1.mp3          # Audio failas 1
├── 🎵 track_2.mp3          # Audio failas 2  
├── 🖼️ cover_art.jpg        # Albumo viršelis
├── 🎬 track_1_video.mp4    # Video su audio + viršeliu
├── 📄 metadata.json       # Proyecto informacija
└── 📊 performance_report.txt # Techninė ataskaita
```

### Metadata.json Pavyzdys:
```json
{
  "title": "Midnight Rain Sessions",
  "genre": "Lo-Fi Hip Hop", 
  "theme": "rainy night in Tokyo",
  "mode": "mock",
  "created_at": "2025-09-13T12:34:56",
  "tracks_created": 2,
  "cover_created": true
}
```

---

## 7️⃣ Trikčių Sprendimas

### Dažnos Problemos:

#### ❌ "ModuleNotFoundError: No module named 'moviepy.editor'"
```bash
pip uninstall moviepy -y
pip install moviepy==1.0.3
```

#### ❌ Web sąsaja neprisijungia:
```bash
# Patikrinkite ar serveris veikia
supervisorctl -c supervisord.conf status

# Restart
supervisorctl -c supervisord.conf restart webserver
```

#### ❌ "API key not configured":
- Testavimo režimui: Pasirinkite "Mock" režimą
- Realiam: Žr. `API_SETUP.md` instrukciją

#### ❌ Nėra audio failų:
```bash  
# Patikrinkite ar egzistuoja mock failai
ls mock_audio/
# Turėtų būti: sample_track_1.mp3, sample_track_2.mp3
```

### Log'ų Peržiūra:

```bash
# Supervisord logai
tail -f logs/webserver.log

# Terminalo logai  
python main.py 2>&1 | tee logs/manual.log
```

---

## 8️⃣ Konfigūravimas Gamybai

### Aplinkos Kintamieji (.env):
```env
# MINIMALŪS (testavimui)
LOG_LEVEL=INFO
OUTPUT_DIR=output/
TEMP_DIR=temp/

# PILNI (gamybai - žr. API_SETUP.md)
SUNO_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here  
STABLE_DIFFUSION_API_KEY=your_key_here
```

### Saugumo Patarimai:
- 🔒 Niekada nedalinkitės API raktų
- 🚫 Nepridėkite .env failo į Git  
- 💰 Stebėkite API kreditų naudojimą
- 🧪 Testuokite su mock duomenimis

---

## 9️⃣ Kita Dokumentacija

- 📖 **README.md** - Detalus aprašymas
- 🔑 **API_SETUP.md** - API raktų konfigūravimas  
- 📊 **FEATURES.md** - Funkcionalumo aprašymas
- 🎥 **YOUTUBE_SETUP.md** - YouTube integracija

---

## 🎯 Greitie Patarimai

### Pradedantiesiems:
1. **Pradėkite su testavimo režimu**
2. **Naudokite web sąsają**  
3. **Išbandykite visus režimus**
4. **Skaitykite log'us**

### Pažengusiems:
1. **Sukonfigūruokite API raktus**
2. **Optimizuokite prompt'us**
3. **Naudokite analitiką**  
4. **Kurkite custom workflow'us**

### Kūrėjams:
1. **Modifikuokite core/ modulius**
2. **Pridėkite naujus API**
3. **Kurkite plugins**
4. **Prisidėkite prie projekto**

---

## ✅ Checklist Sėkmingam Paleidimui

- [ ] Python 3.8+ įdiegtas
- [ ] Priklausomybės įdiegtos (`pip install -r requirements.txt`)
- [ ] Mock audio failai sukurti (`mock_audio/sample_track_*.mp3`)
- [ ] Aplankai sukurti (`output/`, `temp/`, `configs/`)
- [ ] Testavimo režimas paleistas ir veikia
- [ ] Web sąsaja pasiekiama (http://localhost:5000)  
- [ ] Rezultatai generuojami į `output/` aplankę
- [ ] API raktai sukonfigūruoti (jei naudojate realų režimą)

**🎉 Sveikiname! Jūsų Autonominis Muzikantas paruoštas kurti muziką!**

---

**📞 Reikia pagalbos?** Žiūrėkite detalesnę dokumentaciją arba kurkite GitHub issue.