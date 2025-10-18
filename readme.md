# Vidscribe

Vidscribe is a web-based tool that utilizes OpenAI's Whisper model to transcribe videos and generate subtitles. Users can upload a video, select a model size and language, and download both transcripts and subtitle files in SRT format.

---

## Features

- Transcribe video audio into text.
- Generate subtitle files (SRT) with timestamps.
- Supports multiple languages (ISO codes).
- Selectable Whisper model sizes: tiny, base, small, medium, large.
- Simple and minimal web interface built with Gradio.
- Automatic audio extraction using ffmpeg.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/auwardak/vidscribe.git
cd vidscribe
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv .venv
# Activate the environment:
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install torch
pip install git+https://github.com/openai/whisper.git
pip install gradio
```

4. **Install ffmpeg**

- Ensure `ffmpeg` is installed and available in your system's PATH.
- You can download it from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).

---

## Usage

Yes, your README should be **slightly updated** to reflect the latest implementation details. Here’s what should change or be clarified:

---

### **1️⃣ Output file locations**

- Mention that **transcripts (`.txt`) are saved in a `logs/` folder**.
- Mention that **subtitles (`.srt`) are saved alongside the video file**.
- This helps users know where to find their outputs.

---

### **2️⃣ Dependencies / installation**

- Make sure `torchvision` is **removed** from instructions.
- Keep instructions for installing `ffmpeg`, as it’s now mandatory for audio extraction.

---

### **3️⃣ UI notes**

- Clarify that Gradio **default theme** is used.
- Video upload box height and layout scaling for columns.
- Model size and language selection are available in the UI.

---

### **4️⃣ Minor suggestions**

- Note that **GPU is used automatically if available**, otherwise CPU is used.
- Warn that **Whisper model weights will download the first time**, and large models can be >1GB.

---

### ✅ **Updated usage section snippet**

1. Run the Gradio app:

```bash
python app.py
```

2. Open the local URL provided in the console (usually [http://127.0.0.1:7860](http://127.0.0.1:7860)).

3. Steps in the UI:

- Upload a video (MP4, MKV, etc.)
- Enter the language ISO code (e.g., `en` for English, `ur` for Urdu)
- Choose a Whisper model size (tiny, base, small, medium, large)
- Click **Transcribe**
- Download the generated transcript (.txt) from the `logs/` folder and subtitles (.srt) from the same folder as the video.

## Notes

- The first time you select a model, Whisper will download the pre-trained weights. Large models can be over 1 GB.
- Smaller models are faster and use less memory but may be less accurate.
- Audio extraction uses ffmpeg to convert video to a 16kHz mono WAV file for faster transcription.
- GPU support is enabled automatically if available (requires CUDA and compatible PyTorch installation).

---

## License

This project is released under the MIT License.
