#! /bin/bash

weights=datasets/noise1.8-rot15/run1/train_results/weights/best.pt          # model path or triton URL
source=datasets/noise1.8-rot15/test/images                                  # optional file/dir/URL/glob/screen/0(webcam)
data=                                                                       # optional dataset.yaml path
imgsz=                                                                      # optional inference size h, w
conf_thresh=                                                                # optional confidence threshold
iou_thresh=                                                                 # optional NMS IoU theshold
device=                                                                     # optional cuda device, i.e. 0 or 0,1,2,3 or cpu
view_img=false                                                              # optional show results
save_txt=true                                                               # optional save results to *.txt
save_csv=true                                                               # optional save results to CSV format
save_conf=true                                                              # optional save confidences in --save-txt labels
save_crop=false                                                             # optional save cropped prediction boxes
nosave=false                                                                # optional do not save images/videos
classes=1                                                                   # optional filter by class: --classes 0, or --classes 0 2 3
augment=false                                                               # optional augmented inference
visualize=false                                                             # optional visualize features
project=datasets/noise1.8-rot15/run1                                        # optional save results to project/name
name=detections                                                             # optional save results to project/name
exist_ok=true                                                               # optional existing project/name ok, do not increment
line_thickness=                                                             # optional bounding box thickness (pixels)
vid_stride=                                                                 # optional video frame-rate stride


cmd="python yolov5/detect.py --weights ${weights}"

[[ -n $source ]] && cmd+=" --source ${source}"
[[ -n $data ]] && cmd+=" --data ${data}"
[[ -n $imgsz ]] && cmd+=" --imgsz ${imgsz}"
[[ -n $conf_thresh ]] && cmd+=" --conf-thres ${conf_thresh}"
[[ -n $iou_thresh ]] && cmd+=" --iou-thres ${iou_thresh}"
[[ -n $device ]] && cmd+=" --device ${device}"

$view_img && cmd+=" --view-img"
$save_txt && cmd+=" --save-txt"
$save_csv && cmd+=" --save-csv"
$save_conf && cmd+=" --save-conf"
$save_crop && cmd+=" --save-crop"
$nosave && cmd+=" --nosave"
$augment && cmd+=" --augment"
$visualize && cmd+=" --visualize"
$exist_ok && cmd+=" --exist-ok"

[[ -n $classes ]] && cmd+=" --classes ${classes}"
[[ -n $project ]] && cmd+=" --project ${project}"
[[ -n $name ]] && cmd+=" --name ${name}"
[[ -n $line_thickness ]] && cmd+=" --line-thickness ${line_thickness}"
[[ -n $vid_stride ]] && cmd+=" --vid-stride ${vid_stride}"

echo $cmd
eval $cmd
