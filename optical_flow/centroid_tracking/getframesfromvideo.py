import os
import cv2

INPUT_VIDEO = r"C:\Git\UXO\UXO_CV\optical_flow\240204_flighttest\raw\UXO-YOLOLabeled-Cropped-5sec.mp4"
OUTPUT_DIR = r"C:\Git\UXO\UXO_CV\optical_flow\240204_flighttest\processed"

vidcap = cv2.VideoCapture(INPUT_VIDEO)
success, image = vidcap.read()
count = 0
while success:
    cv2.imwrite(
        os.path.join(
            OUTPUT_DIR,
            f"{count:03}frame.jpg",
        ),
        image,
    )  # save frame as JPEG file
    success, image = vidcap.read()
    print("Read a new frame: ", success)
    count += 1
