from gtts import gTTS
from playsound import playsound

language = 'en'
slow_audio_speed = False
filename = 'tts_file.mp3'


def text_to_speech(text):
    audio_created = gTTS(text=text, lang=language,
                         slow=slow_audio_speed)
    audio_created.save(filename)
    playsound(filename)
