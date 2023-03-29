import cv2
from datetime import datetime

from pypylon import pylon


class Camera():
    def __init__(self):
        self.frame_count = 0
        self.start_time = cv2.getTickCount()

    def get_img(self):
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # ret, frame = cap.read()
            # if grabResult.GrabSucceeded():
            # Access the image dataq
            # if ret:
            image = converter.Convert(grabResult)
            img = image.GetArray()
            img = img[1200:1200+640, 1487:1487+640]
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            self.frame_count += 1
            elapsed_time = (cv2.getTickCount() - self.start_time) / cv2.getTickFrequency()
            fps = self.frame_count / elapsed_time

            img = cv2.putText(img, datetime.now().strftime("%d:%m:%y") + f" FPS: {fps:.2f}", org, font, fontScale, color, thickness,cv2.LINE_AA)
            # cv2.imshow("ss", img)
            yield img

