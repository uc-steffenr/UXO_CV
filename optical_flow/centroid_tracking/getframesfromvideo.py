import os
import cv2

vidcap = cv2.VideoCapture(
    r"C:\Git\UXO\UXO_CV\optical_flow\UXO-YOLOLabeled-SuperShort.mp4"
)
success, image = vidcap.read()
count = 0
while success:
    cv2.imwrite(
        os.path.join(
            r"C:\Git\UXO\UXO_CV\optical_flow\raw_supershort_frames",
            f"{count:02}frame.jpg",
        ),
        image,
    )  # save frame as JPEG file
    success, image = vidcap.read()
    print("Read a new frame: ", success)
    count += 1
