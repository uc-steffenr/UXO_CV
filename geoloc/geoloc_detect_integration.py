import torch
import pathlib
import cv2
from constants import states_const
from geolocation import Geolocation

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

MODEL_NAME = "datasets/noise1.8-rot15/run1/train_results/weights/best.pt"

model = torch.hub.load("ultralytics/yolov5", "custom", MODEL_NAME)
model.cpu()

IMAGE_PATH = r"C:\Git\UXO\UXO_CV\geoloc\TwoMines_DifferentTypes.jpg"

results = model(IMAGE_PATH)
results.print()
print(results.pandas().xyxy[0])

boxes = results.xyxy[0]
points = []
full_pxs = []
for box in boxes:
    # xmin ymin xmax ymax confidence class
    box_astuple = tuple(box.numpy())
    xmin, ymin, xmax, ymax, confidence, classi = box_astuple

    y_center = ymin + ((ymax - ymin) / 2)
    x_center = xmin + ((xmax - xmin) / 2)

    points.append((int(x_center), int(y_center)))
    full_pxs.append((x_center, y_center))

g = Geolocation()
gps_points = []
for px in full_pxs:
    out = g.get_target_loc(px[0], px[1], states_const)
    out2 = g.get_lat_long(out)
    gps_points.append((round(out2[0], 2), round(out2[1], 2)))

img = cv2.imread(IMAGE_PATH)
img2 = img.copy()

for p in points:
    cv2.circle(img2, p, 3, (255, 0, 0), -1, lineType=cv2.LINE_AA)
    cv2.putText(
        img2,
        f"{gps_points[0]}",
        p,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2,
    )

cv2.imshow("Annotated Image", img2)
cv2.waitKey(0)
