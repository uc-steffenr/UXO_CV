from math import sin, cos, sqrt
import numpy as np
from constants import focal_px, alpha_az, alpha_el, states_const
from utils import pretty_print


class Geolocation:
    def __init__(self) -> None:
        pass

    def get_target_loc(
        self,
        px,
        py,
        states,
        focal_px=focal_px,
        alpha_az_deg=alpha_az,
        alpha_el_deg=alpha_el,
        print_matricies: bool = False,
    ):
        alpha_az = alpha_az_deg * np.pi / 180
        alpha_el = alpha_el_deg * np.pi / 180

        x = states.item(0)
        y = states.item(1)
        h = states.item(2)
        phi = states.item(3)
        theta = states.item(4)
        psi = states.item(5)
        u = states[6]
        v = states[7]
        w = states[8]
        p = states[9]
        q = states[10]
        r = states[11]

        pn = x
        pe = y
        pd = h

        gimbal1_frame = np.array(
            [
                [cos(alpha_az), sin(alpha_az), 0],
                [-sin(alpha_az), cos(alpha_az), 0],
                [0, 0, 1],
            ]
        )

        gimbal_frame = np.array(
            [
                [cos(alpha_el), 0, -sin(alpha_el)],
                [0, 1, 0],
                [sin(alpha_el), 0, cos(alpha_el)],
            ]
        )

        body2gimbal = gimbal_frame @ gimbal1_frame
        Rbg = body2gimbal

        gimbal2camera = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        Rgc = gimbal2camera

        puav_i = np.array([[pn], [pe], [pd]])
        Rib = np.array(
            [
                [cos(theta) * cos(psi), cos(theta) * sin(psi), -sin(theta)],
                [
                    sin(phi) * sin(theta) * cos(psi) - cos(phi) * sin(psi),
                    sin(phi) * sin(theta) * sin(psi) + cos(phi) * cos(psi),
                    sin(phi) * cos(theta),
                ],
                [
                    cos(phi) * sin(theta) * cos(psi) + sin(phi) * sin(psi),
                    cos(phi) * sin(theta) * sin(psi) - sin(phi) * cos(psi),
                    cos(phi) * cos(theta),
                ],
            ]
        )

        ki = np.array([[0, 0, 1]])
        l0c = (
            1
            / sqrt(px**2 + py**2 + focal_px**2)
            * np.array([[px], [py], [focal_px]])
        )
        cos_Phi = ki @ (Rib @ Rbg @ Rgc @ l0c)
        L = h / cos_Phi
        pobj_i = puav_i + L * (Rib @ Rbg @ Rgc @ l0c)
        pretty_print(pobj_i, "Target Location (Inertial Frame)")
        return pobj_i

    def get_target_loc_with_ekf():
        pass

    def get_target_loc_utm():
        pass


if __name__ == "__main__":
    _px = 1
    _py = 1
    g = Geolocation()
    g.get_target_loc(_px, _py, states_const)
