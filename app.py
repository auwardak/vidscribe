import gradio as gr
import whisper
import torch
import subprocess
import os
import tempfile

# Device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Model cache
models_cache = {}

# Make sure logs folder exists
os.makedirs("logs", exist_ok=True)

def get_model(model_size):
    if model_size not in models_cache:
        models_cache[model_size] = whisper.load_model(model_size, device=device)
    return models_cache[model_size]

def format_timestamp(seconds: float):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def transcribe(video_file, language, model_size):
    if video_file is None:
        return "No file provided.", None, None

    model = get_model(model_size)

    # Extract audio using ffmpeg
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.wav")
        cmd = [
            "ffmpeg", "-y", "-i", video_file,
            "-ac", "1", "-ar", "16000", audio_path
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return f"Audio extraction failed: {result.stderr.decode()}", None, None

        # Transcribe
        result = model.transcribe(audio_path, language=language, verbose=False)

    # Save transcript text
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    txt_output = os.path.join("logs", f"{base_name}.transcript.txt")
    with open(txt_output, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Save subtitles
    srt_output = f"{base_name}.srt"
    with open(srt_output, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    return result["text"], txt_output, srt_output

# === Gradio UI ===
with gr.Blocks(title="🎬 Vidscribe", theme=gr.themes.Default()) as app:

    gr.Markdown("## 🎧 Vidscribe\nUpload a video, select options, and generate transcripts & subtitles.")

    with gr.Row():
        # Left column: Video (increase height by 20px)
        with gr.Column(scale=2):
            video_input = gr.Video(label="🎥 Upload Video", height=270)

        # Right column: Options & controls (increase spacing)
        with gr.Column(scale=1, min_width=250):
            language = gr.Textbox(label="🌐 Language (ISO code)", value="ur", lines=2)
            model_size = gr.Dropdown(
                ["tiny", "base", "small", "medium", "large"],
                value="large",
                label="🧠 Model Size",
            )
            start_btn = gr.Button("🚀 Transcribe")

    # Output section: Transcript (reduce height by 20px)
    with gr.Row():
        output_text = gr.Textbox(label="📝 Transcript", lines=8, interactive=False)

    # Output row: Files
    with gr.Row():
        txt_file = gr.File(label="📄 Download Transcript (.txt)")
        srt_file = gr.File(label="💬 Download Subtitles (.srt)")

    start_btn.click(
        fn=transcribe,
        inputs=[video_input, language, model_size],
        outputs=[output_text, txt_file, srt_file]
    )

app.launch(favicon_path='favicon.png')
