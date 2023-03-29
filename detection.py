
import cv2
import numpy as np
from pypylon import pylon
import torch

class Detect():
    def __init__(self, ):
        # Parameters
        self.model = torch.hub.load('E:/vinh_Project/model_deep_learning/yolov5', 'custom', path='E:/vinh_Project/model_deep_learning/yolov5/runs/train/exp_nut_good/weights/best.pt', source='local')

    def detect(self, img):
        detection = self.model(img)
        rusult = detection.pandas().xyxy[0].to_dict(orient="records")
        x = np.array(rusult)
        if len(x):
            for result in rusult:
                confidence = round(result['confidence'], 2)
                name = result["name"]
                clas = result["class"]
                if confidence > 0.2:
                    x1 = int(result["xmin"])
                    y1 = int(result["ymin"])
                    x2 = int(result["xmax"])
                    y2 = int(result["ymax"])
                    # print(x1,y1,x2,y2)

                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(img, name, (x1 + 3, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)

        return cv2.imencode('.jpg', img)[1].tobytes()