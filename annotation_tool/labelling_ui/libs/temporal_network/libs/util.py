import math
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable

def get_range_lim(points):
    assert points.ndim == 3
    lims = []
    max_d = 0
    for i in range(points.shape[-1]):
        min_value = (np.amin(points[:,:,i])*0.9)
        max_value = (np.amax(points[:,:,i])*1.1)

        if max_value - min_value > max_d:
            max_d = max_value - min_value
        lims.append([min_value, max_value])
    for i in range(points.shape[-1]):
        lims[i][1] = lims[i][0] + max_d
    
    return lims

def plot_grad_flow(named_parameters):
    fig, ax = plt.subplots()
    ave_grads = []
    layers = []
    for n, p in named_parameters:
        if(p.requires_grad) and ("bias" not in n):
            layers.append(n)
            ave_grads.append(p.grad.abs().mean())
    ax.plot(ave_grads, alpha=0.3, color="b")
    ax.hlines(0, 0, len(ave_grads)+1, linewidth=1, color="k" )

    ax.set_xticks(range(0,len(ave_grads), 1))
    ax.set_xticklabels(layers, rotation=90)
    ax.set_xlim(xmin=0, xmax=len(ave_grads))
    # ax.set_ylim(ymin=0, ymax=2)
    ax.set_xlabel("Layers")
    ax.set_ylabel("average gradient")
    ax.set_title("Gradient flow")
    ax.grid()
    
    return fig

def cartesian_to_spherical(origin_pos, current_pos):
    dx = current_pos[0] - origin_pos[0]
    dy = current_pos[1] - origin_pos[1]
    dz = current_pos[2] - origin_pos[2]


    r = math.sqrt(dx*dx + dy*dy + dz*dz)
    theta = math.atan2(math.sqrt(dx*dx + dy*dy), dz)
    phi = math.atan2(dy, dx)

    return r, theta, phi

def spherical_to_cartesian(origin_pos, spherical_pos):
    r = spherical_pos[0]
    theta = spherical_pos[1]
    phi = spherical_pos[2]

    x = origin_pos[0] + r*math.sin(theta)*math.cos(phi)
    y = origin_pos[1] + r*math.sin(theta)*math.sin(phi)
    z = origin_pos[2] + r*math.cos(theta)

    return x, y, z


def cartesian_to_polar(origin_pos, current_pos):
    dx = current_pos[0] - origin_pos[0]
    dy = current_pos[1] - origin_pos[1]

    r = math.sqrt(dx*dx + dy*dy)
    theta = math.atan2(dy, dx)

    return r, theta

def polar_to_cartesian(origin_pos, polar_pos):
    r = polar_pos[0]
    theta = polar_pos[1]

    x = origin_pos[0] + r*math.cos(theta)
    y = origin_pos[1] + r*math.sin(theta)

    return x, y

def calculate_camera_matrix(points_3d, points_2d):

    M = np.zeros((3,4))

    num_joints = points_3d.shape[0]

    A = np.zeros((num_joints*2, 12))

    for i in range(num_joints):
        X_i = points_3d[i, 0]
        Y_i = points_3d[i, 1]
        Z_i = points_3d[i, 2]

        u_i = points_2d[i, 0]
        v_i = points_2d[i, 1]

        A[2*i, 0] = X_i
        A[2*i, 1] = Y_i
        A[2*i, 2] = Z_i
        A[2*i, 3] = 1
        A[2*i, 8] = -u_i * X_i
        A[2*i, 9] = -u_i * Y_i
        A[2*i, 10] = -u_i * Z_i
        A[2*i, 11] = -u_i

        A[2*i+1, 4] = X_i
        A[2*i+1, 5] = Y_i
        A[2*i+1, 6] = Z_i
        A[2*i+1, 7] = 1
        A[2*i+1, 8] = -v_i * X_i
        A[2*i+1, 9] = -v_i * Y_i
        A[2*i+1, 10] = -v_i * Z_i
        A[2*i+1, 11] = -v_i

    u, s, vh = np.linalg.svd(A)
    
    M = vh[-1].reshape((M.shape))

    return M

def project_3d_2_2d(M, points_3d):
    
    assert points_3d.shape[1] == 3

    homogeneous = np.concatenate([points_3d, np.ones((points_3d.shape[0], 1))], axis=-1).T
    projection = np.matmul(M, homogeneous).T
    projection = np.divide(projection[:, :2], np.expand_dims(projection[:, 2], axis=-1), out=np.zeros_like(projection[:, :2]), where=np.expand_dims(projection[:, 2], axis=-1)!=0)

    return projection

def calculate_homogeneous(points, points_dst):

    H = np.zeros((3,3))
    num_joints = points.shape[0]

    A = np.zeros((num_joints*2, 9))

    for i in range(num_joints):
        X_i = points[i, 0]
        Y_i = points[i, 1]

        x_i = points_dst[i, 0]
        y_i = points_dst[i, 1]

        A[2*i, 0] = X_i
        A[2*i, 1] = Y_i
        A[2*i, 2] = 1
        A[2*i, 6] = -x_i * X_i
        A[2*i, 7] = -x_i * Y_i
        A[2*i, 8] = -x_i

        A[2*i+1, 3] = X_i
        A[2*i+1, 4] = Y_i
        A[2*i+1, 5] = 1
        A[2*i+1, 6] = -y_i * X_i
        A[2*i+1, 7] = -y_i * Y_i
        A[2*i+1, 8] = -y_i


    u, s, vh = np.linalg.svd(A)
    
    H = vh[-1].reshape((H.shape))

    return H


def homogeneous_transform(H, points):
    
    assert points.shape[1] == 2

    homogeneous = np.concatenate([points, np.ones((points.shape[0], 1))], axis=-1).T
    projection = np.matmul(H, homogeneous).T
    projection = np.divide(projection[:, :-1], np.expand_dims(projection[:, -1], axis=-1), out=np.zeros_like(projection[:, :-1]), where=np.expand_dims(projection[:, -1], axis=-1)!=0)

    return projection

def rigid_transformation(points, points_dst):
    origin_idx = 0

    translation = points_dst[origin_idx] - points[origin_idx]

    remove_translation = points + translation

    s1 = np.sum(np.sqrt(np.sum(np.square(remove_translation - remove_translation[origin_idx]), axis=1)))
    s2 = np.sum(np.sqrt(np.sum(np.square(points_dst - points_dst[origin_idx]), axis=1)))
    scale = s2/s1

    return translation, scale


