import os
import json
from pathlib import Path
from pprint import pprint
from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError
import time
from utils import get_first_frame
from face_recognition import recognize
from gtts import gTTS
from playsound import playsound

cache_file = Path("test_token.cache")


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

    devices = ring.devices()
    pprint(devices)
    wait_for_update(ring)


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
    frame = get_first_frame('last_ding.mp4')
    # os.remove('last_ding.mp4')
    try:
        people = recognize(frame)
        print('[INFO] finished detection in:', str(time.time() - start))
        if people is None:
            print('No one was detected')
            return None
    except LookupError:
        return None
    return_string = ''
    for person in people:
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