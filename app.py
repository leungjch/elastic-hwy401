import torch
import time
from datetime import datetime

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
vehicle_classes = {'car', 'motorcycle', 'bus', 'truck'}
# Images
while True:
    now = datetime.now()

    dt_string = now.strftime("%d-%m-%Y/%H:%M:%S")

    imgs = ['https://511on.ca/map/Cctv/loc18--2']  # batch of images

    # Inference
    results = model(imgs)

    # Results
    results.print()
    results.save(dt_string)  # or .show()

    results.xyxy[0]  # img1 predictions (tensor)
    df = results.pandas().xyxy[0]  # img1 predictions (pandas)

    # Filter vehicles only
    df['is_vehicle'] = df['name'].apply(
        lambda x: (1 if x in vehicle_classes else 0))
    df = df[df.is_vehicle == 1]
    df.to_json(dt_string + "/result.json", orient="records")
    print(df)
    time.sleep(30)
