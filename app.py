from elasticsearch import Elasticsearch
import torch
import time
import json
from datetime import datetime
import requests

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
vehicle_classes = {'car', 'motorcycle', 'bus', 'truck'}

# Connect to ES
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

INDEX = "dataframe"
TYPE = "record"


def rec_to_actions(df):
    import json
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}' % (INDEX, TYPE))
        yield (json.dumps(record, default=int))


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
    df['date'] = int(datetime.strftime(datetime.utcnow(), "%s"))
    doc = json.dumps(json.loads(df.to_json(orient="records")))
    print(doc)
    r = es.bulk(rec_to_actions(df))  # return a dict

    time.sleep(30)
