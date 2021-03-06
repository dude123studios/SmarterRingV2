import cv2


def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / (std + 1e-7)


def preprocess(cv2_img):
    cv2_img = normalize(cv2_img)
    cv2_img = cv2.resize(cv2_img, (160, 160))
    return cv2_img


def get_specific_frames(video_path, times):
    vidcap = cv2.VideoCapture(video_path)
    frames = []
    for time in times:
        vidcap.set(1, time * 15)
        success, image = vidcap.read()
        if success:
            frames.append(image)
    return frames
