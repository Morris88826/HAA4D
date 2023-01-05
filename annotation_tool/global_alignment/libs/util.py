import numpy as np
import math

def get_rotation_matrix(theta_x, theta_y, theta_z):

    Rx = np.identity(3)
    Ry = np.identity(3)
    Rz = np.identity(3)

    Rx[1:, 1:] = np.array(
        [[math.cos(theta_x), -math.sin(theta_x)],
        [math.sin(theta_x), math.cos(theta_x)]]
    )


    Ry[0,0] = math.cos(theta_y)
    Ry[0,2] = math.sin(theta_y)
    Ry[2,0] = -math.sin(theta_y)
    Ry[2,2] = math.cos(theta_y)


    Rz[:-1, :-1] = np.array(
        [[math.cos(theta_z), -math.sin(theta_z)],
        [math.sin(theta_z), math.cos(theta_z)]]
    )

    R = np.linalg.multi_dot([Rz, Ry, Rx])

    return R