import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
import json
import os
import seaborn as sn
import pandas as pd

try:
    from libs.skeleton.skeleton import Skeleton
except:
    from labelling_ui.libs.skeleton.skeleton import Skeleton

def plot_2d(skeleton_2d, type, ax, xlim=[-1,1], ylim=[1,-1], xlabel='x', ylabel='y', title=''):
    if xlim is not None and ylim is not None:
        ax.set(xlim = xlim, ylim=ylim)
    sk = Skeleton(type)

    for body_part, joints in zip(sk.body_parts.keys(), sk.body_parts.values()):
        for i in range(1, len(joints)):
            start = sk.dict_joint_2_idx[joints[i-1]]
            end = sk.dict_joint_2_idx[joints[i]]
            x0, y0, = list(skeleton_2d[start])
            x1, y1, = list(skeleton_2d[end])
            ax.plot([x0, x1], [y0, y1], sk.body_parts_color[body_part])

    # draw dots
    for i in range(skeleton_2d.shape[0]):
        ax.scatter(skeleton_2d[i, 0], skeleton_2d[i, 1], c='black', s=2)

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

def plot_3d(skeleton_3d, type, ax, elev=-70, azim=-90,  max_range=1):

    ax.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range,max_range])
    sk = Skeleton(type)

    for body_part, joints in zip(sk.body_parts.keys(), sk.body_parts.values()):
        for i in range(1, len(joints)):
            start = sk.dict_joint_2_idx[joints[i-1]]
            end = sk.dict_joint_2_idx[joints[i]]
            x0, y0, z0 = list(skeleton_3d[start])
            x1, y1, z1= list(skeleton_3d[end])
            ax.plot([x0, x1], [y0, y1], [z0, z1], sk.body_parts_color[body_part])


    # draw dots
    for i in range(skeleton_3d.shape[0]):
        ax.scatter(skeleton_3d[i, 0], skeleton_3d[i, 1], skeleton_3d[i, 2], c='black', s=2)

            
    ax.set(xlabel='x', ylabel='y', zlabel='z')
    ax.view_init(elev=elev, azim=azim)