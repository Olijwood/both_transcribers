from pydub import AudioSegment
import os
import time
def main():
    cwd = os.getcwd() 
    unformatted_audio = f"{cwd}/unformatted_audio/"
    processed_audio = f'{cwd}/processed_audio/'
    if not os.path.isdir(unformatted_audio):
        os.mkdir(unformatted_audio)
    if not os.path.isdir(processed_audio):
        os.mkdir(processed_audio)
    for file in os.listdir(f'{unformatted_audio}'):
        if file.endswith('.wav'):
            raw_audio = AudioSegment.from_file(f'{unformatted_audio}{file}', format="wav")
            raw_audio.export(f"{processed_audio}{file.rstrip('.wav') + '_processed.wav'}_processed.wav", format="wav", codec="pcm_s16le", parameters=["-ac", "1", '-ar', '16000', '-b:a', '256k'])
        elif file.endswith('.mp3'):
            raw_audio = AudioSegment.from_file(f'{unformatted_audio}{file}', format="mp3")
            raw_audio.export(f"{unformatted_audio}{file.rstrip('.wav')}_processed.wav", format="wav", codec="pcm_s16le", parameters=["-ac", "1", '-ar', '16000', '-b:a', '256k'])
            for file in os.listdir(f'{unformatted_audio}'):
                if file.endswith('.mp3'):
                    os.remove(f"{unformatted_audio}{file}")
                for file in os.listdir(f'{unformatted_audio}'):
                    if file.endswith('.wav'):
                        raw_audio = AudioSegment.from_file(f'{unformatted_audio}{file}', format="wav")
                        raw_audio.export(f"{processed_audio}{file.rstrip('.wav') + '_processed.wav'}_processed.wav", format="wav", codec="pcm_s16le", parameters=["-ac", "1", '-ar', '16000', '-b:a', '256k'])
        elif file.endswith('.mp4'):
            raw_audio = AudioSegment.from_file(f'{unformatted_audio}{file}', format="mp4")
            raw_audio.export(f"{processed_audio}{file.rstrip('.wav') + '_processed.wav'}_processed.wav", format="wav", codec="pcm_s16le", parameters=["-ac", "1", '-ar', '16000', '-b:a', '256k'])
main()