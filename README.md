# AI Crop Disease Detection Web App

A beginner-friendly web app that detects crop diseases from leaf images using a **pretrained MobileNetV2 model** trained on the PlantVillage dataset. It also includes a **local AI assistant** (Ollama) and a **weather panel** to guide planting decisions.

## Features
- Image upload + preview
- AI disease prediction + confidence score
- Treatment recommendation
- Clean UI dashboard
- Simple REST API
- Local AI assistant (no API limits)
- Weather details + planting guidance

## Project Structure
```
crop-disease-ai/
+-- backend/
¦   +-- app.py
¦   +-- assistant.py
¦   +-- model_loader.py
¦   +-- predictor.py
¦   +-- weather.py
+-- frontend/
¦   +-- index.html
¦   +-- style.css
¦   +-- script.js
+-- model/
¦   +-- plant_disease_model.h5
+-- utils/
¦   +-- treatments.py
+-- requirements.txt
+-- README.md
```

## Setup Instructions

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Add the pretrained model
Download a **MobileNetV2 PlantVillage .h5 model** and place it here:
```
model/plant_disease_model.h5
```

> Note: The class label order must match your model’s training order. If predictions look incorrect, update `CLASS_LABELS` in `backend/predictor.py`.

### 3) Install Ollama (Local LLM)
1. Install Ollama from the official website.
2. Pull a model (recommended):
```bash
ollama pull llama3.1
```
3. Start the Ollama server:
```bash
ollama serve
```

You can change the model by setting an environment variable:
```bash
set OLLAMA_MODEL=mistral
```

### 4) Add OpenWeatherMap API key
Create a free API key at OpenWeatherMap and set it in your environment:
```bash
set OPENWEATHER_API_KEY=your_api_key_here
```

### 5) Run the backend
```bash
python backend/app.py
```
The API will run at `http://127.0.0.1:5000`.

### 6) Run the frontend
From the `frontend/` folder:
```bash
python -m http.server 5500
```
Then open `http://127.0.0.1:5500` in your browser.

## API Usage
**POST** `/predict`
- Form-data key: `file`
- Response example:
```json
{
  "disease": "Tomato Early blight",
  "confidence": 0.92,
  "treatment": "Remove infected leaves, improve airflow, and apply a copper-based fungicide."
}
```

**POST** `/assistant`
- JSON body: `{ "question": "How do I treat tomato late blight?" }`
- Response example:
```json
{
  "answer": "...",
  "source": "ollama",
  "model": "llama3.1"
}
```

**POST** `/weather`
- JSON body (city): `{ "city": "Pune, IN" }`
- JSON body (geo): `{ "lat": 18.5204, "lon": 73.8567 }`
- Response example:
```json
{
  "location": "Pune, IN",
  "temperature_c": 29.4,
  "humidity_pct": 62,
  "pressure_hpa": 1008,
  "wind_mps": 3.1,
  "cloud_pct": 40,
  "condition": "scattered clouds",
  "rain_next_24h_mm": 2.4,
  "planting_guidance": "Conditions look generally suitable for planting. Use crop-specific guidance for best results."
}
```

## Preprocessing
The model expects **224x224** images with normalization to `[0, 1]`.
If your model expects `mobilenet_v2.preprocess_input`, modify `preprocess_image()` in `backend/predictor.py` accordingly.

## Troubleshooting
- If you see `Model file looks too small`, replace the placeholder file with the real `.h5` model.
- For CORS errors, ensure the backend is running and reachable at `http://127.0.0.1:5000`.
- If the assistant fails, confirm Ollama is running and the model is pulled.
- If weather fails, verify your OpenWeatherMap API key is set.

## License
Use this project freely for learning and demos.
## Weather Setup Notes
- `OPENWEATHER_API_KEY` is read at runtime. If you set it after the server starts, restart the backend.
- In PowerShell, `set OPENWEATHER_API_KEY=...` only affects the current session.
## Environment Setup (Recommended)
Create a `.env` file in the project root (same folder as `README.md`) and add your keys:
```
OPENWEATHER_API_KEY=your_api_key_here
OLLAMA_MODEL=llama3.1
```
Then restart the backend.
## Label Mapping Note
If the `PlantVillage` dataset folder exists in the project root, the app will auto-load class labels in the same alphabetical order used by `flow_from_directory`. This keeps predictions aligned with your trained model.
## Custom Model Labels
If your model was trained on a subset of classes (e.g., 3 classes), create or edit:
`model/labels.txt`

Add **one class per line** in the exact order used during training. Example:
```
Tomato___Early_blight
Tomato___Late_blight
Tomato___healthy
```
The app will prioritize `labels.txt` over dataset folders.
## UI Upgrade (ChatGPT-style)
- Chat history on the left
- Center chat area with bottom input
- Upload button next to the input
- Crop health dashboard cards
- Weather control bar

## Translation Setup (AI Replies)
This project uses a LibreTranslate-compatible API to translate AI responses.
Set these in `.env`:
```
TRANSLATE_URL=http://localhost:5001/translate
TRANSLATE_API_KEY=
```
If translation is not available, AI replies remain in English.
## Local Translation (LibreTranslate)
To run translation locally without any API key:

1. Install Docker Desktop.
2. Start LibreTranslate:
```bash
docker compose up -d libretranslate
```
3. Confirm it is running at `http://localhost:5001`.

The app is already configured to call:
```
TRANSLATE_URL=http://localhost:5001/translate
```

If you don’t want translation, you can skip this and AI replies will stay in English.
## Local Translation (IndicTrans2 - Recommended)
This project uses **IndicTrans2** for Kannada, Hindi, Telugu, Tamil translations.

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Recommended for CPU) Install PyTorch CPU build if needed:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

3. Set these in `.env` (optional overrides):
```
INDIC_MODEL_EN_INDIC=ai4bharat/indictrans2-en-indic-1B
INDIC_MODEL_INDIC_EN=ai4bharat/indictrans2-indic-en-1B
INDIC_DEVICE=cpu
```

On first run, the models will download (large files). After that, translation runs locally.

## Legacy (LibreTranslate)
LibreTranslate does **not** support kn/ta/te in the default container. We no longer rely on it.
## IndicTrans2 Access (Required)
The IndicTrans2 models are **gated** on Hugging Face.

Steps:
1. Request access on the model pages:
   - ai4bharat/indictrans2-en-indic-1B
   - ai4bharat/indictrans2-indic-en-1B
2. Create a Hugging Face token (read access).
3. Add it to your `.env`:
```
HF_TOKEN=your_huggingface_token_here
```
4. Restart the backend.

Once access is granted, translations will work locally.
## Local Translation (No Token)
We now use an open NLLB model for English â†” Kannada translation (no token required).

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Recommended for CPU) Install PyTorch CPU build if needed:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

3. Optional: override model in `.env`:
```
NLLB_MODEL=facebook/nllb-200-distilled-600M
INDIC_DEVICE=cpu
```

On first use, the model will download.
## Android App (WebView)
A simple Android wrapper that loads the web app from your PC on the same Wi-Fi.

### 1) Start backend (PC)
```bash
python backend/app.py
```

### 2) Start frontend (PC)
```bash
cd frontend
python -m http.server 5500
```

### 3) Find your PC IP
```bash
ipconfig
```
Look for a local IP like `192.168.x.x`.

### 4) Update the Android app URL
Edit:
`android-app/app/src/main/java/com/crophealth/webview/MainActivity.java`

Replace:
```
private static final String BASE_URL = "http://192.168.1.100:5500";
```
with your actual PC IP.

### 5) Build Android app
Open `android-app/` in Android Studio and run on your device.

**Note:** Phone and PC must be on the same Wi-Fi.
