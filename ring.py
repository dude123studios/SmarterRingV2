import os
import json
from pathlib import Path
from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError
import time
from utils import get_specific_frames
from face_recognition import recognize
from gtts import gTTS
from playsound import playsound

cache_file = Path("test_token.cache")
times = [5, 10, 15]


def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("[INPUT] 2FA code: ")
    return auth_code


def main(download_only=False):
    if cache_file.is_file():
        auth = Auth("MyProject/1.0", json.loads(cache_file.read_text()), token_updated)
    else:
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        auth = Auth("MyProject/1.0", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()

    wait_for_update(ring, download_only=download_only)


def wait_for_update(ring, download_only=False):
    id = -1
    start = time.time()
    while True:
        try:
            ring.update_data()
        except:
            time.sleep(1)
            continue
        doorbell = ring.devices()['authorized_doorbots'][0]
        for event in doorbell.history(limit=20, kind='ding'):
            current_id = event['id']
            break
        if current_id != id:
            id = current_id
            print('[INFO] finished search in:', str(time.time() - start))
            start = time.time()
            if download_only:
                handle_video(ring, True)
                return
            handle = handle_video(ring)
            if handle:
                text_to_speech(handle)
            else:
                text_to_speech('The person at the door is not very clear')
        time.sleep(1)


def handle_video(ring, download_only=False):
    devices = ring.devices()
    doorbell = devices['authorized_doorbots'][0]
    start = time.time()
    doorbell.recording_download(
        doorbell.history(limit=100, kind='ding')[0]['id'],
        filename='last_ding.mp4',
        override=True)
    print('[INFO] finished download in:', str(time.time() - start))
    if download_only:
        return
    start = time.time()
    frames = get_specific_frames('last_ding.mp4', times)
    # os.remove('last_ding.mp4')
    for frame in frames:
        people = recognize(frame)
        print('[INFO] finished detection in:', str(time.time() - start))
        if people is None:
            continue
        else:
            break
    if people is None:
        return None
    return_string = ''
    for i, person in enumerate(people):
        if (i == len(people)-1) and (len(people) is not 1):
            return_string += ('and '+person)
            break
        return_string += (person + ', ')
    if len(people) == 1:
        return_string += 'is at the door'
    else:
        return_string += 'are at the door'
    return return_string


language = 'en'
slow_audio_speed = False
filename = 'tts_file.mp3'


def text_to_speech(text):
    audio_created = gTTS(text=text, lang=language,
                         slow=slow_audio_speed)
    audio_created.save(filename)
    playsound(filename)
