# YOLOv5 Implementation for UXO Detection

This is a repository for preprocessing the orthoimages and original
labeled images from the [Binghampton Open Repository](https://orb.binghamton.edu/geology_fac/) (BOR) and training
a YOLOv5 model on those images. 

## Preprocessing

In the preprocessing step, databases are set up with the original labeled images
from BOR as well as the current iteration of split/augmented orthoimages. Orthoimages
are split using a package called `impy`. A few modifications were made to this, and
the modifications to that package are included in this repository.

Since `impy` is no longer supported, it requires using a subprocess to open the
proper conda environment, use impy to split the orthoimages and label the split
images correctly, and then to save those files to the database. There, the xml
format of the annotations are now converted to a format for YOLO to read.

The requested dataset is then made. The difference between a dataset and a database
is that a dataset can have different variations of training, testing, and validation
data, whereas a database is simply the place for processed data to be stored. Once
The dataset is made with the proper distribution of training, testing, and validation 
data, a `yaml` file is made so that YOLO can use it for training.

For access to images used for training, validation, and testing, see [here](https://mailuc-my.sharepoint.com/:f:/r/personal/steffenr_mail_uc_edu/Documents/UAV%20Design/UXO%20%F0%9F%92%A3?csf=1&web=1&e=f7bM14).

## Training

The training step is simple. All it does it invoke YOLO from `ultralytics`, define a
model, and train that model based on the specified hyperparameters.

## Tuning

...

## Archive

Previous attempts are stored here for future reference.

## Resources

Will be put in as citations later. See resources tab.

## TODO

- Make valdation method
- Get rest of annotations
- Look into adding noise to images
- Figure out how to get yolov5n.pt instead of yolov5s.pt
- Turn this into a git repo
- Program to compare `faster_rcnn_1_50_10067.pth` to weights from yolo
