import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
import json
from libs.skeleton.skeleton import Skeleton
from libs.util import get_golden_circle


bones_indices = [
    [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
    [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
    [[0,7],[7,8],[8,9],[9,10]] # black
] # left-> pink, right->blue


def plot_camera(ax, position, axes, color='black'):
    ax.scatter(position[0], position[1], position[2], c=color)

    axes = axes/10
    ax.plot([position[0], (position+axes[0])[0]], [position[1], (position+axes[0])[1]], [position[2], (position+axes[0])[2]], c='r')
    ax.plot([position[0], (position+axes[1])[0]], [position[1], (position+axes[1])[1]], [position[2], (position+axes[1])[2]], c='g')
    ax.plot([position[0], (position+axes[2])[0]], [position[1], (position+axes[2])[1]], [position[2], (position+axes[2])[2]], c='b')

    return

def plot_golden_circle(ax):

    vertices, adjacency_matrix = get_golden_circle()
    connection = np.tril(adjacency_matrix, -1).T

    for i in range(connection.shape[0]):
        nodes = np.argwhere(connection[i]==1).flatten()
        for n in nodes:
            ax.plot([vertices[i][0], vertices[n][0]], [vertices[i][1], vertices[n][1]], [vertices[i][2], vertices[n][2]], c='gray')

    return

def plot_2d(joints2d, ax, xlim=[-1,1], ylim=[1,-1]):
    ax.set(xlim = xlim, ylim=ylim)
    sk = Skeleton()

    for _, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, = list(joints2d[start])
            x1, y1, = list(joints2d[end])
            ax.plot([x0, x1], [y0, y1])

    # draw dots
    for i in range(17):
        if sk.dict_idx_2_joint[i] in (sk.body_parts['torso'] + sk.body_parts['head']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='b')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='r')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='g')
        else:
            raise NotImplementedError


def plot_3d(joints3d, ax, elev=-70, azim=-90,  max_range=1):


    ax.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range,max_range])

    for _, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]
            x0, y0, z0 = list(joints3d[start])
            x1, y1, z1 = list(joints3d[end])
            ax.plot([x0, x1], [y0, y1], [z0, z1])
    # draw dots
    sk = Skeleton()
    for i in range(17):
        if sk.dict_idx_2_joint[i] in (sk.body_parts['torso'] + sk.body_parts['head']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='b')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='r')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='g')
        else:
            raise NotImplementedError
            
    ax.set(xlabel='x', ylabel='y', zlabel='z')
    ax.view_init(elev=elev, azim=azim)


if __name__ == '__main__':

    class_name = 'burpee'
    video_idx = 0
    frame_idx = 1

    joints2d_path = './dataset/joints2d/{}/{}_{:03d}/{:04d}.json'.format(class_name, class_name, video_idx, frame_idx)
    
    with open(joints2d_path, 'rb') as jsonfile:
        data = json.load(jsonfile)
        joints2d = np.array(data).reshape((17,-1))

    joints3d_path = joints2d_path.replace('joints2d', 'joints3d').replace('json', 'npy')
    joints3d = np.load(joints3d_path)


    fig1 = plt.figure(0, figsize=(10, 10), dpi=50)
    ax = fig1.add_subplot(111, projection="3d")
    plot_3d(joints3d, ax)

    fig2 = plt.figure(1, figsize=(10, 10), dpi=50)
    ax = fig2.add_subplot(111)
    plot_2d(joints2d, ax)
    

    plt.show()