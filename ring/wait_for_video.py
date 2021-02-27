import os
import json
from pathlib import Path
from pprint import pprint
from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError
from ring.handle_video import handle_video
import time

cache_file = Path("test_token.cache")


def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("[INPUT] 2FA code: ")
    return auth_code


def main():
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


def wait_for_update(ring):
    id = -1
    start = time.time()
    while True:
        time.sleep(1)
        try:
            ring.update_data()
        except:
            continue
        doorbell = ring.devices()['authorized_doorbots'][0]
        for event in doorbell.history(limit=15, kind='ding'):
            current_id = event['id']
            break
        if current_id != id:
            id = current_id
            print('[INFO] finished search in:',str(time.time()-start))
            start = time.time()
            handle = handle_video(ring)
            if handle:
                print(handle)