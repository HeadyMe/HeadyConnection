import gradio as gr
from gtts import gTTS
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

def generate_speech(text, reference_audio=None):
    if not text:
        return None
    
    if reference_audio:
        print(f"Simulating voice cloning using reference: {reference_audio}")
    
    # Generate speech using gTTS
    tts = gTTS(text)
    
    # Save to a temporary file
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    tts.save(path)
    
    return path

def generate_waveform(audio_path):
    if not audio_path:
        return None
        
    # Load audio file
    y, sr = librosa.load(audio_path)
    
    # Create waveform plot
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio Waveform')
    plt.tight_layout()
    
    # Save plot to temporary file
    fd, img_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    plt.savefig(img_path)
    plt.close()
    
    return img_path

def process_interaction(text, avatar_image, reference_audio):
    # Generate speech
    audio_path = generate_speech(text, reference_audio)
    
    # Generate waveform visualization
    waveform_path = generate_waveform(audio_path)
    
    # Return generated assets and echo the avatar image
    return audio_path, waveform_path, avatar_image

# Build Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# AI Interface Application")
    gr.Markdown("Generate speech from text and visualize the waveform.")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Input Text", placeholder="Enter text to speak...")
            avatar_input = gr.Image(label="Avatar Image", type="filepath")
            ref_audio_input = gr.Audio(label="Reference Voice Sample", type="filepath")
            generate_btn = gr.Button("Generate")
        
        with gr.Column():
            output_audio = gr.Audio(label="Generated Speech")
            output_waveform = gr.Image(label="Waveform Visualization")
            output_avatar = gr.Image(label="Avatar Display")
            
    generate_btn.click(
        fn=process_interaction,
        inputs=[input_text, avatar_input, ref_audio_input],
        outputs=[output_audio, output_waveform, output_avatar]
    )

if __name__ == "__main__":
    demo.launch(share=True)
