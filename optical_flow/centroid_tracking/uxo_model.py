from enum import IntEnum
import pathlib
from typing import List, Union
from uuid import uuid1
import torch

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


class Mine_Type(IntEnum):
    # see "class" from YOLO results
    KSF_Casing = 0
    PFM_1 = 1


class UXO:
    def __init__(
        self, xmin, xmax, ymin, ymax, confidence, mine_type: Mine_Type
    ) -> None:
        self.confidence = confidence
        self.mine_type = mine_type
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self._gpsloc = None
        self.id = uuid1()

    @property
    def bb_center(self):
        y_center = self.ymin + ((self.ymax - self.ymin) / 2)
        x_center = self.xmin + ((self.xmax - self.xmin) / 2)
        return (x_center, y_center)

    @property
    def gps_location(self):
        return self._gpsloc

    @gps_location.setter
    def gps_location(self, val):
        self._gpsloc = val


def process_frame(
    image_path: str,
    modelname: str = "datasets/noise1.8-rot15/run1/train_results/weights/best.pt",
) -> Union[List[UXO], List[tuple]]:
    model = torch.hub.load("ultralytics/yolov5", "custom", modelname)
    model.cpu()

    rects = []
    results = model(image_path)
    uxos = create_uxo_object(results)
    for u in uxos:
        # (startX, startY, endX, endY)
        rects.append((u.xmin, u.ymin, u.xmax, u.ymax))
    return uxos, rects


def create_uxo_object(results) -> UXO:
    boxes = results.xyxy[0]
    found_mines = []
    for box in boxes:
        print(f"Found a mine!")
        # xmin ymin xmax ymax confidence class
        box_astuple = tuple(box.numpy())
        xmin, ymin, xmax, ymax, confidence, classi = box_astuple
        u = UXO(xmin, xmax, ymin, ymax, confidence, Mine_Type(classi))
        found_mines.append(u)
    return found_mines
