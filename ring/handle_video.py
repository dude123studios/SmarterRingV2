import time
from utils import get_first_frame
from detection.recognize import recognize


def handle_video(ring, download_only=False):
    devices = ring.devices()
    doorbell = devices['authorized_doorbots'][0]
    start = time.time()
    doorbell.recording_download(
        doorbell.history(limit=50, kind='ding')[0]['id'],
        filename='last_ding.mp4',
        override=True)
    print('[INFO] finished download in:', str(time.time() - start))
    if download_only:
        return
    start = time.time()
    frame = get_first_frame('last_ding.mp4')
    #os.remove('last_ding.mp4')
    try:
        people = recognize(frame)
        print('[INFO] finished detection in:', str(time.time() - start))
        if people is None:
            return None
    except LookupError:
        return None
    return_string = '[OUTPUT] '
    for person in people:
        return_string = return_string + person + ', '
    return_string = return_string + 'Are/Is at the door!'
    return return_string


