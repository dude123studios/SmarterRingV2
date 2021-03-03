import cv2


def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / (std + 1e-7)


def preprocess(cv2_img):
    cv2_img = normalize(cv2_img)
    cv2_img = cv2.resize(cv2_img, (160, 160))
    cv2_img = cv2_img / 127.5 - 1
    return cv2_img


frame_of_ring = 15 * 7


def get_first_frame(video_path):
    vidcap = cv2.VideoCapture(video_path)
    vidcap.set(1, frame_of_ring)
    success, image = vidcap.read()
    if success:
        return image


def get_specific_frames(video_path, times):
    vidcap = cv2.VideoCapture(video_path)
    frames = []
    for time in times:
        vidcap.set(1, time * 15)
        success, image = vidcap.read()
        if success:
            frames.append(image)
    return frames
