from glob import glob
import os
import sys
import cv2

sys.path.append(r"C:\Git\UXO\UXO_CV")
from optical_flow.centroid_tracking.centroidtracker import CentroidTracker
from optical_flow.centroid_tracking.uxo_model import process_frame

frames = glob(r"C:\Git\UXO\UXO_CV\optical_flow\raw_supershort_frames\*.jpg")
# print(frames)
ct = CentroidTracker()
i = 0
frames.sort()
for img in frames:
    print(f"Checking frame {i}/{len(frames)}")
    uxos, rectangles = process_frame(
        img, r"C:\Git\UXO\UXO_CV\optical_flow\reallyreallybig_run3_best.pt"
    )
    # for u in uxos:
    #     ct.register(u.bb_center)
    objects = ct.update(rectangles)
    img2 = cv2.imread(img)
    # img3 = img2.copy()

    # update our centroid tracker using the computed set of bounding box rectangles
    # objects = ct.update(rects)
    # loop over the tracked objects
    for objectID, centroid in ct.objects.items():
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        text = "ID {}".format(objectID)
        cv2.putText(
            img2,
            text,
            (int(centroid[0] - 10), int(centroid[1] - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        cv2.circle(img2, (int(centroid[0]), int(centroid[1])), 4, (0, 255, 0), -1)
    # show the output frame
    temp_path = os.path.join(
        r"C:\Git\UXO\UXO_CV\optical_flow\supershort_tracking", f"{i:02}frame.jpg"
    )
    print(temp_path)
    cv2.imwrite(temp_path, img2)
    # cv2.imshow(f"Frame {i}", img2)
    i += 1
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
