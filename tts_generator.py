from gtts import gTTS
import os

def generate_speech(text, output_file):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_file)
    
    # Convert to WAV format for better compatibility
    mp3_file = output_file
    wav_file = os.path.splitext(output_file)[0] + '.wav'
    os.system(f'ffmpeg -i {mp3_file} {wav_file}')
    os.remove(mp3_file)
    
    return wav_file