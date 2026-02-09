# cheating_detection.py
import torch

# Load YOLOv5 pretrained model
model = torch.hub.load(
    'ultralytics/yolov5',
    'yolov5s',
    pretrained=True
)

CLASS_NAMES = model.names
CHEATING_OBJECTS = ["cell phone"]

def detect_cheating(frame):
    if frame is None:
        return "No Cheating"

    results = model(frame)
    detections = results.xyxy[0]

    for *box, conf, cls in detections:
        label = CLASS_NAMES[int(cls)]

        # Mobile phone detected
        if label in CHEATING_OBJECTS:
            return "Cheating"

    return "No Cheating"
