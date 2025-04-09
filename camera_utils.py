import cv2

def initialize_camera():
    return cv2.VideoCapture(0)

def capture_image(camera, filename):
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(filename, frame)
