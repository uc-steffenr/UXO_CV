from math import atan, pi, tan
import cv2
import numpy as np

from my_utils import long2UTM

# ----------------------------------------------
#               STATES
# ----------------------------------------------
altitude = 10  # m
speed = 2  # m/s
E0 = 420000  # m, object
N0 = 4600000  # m
long_brighampton = -75.970421  # °
utm_zone = long2UTM(long_brighampton)

# x,y,h,phi,theta,psi,u,v,w,p,q,r
states_const = np.array((E0, N0, altitude, 0, 0, 0, speed, 0, 0, 0, 0, 0))

# ----------------------------------------------
#           CAMERA PARAMETERS
# ----------------------------------------------
# see https://www.dji.com/phantom-4-pro/info
# f/2.8-f/11, autofocus at 1 m
fov = 84  # °
image_height = 4  # m
image_width = 6  # m
alpha_az = 0  # degrees
alpha_el = 0  # degrees

# ----------------------------------------------
#           CAMERA CALCULATIONS
# ----------------------------------------------
im = cv2.imread(r"C:\Git\UXO\UXO_CV\geoloc\ref_pic.jpg")
image_h_px, image_w_px, _ = im.shape
image_h_m = 2.321  # m
mperpx = image_h_m / image_h_px  # m/px
image_w_m = image_w_px * mperpx
focal_m = image_w_m / (2 * tan(((fov / 2) * pi / 180)))  # eqn 13.5
focal_px = focal_m / mperpx

# Calc Refs
# https://shotkit.com/field-of-view/#:~:text=On%20a%20full%2Dframe%20camera%2C%20a%20200mm%20lens%20would%20get,full%20180%2Ddegree%20horizontal%20FOV.
# https://photo.stackexchange.com/questions/97213/finding-focal-length-from-image-size-and-fov
