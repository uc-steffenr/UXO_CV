from glob import glob
import os
import sys
from typing import Tuple
import cv2

MODEL = r"C:\Git\UXO\UXO_CV\optical_flow\super-big-augmented-medium.pt"
INPUT_DIR = r"C:\Git\UXO\UXO_CV\optical_flow\240226-1301_flighttest\raw-short"
OUTPUT_DIR = r"C:\Git\UXO\UXO_CV\optical_flow\240226-1301_flighttest\processed-short"
UNCONFIRMED_COLOR = (230, 16, 34)
CONFIRMED_COLOR = (94, 16, 230)
SHOW_FRAMES = False


def annotate_image(
    img, point_id: int, centroid: Tuple[int, int], color: Tuple[int, int, int]
):
    text = f"ID {point_id}"
    cv2.putText(
        img,
        text,
        (int(centroid[0] - 10), int(centroid[1] - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
    )
    cv2.circle(
        img,
        (int(centroid[0]), int(centroid[1])),
        4,
        color,
        -1,
    )


sys.path.append(r"C:\Git\UXO\UXO_CV")
from optical_flow.centroid_tracking.centroidtracker import CentroidTracker
from optical_flow.centroid_tracking.uxo_model import process_frame

frames = glob(os.path.join(INPUT_DIR, "*.jpg"))
ct = CentroidTracker()
i = 0
frames.sort()
for img in frames:
    print(f"Checking frame {i+1}/{len(frames)}")
    uxos, rectangles = process_frame(img, MODEL, 0.4)
    objects = ct.update(rectangles)
    img2 = cv2.imread(img)
    # img3 = img2.copy()
    if objects:
        for objectID, centroid in objects.items():
            if objectID not in ct.disappeared_objects:
                print(f"Tracking object: {objectID}")
                if objectID in ct.all_known_objects.keys():
                    annotate_image(img2, objectID, centroid, CONFIRMED_COLOR)
                else:
                    annotate_image(img2, objectID, centroid, UNCONFIRMED_COLOR)
            else:
                print(f"Oops -- looks like object {objectID} has disappeared")
        # show the output frame
    temp_path = os.path.join(OUTPUT_DIR, f"{i:03}frame.jpg")
    cv2.imwrite(temp_path, img2)
    if SHOW_FRAMES:
        cv2.imshow(f"Frame {i}", img2)
    i += 1
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
